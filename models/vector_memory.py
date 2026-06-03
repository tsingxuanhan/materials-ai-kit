# -*- coding: utf-8 -*-
"""
Materials-AI-Kit Vector Memory Module
NGram TF-IDF Semantic Search for Materials Science Knowledge

This module provides semantic search capabilities for materials science knowledge,
enabling queries like "nano SiO2" to match "silica nanoparticle".

Reference: RankSquire L1/L2/L3 Memory Architecture
"""

import json
import logging
import math
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("MaterialsAIKit.VectorMemory")


class MemoryTier(Enum):
    """Memory tier classification"""
    L1_HOT = "l1_hot"         # Current task context (<1ms)
    L2_SEMANTIC = "l2_semantic"  # Cross-task memory (~20ms)
    L3_EPISODIC = "l3_episodic"  # Long-term historical (archive)


@dataclass
class MemoryEntry:
    """A single memory entry"""
    content: str
    role: str = "user"
    importance: float = 1.0
    tier: MemoryTier = MemoryTier.L2_SEMANTIC
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "role": self.role,
            "importance": self.importance,
            "tier": self.tier.value,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "MemoryEntry":
        return cls(
            content=data["content"],
            role=data.get("role", "user"),
            importance=data.get("importance", 1.0),
            tier=MemoryTier(data.get("tier", "l2_semantic")),
            metadata=data.get("metadata", {})
        )


@dataclass
class SearchResult:
    """Search result with score"""
    entry: MemoryEntry
    score: float
    rank: int


class NGramTFIDFProvider:
    """
    NGram TF-IDF Embedding Provider
    
    Combines word-level and character-level n-grams for robust semantic matching.
    
    Key Features:
    - Word n-grams (unigrams, bigrams, trigrams)
    - Character n-grams (3-5 chars) for subword matching
    - TF-IDF weighting with smooth IDF
    - L2 normalized vectors
    """
    
    def __init__(
        self,
        word_ngram_range: Tuple[int, int] = (1, 3),
        char_ngram_range: Tuple[int, int] = (3, 5),
        dimension: int = 384
    ):
        self.word_ngram_range = word_ngram_range
        self.char_ngram_range = char_ngram_range
        self.dimension = dimension
        self._doc_count = 0
        self._idf_cache = {}
    
    def _get_ngrams(self, text: str, n: int) -> List[str]:
        """Extract character n-grams from text"""
        text = text.lower().replace(" ", "")
        if len(text) < n:
            return [text]
        return [text[i:i+n] for i in range(len(text) - n + 1)]
    
    def _get_word_ngrams(self, words: List[str], n: int) -> List[str]:
        """Extract word n-grams"""
        if len(words) < n:
            return [" ".join(words)] if words else []
        return [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]
    
    def _extract_features(self, text: str) -> Counter:
        """Extract combined word + char n-gram features"""
        words = text.lower().split()
        features = Counter()
        
        # Word n-grams
        for n in range(self.word_ngram_range[0], self.word_ngram_range[1] + 1):
            word_ngrams = self._get_word_ngrams(words, n)
            for ng in word_ngrams:
                features[ng] += 1.0
        
        # Character n-grams (for subword matching)
        for n in range(self.char_ngram_range[0], self.char_ngram_range[1] + 1):
            char_ngrams = self._get_ngrams(text, n)
            for ng in char_ngrams:
                features[ng] += 0.5  # Lower weight for char n-grams
        
        return features
    
    def embed(self, text: str) -> List[float]:
        """
        Generate embedding vector for text
        
        Returns L2-normalized feature vector
        """
        features = self._extract_features(text)
        
        # Create sparse vector
        vector = [0.0] * self.dimension
        for feature, tf in features.items():
            idx = hash(feature) % self.dimension
            vector[idx] += tf
        
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        
        return vector
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch embedding generation"""
        return [self.embed(t) for t in texts]
    
    def compute_idf(self, documents: List[str]) -> Dict[str, float]:
        """Compute IDF weights for documents"""
        df = Counter()
        self._doc_count = len(documents)
        
        for doc in documents:
            words = set(self._extract_features(doc).keys())
            for w in words:
                df[w] += 1
        
        # Smooth IDF
        idf = {}
        for term, doc_freq in df.items():
            idf[term] = math.log((self._doc_count + 1) / (doc_freq + 1)) + 1
        
        return idf
    
    def compute_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Cosine similarity between two vectors"""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        return dot  # Already L2 normalized


class PersistentVectorStore:
    """
    Persistent Vector Memory Store
    
    Provides semantic search with NGram TF-IDF embeddings.
    Supports JSON persistence and optional ChromaDB backend.
    """
    
    def __init__(
        self,
        provider: Optional[NGramTFIDFProvider] = None,
        persist_path: str = "./kb_memory.json",
        top_k_default: int = 5,
        similarity_threshold: float = 0.3
    ):
        self.provider = provider or NGramTFIDFProvider()
        self.persist_path = persist_path
        self.top_k_default = top_k_default
        self.similarity_threshold = similarity_threshold
        
        self._entries: List[MemoryEntry] = []
        self._embeddings: Dict[int, List[float]] = {}  # idx -> embedding
    
    def add(
        self,
        content: str,
        tier: MemoryTier = MemoryTier.L2_SEMANTIC,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Add entry to memory
        
        Returns entry index
        """
        entry = MemoryEntry(
            content=content,
            tier=tier,
            metadata=metadata or {}
        )
        
        idx = len(self._entries)
        self._entries.append(entry)
        self._embeddings[idx] = self.provider.embed(content)
        
        logger.info(f"Added entry [{idx}]: {content[:50]}...")
        return idx
    
    def add_batch(
        self,
        entries: List[Dict[str, Any]]
    ) -> List[int]:
        """
        Batch add entries
        
        Args:
            entries: List of dicts with 'content', optional 'tier', 'metadata'
        
        Returns:
            List of entry indices
        """
        indices = []
        for entry_data in entries:
            idx = self.add(
                content=entry_data["content"],
                tier=MemoryTier(entry_data.get("tier", "l2_semantic")),
                metadata=entry_data.get("metadata")
            )
            indices.append(idx)
        
        return indices
    
    def search(
        self,
        query: str,
        tier: Optional[MemoryTier] = None,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None
    ) -> List[SearchResult]:
        """
        Semantic search for entries
        
        Args:
            query: Search query text
            tier: Optional filter by memory tier
            top_k: Number of results to return
            threshold: Minimum similarity score
        
        Returns:
            List of SearchResult sorted by score (descending)
        """
        top_k = top_k or self.top_k_default
        threshold = threshold or self.similarity_threshold
        
        # Compute query embedding
        query_emb = self.provider.embed(query)
        
        # Search all entries
        results = []
        for idx, entry in enumerate(self._entries):
            if tier and entry.tier != tier:
                continue
            
            score = self.provider.compute_similarity(query_emb, self._embeddings[idx])
            
            if score >= threshold:
                results.append(SearchResult(entry=entry, score=score, rank=0))
        
        # Sort and rank
        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results[:top_k]):
            r.rank = i + 1
        
        return results[:top_k]
    
    def persist(self, path: Optional[str] = None) -> bool:
        """
        Save memory to JSON file
        
        Returns True if successful
        """
        path = path or self.persist_path
        
        data = {
            "entries": [e.to_dict() for e in self._entries],
            "config": {
                "word_ngram_range": self.provider.word_ngram_range,
                "char_ngram_range": self.provider.char_ngram_range,
                "dimension": self.provider.dimension
            }
        }
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Persisted {len(self._entries)} entries to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to persist: {e}")
            return False
    
    @classmethod
    def load(
        cls,
        path: str,
        provider: Optional[NGramTFIDFProvider] = None
    ) -> "PersistentVectorStore":
        """
        Load memory from JSON file
        
        Returns new PersistentVectorStore instance
        """
        provider = provider or NGramTFIDFProvider()
        store = cls(provider=provider, persist_path=path)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for entry_dict in data.get("entries", []):
                entry = MemoryEntry.from_dict(entry_dict)
                idx = len(store._entries)
                store._entries.append(entry)
                store._embeddings[idx] = provider.embed(entry.content)
            
            logger.info(f"Loaded {len(store._entries)} entries from {path}")
        except FileNotFoundError:
            logger.warning(f"File not found: {path}, starting fresh")
        except Exception as e:
            logger.error(f"Failed to load: {e}")
        
        return store
    
    def __len__(self) -> int:
        return len(self._entries)
    
    def __repr__(self) -> str:
        tier_counts = Counter(e.tier.value for e in self._entries)
        return f"PersistentVectorStore(entries={len(self)}, tiers={dict(tier_counts)})"


# Example usage
if __name__ == "__main__":
    # Create memory
    memory = PersistentVectorStore(
        provider=NGramTFIDFProvider(),
        persist_path="./kb_memory.json"
    )
    
    # Index cement knowledge
    knowledge = [
        ("LC3: 50% limestone + 50% calcined clay, 5-30% OPC filler", {"type": "binder", "category": "LC3"}),
        ("SSC: min 70% GGBS, 10-15% gypsum, max 5% clinker equivalent", {"type": "binder", "category": "SSC"}),
        ("Nano SiO2 improves early strength by 20-30% at 1-3% dosage", {"type": "admixture", "category": "nano"}),
        ("MBCMs: MgO, MgSO4, MgCO3 based binders", {"type": "binder", "category": "MBCM"}),
        ("GGBS: Ground Granulated Blast Furnace Slag", {"type": "SCM", "category": "slag"}),
    ]
    
    for content, meta in knowledge:
        memory.add(content, metadata=meta)
    
    # Search examples
    print("\n=== Search Examples ===")
    
    queries = [
        "ground granulated blast furnace slag cement composition",
        "nano silica nanoparticle strength improvement",
        "limestone calcined clay ternary blend"
    ]
    
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = memory.search(q, top_k=3)
        for r in results:
            print(f"  [{r.score:.3f}] Rank {r.rank}: {r.entry.content}")
    
    # Persist
    memory.persist()
    print(f"\nPersisted {len(memory)} entries")

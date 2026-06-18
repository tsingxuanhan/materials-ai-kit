#!/usr/bin/env python3
"""系统巡检 — 检查显存、磁盘、服务状态"""
import subprocess
import shutil
import psutil

def check_gpu():
    """检查GPU显存使用"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        used, total = result.stdout.strip().split(", ")
        used_gb = float(used) / 1024
        total_gb = float(total) / 1024
        pct = used_gb / total_gb * 100
        status = "✅" if pct < 80 else "⚠️" if pct < 95 else "❌"
        print(f"{status} GPU VRAM: {used_gb:.1f}GB / {total_gb:.1f}GB ({pct:.0f}%)")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

def check_disk():
    """检查磁盘空间"""
    for drive in ["C:\\", "D:\\"]:
        try:
            usage = shutil.disk_usage(drive)
            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            pct = (1 - free_gb/total_gb) * 100
            status = "✅" if free_gb > 10 else "⚠️" if free_gb > 3 else "❌"
            print(f"{status} {drive}: {free_gb:.1f}GB free / {total_gb:.1f}GB")
        except:
            pass

def check_services():
    """检查关键服务"""
    services = {
        "Ollama": ("http://127.0.0.1:11434", "ollama"),
        "Open WebUI": ("http://127.0.0.1:3000", None),
        "ComfyUI": ("http://127.0.0.1:8188", None),
        "JupyterLab": ("http://127.0.0.1:8888", None),
        "Portainer": ("http://127.0.0.1:9000", None),
    }
    import urllib.request
    for name, (url, proc) in services.items():
        try:
            req = urllib.request.Request(url, method='HEAD')
            urllib.request.urlopen(req, timeout=2)
            print(f"✅ {name}: running")
        except:
            print(f"❌ {name}: not responding")

def main():
    print("=== System Health Check ===\n")
    check_gpu()
    print()
    check_disk()
    print()
    check_services()
    print("\n=== Done ===")

if __name__ == "__main__":
    main()

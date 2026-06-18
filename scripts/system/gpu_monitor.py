#!/usr/bin/env python3
"""GPU显存实时监控"""
import subprocess
import time
import sys

def monitor_gpu(interval=2):
    """实时监控GPU显存使用"""
    print("GPU Memory Monitor | Ctrl+C to exit")
    print("-" * 50)
    try:
        while True:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.used,memory.total,temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True
            )
            used, total, temp = result.stdout.strip().split(", ")
            used_gb = float(used) / 1024
            total_gb = float(total) / 1024
            pct = used_gb / total_gb * 100

            bar_len = 40
            filled = int(bar_len * pct / 100)
            bar = "█" * filled + "░" * (bar_len - filled)

            print(f"\rVRAM: [{bar}] {used_gb:.1f}/{total_gb:.1f}GB ({pct:.0f}%) | {temp}°C", end="")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 2
    monitor_gpu(interval)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSI_LAUNCHER.py

External RSI Loop Launcher
==========================
This script runs the RSI engine in a proper subprocess loop,
ensuring that after each self-modification, the NEW code is
actually executed (not the old in-memory version).

Usage:
  python RSI_LAUNCHER.py --rounds 10 --gens 50

What it does:
1. Run: evolve (train the engine)
2. Run: autopatch --apply (attempt self-modification)
3. If file changed → restart from step 1 with NEW code
4. Repeat for N rounds
"""

import subprocess
import sys
import time
import hashlib
from pathlib import Path

TARGET_SCRIPT = Path(__file__).parent / "UNIFIED_RSI_EXTENDED.py"

def file_hash(p: Path) -> str:
    """Get SHA256 hash of file contents."""
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run_evolve(gens: int, pop: int, resume: bool) -> bool:
    """Run evolution phase. Returns True if successful."""
    args = [sys.executable, str(TARGET_SCRIPT), "evolve"]
    if not resume:
        args.append("--fresh")
    args.extend(["--generations", str(gens), "--population", str(pop), "--universes", "2"])
    
    print(f"\n{'='*60}")
    print(f"[EVOLVE] Running {gens} generations...")
    print(f"{'='*60}\n")
    
    result = subprocess.run(args, cwd=str(TARGET_SCRIPT.parent))
    return result.returncode == 0

def run_autopatch(levels: str) -> dict:
    """Run autopatch phase. Returns info about what happened."""
    args = [sys.executable, str(TARGET_SCRIPT), "autopatch", 
            "--levels", levels, "--candidates", "6", "--apply"]
    
    print(f"\n{'='*60}")
    print(f"[AUTOPATCH] Attempting self-modification (L{levels})...")
    print(f"{'='*60}\n")
    
    result = subprocess.run(args, cwd=str(TARGET_SCRIPT.parent), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return {
        "returncode": result.returncode,
        "output": result.stdout,
        "applied": "Applied" in result.stdout or "applied" in result.stdout
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="External RSI Loop Launcher")
    parser.add_argument("--rounds", type=int, default=5, help="Number of RSI rounds")
    parser.add_argument("--gens", type=int, default=50, help="Generations per round")
    parser.add_argument("--pop", type=int, default=64, help="Population size")
    parser.add_argument("--levels", default="0,1,3,5", help="Autopatch levels to try")
    args = parser.parse_args()
    
    if not TARGET_SCRIPT.exists():
        print(f"[ERROR] Target script not found: {TARGET_SCRIPT}")
        return 1
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           RSI LAUNCHER - External Re-execution Loop          ║
╠══════════════════════════════════════════════════════════════╣
║  Target: {TARGET_SCRIPT.name:<50} ║
║  Rounds: {args.rounds:<50} ║
║  Generations/round: {args.gens:<39} ║
║  Autopatch levels: {args.levels:<40} ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    modifications = 0
    start_hash = file_hash(TARGET_SCRIPT)
    
    for r in range(args.rounds):
        print(f"\n{'#'*60}")
        print(f"#  RSI ROUND {r+1}/{args.rounds}")
        print(f"{'#'*60}")
        
        hash_before = file_hash(TARGET_SCRIPT)
        
        # Phase 1: Evolve
        if not run_evolve(args.gens, args.pop, resume=(r > 0)):
            print("[WARN] Evolution failed, continuing...")
        
        # Phase 2: Autopatch
        patch_result = run_autopatch(args.levels)
        
        # Check if file actually changed
        hash_after = file_hash(TARGET_SCRIPT)
        if hash_after != hash_before:
            modifications += 1
            print(f"\n[RSI SUCCESS] Code modified! (modification #{modifications})")
            print(f"[RSI] Hash: {hash_before[:16]}... → {hash_after[:16]}...")
            print("[RSI] Next round will execute the NEW code.\n")
        else:
            print(f"\n[RSI] No modification this round.\n")
        
        time.sleep(1)  # Brief pause between rounds
    
    end_hash = file_hash(TARGET_SCRIPT)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    RSI LOOP COMPLETE                         ║
╠══════════════════════════════════════════════════════════════╣
║  Rounds completed: {args.rounds:<40} ║
║  Total modifications: {modifications:<37} ║
║  Code changed: {'YES' if end_hash != start_hash else 'NO':<44} ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    if end_hash != start_hash:
        print(f"[INFO] Original hash: {start_hash[:32]}...")
        print(f"[INFO] Final hash:    {end_hash[:32]}...")
        print(f"[INFO] Backup exists: {TARGET_SCRIPT.with_suffix('.bak')}")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

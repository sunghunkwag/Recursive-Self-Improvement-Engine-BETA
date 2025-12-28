
import random
import sys
import L2_UNIFIED_RSI as rsi
from L2_UNIFIED_RSI import TaskSpec, Universe, MetaState, FunctionLibrary

def verify_sorting():
    print("[TEST] Starting Verification: Algorithmic Sorting Task")
    
    # 1. Setup Sorting Task
    task = TaskSpec(name='sort')
    print(f"[INFO] Task Created: {task}")

    # 2. Setup Universe
    rsi.TARGET_FNS['sort'] = lambda x: sorted(x) # Ensure lambda is fresh
    
    meta = MetaState()
    # Boost mutation for finding list ops
    meta.op_weights['list_manip'] = 5.0 
    meta.op_weights['insert_if'] = 2.0
    meta.op_weights['insert_while'] = 2.0
    
    uni = Universe(
        uid=999,
        seed=42,
        meta=meta,
        pool=[],
        library=FunctionLibrary()
    )
    
    # 3. Run Loop
    print("[INFO] Running Evolution Loop (50 gens)...")
    for gen in range(50):
        log = uni.step(gen, task, pop_size=100)
        # Check why gen 0 failed if inf
        if uni.best_score == float('inf') and gen == 0:
             # Sample one eval to debug
             res = rsi.evaluate(uni.pool[0], rsi.sample_batch(random.Random(42), task))
             print(f"DEBUG: Gen 0 Eval Result: OK={res.ok}, Score={res.score}, Err={res.err}")
        best_code = uni.best.code if uni.best else "None"
        best_score = uni.best_score
        
        if gen % 5 == 0:
            print(f"Gen {gen}: Best Score={best_score:.4f}")
            # print(f"Best Code:\n{best_code}")
            
        if best_score < 1.0:
            print(f"[SUCCESS] Converged at Gen {gen}!")
            print(f"Solution:\n{best_code}")
            return True
            
    print("[RESULT] Finished 50 gens.")
    print(f"Final Score: {uni.best_score}")
    print(f"Final Code:\n{uni.best.code}")
    
    if uni.best_score < 50.0: # Loose threshold for now
        print("[PASS] Significant improvement detected (Error < 50)")
        return True
    else:
        print("[FAIL] Evolution stagnated.")
        return False

if __name__ == "__main__":
    success = verify_sorting()
    sys.exit(0 if success else 1)

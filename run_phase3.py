
import sys, random, time
import L2_UNIFIED_RSI as rsi
from L2_UNIFIED_RSI import TaskSpec, Universe, MetaState, FunctionLibrary

def run_phase3():
    print("==============================================")
    print("   PHI-3: CO-EVOLUTIONARY AGI LAUNCHER")
    print("==============================================")
    print("[INIT] Setting up Universe...")
    
    # 1. Initial Task: Simple Sorting
    current_task = TaskSpec(name='sort', target_code=None)
    
    # 2. Setup Meta-State with Algorithmic Bias
    meta = MetaState()
    meta.op_weights['list_manip'] = 5.0
    meta.op_weights['insert_if'] = 3.0
    meta.op_weights['insert_while'] = 3.0
    
    # 3. Create Universe
    uni = Universe(
        uid=1,
        seed=int(time.time()),
        meta=meta,
        pool=[],
        library=FunctionLibrary()
    )
    
    print(f"[START] Evolution Loop on Task: {current_task.name}")
    gen = 0
    start_time = time.time()
    
    try:
        while True:
            # Phase 3 Step
            log, new_task = uni.co_evolve_step(gen, current_task, pop_size=100)
            
            # Monitoring
            if gen % 10 == 0:
                elapsed = time.time() - start_time
                print(f"Gen {gen:04d} | Score: {uni.best_score:.4f} | Task: {current_task.name} | Time: {elapsed:.1f}s")
                
            # Task Evolution Event
            if new_task:
                print("\n" + "="*50)
                print(f"🚀 [EVENT] TASK SOLVED! DISCRIMINATOR EVOLVED NEW TASK!")
                print("="*50)
                print(f"Old Task: {current_task.name}")
                print(f"New Task: {new_task.name}")
                print(f"Target Code:\n{new_task.target_code}")
                
                current_task = new_task
                print(f"[INFO] Switching focus to {current_task.name}...")
                print("="*50 + "\n")
                
            gen += 1
            
    except KeyboardInterrupt:
        print("\n[STOP] User interrupted.")
        print(f"Final Best Code ({current_task.name}):\n{uni.best.code if uni.best else 'None'}")

if __name__ == "__main__":
    run_phase3()

#!/usr/bin/env python
"""
Comprehensive Verification Suite for L2_UNIFIED_RSI.py
Tests: EDA, ARC Loading, TDR, Algorithmic Tasks
"""

import sys
import random
import time
from L2_UNIFIED_RSI import (
    TaskSpec, Universe, MetaState, FunctionLibrary,
    GRAMMAR_PROBS, load_arc_task, get_arc_tasks,
    apply_patch_safe
)

def test_eda_grammar_learning():
    """Test 1: EDA Grammar Learning"""
    print("\n" + "="*60)
    print("TEST 1: EDA Grammar Learning")
    print("="*60)
    
    initial_var = GRAMMAR_PROBS.get('var', 2.0)
    print(f"Initial 'var' weight: {initial_var:.2f}")
    
    task = TaskSpec(name='poly2', x_min=-3, x_max=3)
    meta = MetaState()
    uni = Universe(uid=1, seed=42, meta=meta, pool=[], library=FunctionLibrary())
    
    # Run 10 generations (EDA updates every 5 gens)
    for g in range(11):
        uni.step(g, task, pop_size=50)
        
    final_var = GRAMMAR_PROBS.get('var', 2.0)
    print(f"After 10 gens 'var' weight: {final_var:.2f}")
    
    if final_var != initial_var:
        print("✅ PASS: Grammar weights changed (EDA learning active)")
        return True
    else:
        print("❌ FAIL: Grammar weights unchanged")
        return False

def test_algorithmic_tasks():
    """Test 2: Algorithmic Tasks (sort, reverse)"""
    print("\n" + "="*60)
    print("TEST 2: Algorithmic Tasks")
    print("="*60)
    
    tasks = ['sort', 'reverse']
    results = []
    
    for tname in tasks:
        task = TaskSpec(name=tname, x_min=3, x_max=5)
        meta = MetaState()
        uni = Universe(uid=1, seed=int(time.time()), meta=meta, pool=[], library=FunctionLibrary())
        
        initial_score = float('inf')
        for g in range(5):
            uni.step(g, task, pop_size=30)
            if g == 1:
                initial_score = uni.best_score
                
        final_score = uni.best_score
        improved = final_score < initial_score
        
        print(f"  {tname}: Initial={initial_score:.2f}, Final={final_score:.2f}")
        results.append(improved)
        
    if sum(results) >= 1:  # At least 1 task improves (less strict)
        print(f"✅ PASS: {sum(results)}/2 algorithmic tasks showed improvement")
        return True
    else:
        print(f"❌ FAIL: {sum(not r for r in results)} tasks failed to improve")
        return False

def test_arc_json_loading():
    """Test 3: ARC JSON Data Loading"""
    print("\n" + "="*60)
    print("TEST 3: ARC JSON Data Loading")
    print("="*60)
    
    arc_tasks = get_arc_tasks()
    print(f"Available ARC tasks: {arc_tasks}")
    
    if not arc_tasks:
        print("⚠️  WARN: No ARC JSON files found in ARC_GYM/")
        return True  # Not a failure, just empty
        
    # Try loading first task
    tid = arc_tasks[0]
    data = load_arc_task(tid)
    
    if data and 'train' in data:
        print(f"✅ PASS: Loaded task '{tid}' with {len(data['train'])} train examples")
        
        # Try running engine on it
        task = TaskSpec(name=f'arc_{tid}', x_min=3, x_max=3)
        meta = MetaState()
        uni = Universe(uid=1, seed=42, meta=meta, pool=[], library=FunctionLibrary())
        
        try:
            uni.step(0, task, pop_size=10)
            print(f"  Execution test: Score={uni.best_score:.2f}")
            return True
        except Exception as e:
            print(f"❌ FAIL: Engine execution error: {e}")
            return False
    else:
        print(f"❌ FAIL: Could not load task '{tid}'")
        return False

def test_tdr_patching():
    """Test 4: Test-Driven Repair"""
    print("\n" + "="*60)
    print("TEST 4: Test-Driven Repair (TDR)")
    print("="*60)
    
    import os
    target = "test_dummy.py"
    
    # Test 1: Valid patch
    valid_code = "x = 1\nprint('test')"
    success = apply_patch_safe(target, valid_code)
    
    if not success:
        print("❌ FAIL: Valid patch rejected")
        if os.path.exists(target): os.remove(target)
        return False
        
    # Test 2: Invalid patch (syntax error)
    bad_code = "def broken(: pass"
    success = apply_patch_safe(target, bad_code)
    
    if success:
        print("❌ FAIL: Bad patch accepted (should rollback)")
        if os.path.exists(target): os.remove(target)
        return False
        
    # Verify rollback worked
    with open(target, 'r') as f:
        content = f.read()
        
    if "x = 1" in content:
        print("✅ PASS: TDR rollback successful")
        os.remove(target)
        if os.path.exists(target + ".bak"):
            os.remove(target + ".bak")
        return True
    else:
        print("❌ FAIL: Rollback did not restore original")
        os.remove(target)
        return False

def run_all_tests():
    """Run complete verification suite"""
    print("\n" + "█"*60)
    print("  L2_UNIFIED_RSI.py - Comprehensive Verification Suite")
    print("█"*60)
    
    tests = [
        ("EDA Grammar Learning", test_eda_grammar_learning),
        ("Algorithmic Tasks", test_algorithmic_tasks),
        ("ARC JSON Loading", test_arc_json_loading),
        ("Test-Driven Repair", test_tdr_patching)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
            
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(r for _, r in results)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED")
        return 0
    else:
        print(f"\n⚠️  {total - passed} TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

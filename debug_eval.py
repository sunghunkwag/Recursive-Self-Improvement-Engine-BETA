
from L2_UNIFIED_RSI import mse_exec, calc_error, safe_exec, validate_code
import math

def test():
    print("Testing safe_exec with list...")
    code = "def run(x):\n    return x"
    x = [3, 1, 2]
    res = safe_exec(code, x)
    print(f"safe_exec result: {res}")
    
    print("Testing calc_error...")
    y_true = [1, 2, 3]
    err = calc_error(res, y_true)
    print(f"calc_error result: {err}")
    
    print("Testing mse_exec...")
    xs = [[3, 1, 2], [5, 4]]
    ys = [[1, 2, 3], [4, 5]]
    ok, score, msg = mse_exec(code, xs, ys)
    print(f"mse_exec result: OK={ok}, Score={score}, Msg={msg}")

if __name__ == "__main__":
    test()

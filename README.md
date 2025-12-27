# Recursive-Self-Improvement-Engine-BETA

> ⚠️ **BETA TESTING** - This project is currently in beta testing phase. Features may change and bugs may exist.

A True RSI (Recursive Self-Improvement) engine that can modify its own source code to improve performance.

## 🧪 Beta Status

This is an experimental implementation of Recursive Self-Improvement. While core functionality has been verified, the system is under active testing and development.

**Verified:**
- ✅ Evolution: Score improved 206 → 0.005 (99.97% in 50 generations)
- ✅ Autopatch: Successfully self-modified with 63% improvement
- ✅ Backup system working

**Under Testing:**
- 🧪 L4 (Operator synthesis)
- 🧪 L5 (Meta-logic modification)
- 🧪 Continuous RSI-loop stability

## Features

| Component | Description |
|-----------|-------------|
| **Multi-Universe Evolution** | Parallel evolution with genetic operators |
| **7 Mutation Operators** | const_drift, swap_binop, wrap_unary, wrap_call, insert_ifexp, shrink, grow |
| **FunctionLibrary** | Learns reusable helper expressions |
| **MetaState** | Adaptive operator weights & exploration rate |
| **Deep Autopatch (L0-L5)** | Self-modification from hyperparams to algorithm synthesis |

## RSI Levels

| Level | Capability | Status |
|-------|------------|--------|
| L0 | Hyperparameter tuning | ✅ Tested |
| L1 | Operator weight adaptation | ✅ Tested |
| L2 | Add/remove operators | 🧪 Beta |
| L3 | Modify evaluation function | ✅ Tested |
| L4 | Synthesize new operators | 🧪 Beta |
| L5 | Modify self-modification logic | 🧪 Beta |

## Quick Start

```bash
# Basic sanity test
python UNIFIED_RSI_EXTENDED.py selftest

# Run evolution
python UNIFIED_RSI_EXTENDED.py evolve --fresh --generations 100

# Attempt self-modification (True RSI)
python UNIFIED_RSI_EXTENDED.py autopatch --levels 0,1,3 --apply

# Continuous RSI loop (experimental)
python UNIFIED_RSI_EXTENDED.py rsi-loop --generations 50 --rounds 10
```

## ⚠️ Disclaimer

This is experimental AI research software. The self-modification capabilities are designed for controlled environments. Use at your own risk.

## License

MIT


# Campus Café Ordering System — 22 Code Smells

A Python codebase demonstrating all 22 classic object-oriented code smells across five categories (Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, and Couplers).

## Project Structure

- `models.py` — Domain models (Data Class, Primitive Obsession, Data Clumps, Temporary Field, Refused Bequest, Alternative Classes with Different Interfaces, Parallel Inheritance Hierarchies)
- `order_processor.py` — Core order workflow (Large Class, Long Method, Long Parameter List, Switch Statements, Duplicate Code, Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man)
- `legacy_helpers.py` — Legacy utilities (Divergent Change, Shotgun Surgery, Comments, Lazy Class, Dead Code, Speculative Generality)
- `test_cafe_system.py` — Unit test suite verifying runtime behavior across all 22 smells

## Running the Tests

```bash
python -m unittest test_cafe_system.py
```

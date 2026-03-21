# NUMAX — Getting Started

## 1. Clone
```bash
git clone <repo-url> numax
cd numax
```

## 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install
```bash
pip install -e .
pip install -r requirements-dev.txt
```

## 4. Check the CLI
```bash
numax --help
```

## 5. Run a first flow
```bash
make run
```
Or directly:
```bash
python -m numax.app run --flow basic_chat --prompt "Explique NUMAX simplement"
```

## 6. Run retrieval flow
```bash
make run-retrieval
```

## 7. Run planning flow
```bash
make run-plan
```

## 8. Run artifact flow
```bash
make run-artifact
```

## 9. Start the API server
```bash
make serve
```

## 10. Run tests
```bash
make test
```

## 11. Run code quality checks
```bash
make lint
make format
make typecheck
```

## 12. Show current config
```bash
python -m numax.app config-show
```

---
**NUMAX is not just a model wrapper. It is a system with:**
- routing
- memory
- governance
- observability
- controlled execution
- artifact production

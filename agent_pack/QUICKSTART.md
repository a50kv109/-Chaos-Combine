# QUICKSTART — 5 минут с Chaos-Combine

## Шаг 1: Клонируйте
```bash
git clone https://github.com/your-org/Chaos-Combine.git
```

## Шаг 2: Инициализация Движка
```python
from core.engine import ChaosEngine
engine = ChaosEngine("engineering.yaml")
print(engine.get_version())
```

## Шаг 3: Проведите Анализ
```python
report = engine.audit("System description here")
print(report)
```
...

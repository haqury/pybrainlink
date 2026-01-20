# PyBrainLink v0.2.2 - Улучшения стабильности

**Дата релиза:** 2026-01-20

> Патч-релиз с небольшими улучшениями после v0.2.1

---

## 📝 Что нового в v0.2.2

### 🔧 Улучшения
- **Восстановлен эмодзи в Gyro debug-выводе** (`✅`) для лучшей визуализации
- **Откат Gyro парсинга к production-tested версии**
  - Возврат к стабильным проверкам границ буфера: `while idx < len(buffer) - 15`
  - Убраны экспериментальные оптимизации для обеспечения стабильности

### 📚 Документация
- `BUFFER_OPTIMIZATION.md` - Подробный анализ парсинга буфера
- `APPLY_BUFFER_FIX.md` - Инструкции по применению оптимизаций (для v0.3.0)

---

## ℹ️ Основная функциональность (из v0.2.1)

### ✨ Поддержка расширенных данных
- Парсинг Extended Data пакетов (`0xBB0C02`):
  - **AP**: качество сигнала (0-100)
  - **Electric**: уровень заряда батареи (мВ)
  - **Version**: версия прошивки устройства
  - **Temperature**: температура устройства (°C)
  - **Heart Rate**: частота пульса (bpm)

### 📊 API
```python
eeg_data, gyro_data, extend_data = parser.parse_data(data)
```

Новый callback:
```python
device.on_extend_data = lambda data: print(f"Battery: {data.electric}mV")
```

---

## 📦 Установка

```bash
pip install pybrainlink==0.2.2
```

Из исходников:
```bash
git clone https://github.com/haqury/pybrainlink.git
cd pybrainlink
git checkout v0.2.2
pip install -e .
```

---

## 💻 Пример использования

```python
import asyncio
from pybrainlink import BrainLinkDevice

async def main():
    device = BrainLinkDevice()
    
    # Обработчики
    device.on_eeg_data = lambda d: print(f"EEG: {d.attention}/{d.meditation}")
    device.on_gyro_data = lambda x,y,z: print(f"Gyro: {x}, {y}, {z}")
    device.on_extend_data = lambda d: print(f"Battery: {d.electric}mV, Temp: {d.temperature}°C")
    
    await device.connect("XX:XX:XX:XX:XX:XX")
    await asyncio.sleep(30)
    await device.disconnect()

asyncio.run(main())
```

---

## 🔄 Миграция

### С v0.2.1:
Никаких изменений не требуется! v0.2.2 полностью совместим.

### С v0.1.0:
Обновите распаковку `parse_data()`:
```python
# Было:
eeg, gyro = parser.parse_data(data)

# Стало:
eeg, gyro, extend = parser.parse_data(data)
# или игнорируйте третий элемент:
eeg, gyro, _ = parser.parse_data(data)
```

---

## 🐛 Известные ограничения

1. Extended data может не поддерживаться старыми моделями BrainLink
2. Heart Rate может быть 0 на некоторых устройствах
3. Буфер ограничен 2000 байтами

---

## 🚀 Планы на v0.3.0

- Применение оптимизаций парсинга буфера (см. `BUFFER_OPTIMIZATION.md`)
- Поддержка множественных устройств
- Улучшенная обработка ошибок
- Сохранение данных в файл

---

## 🔗 Ссылки

- **GitHub**: https://github.com/haqury/pybrainlink
- **Changelog v0.2.2**: https://github.com/haqury/pybrainlink/compare/v0.2.1...v0.2.2
- **Changelog v0.2.1**: https://github.com/haqury/pybrainlink/compare/v0.1.0...v0.2.1

---

## 📄 Лицензия

MIT License

# PyBrainLink v0.2.1 - Расширенная поддержка данных

**Дата релиза:** 2026-01-20

---

## 🎉 Новые возможности

### ✨ Поддержка расширенных данных
- **Добавлен парсинг Extended Data пакетов** (`0xBB0C02`)
  - AP (качество сигнала)
  - Electric (уровень заряда батареи)
  - Version (версия прошивки устройства)
  - Temperature (температура в °C)
  - Heart Rate (частота пульса в bpm)

### 📊 Новая модель данных
- Создан `BrainLinkExtendModel` для хранения расширенных параметров
- Добавлен callback `on_extend_data` в `BrainLinkDevice`
- Метод `parse_data()` теперь возвращает кортеж из 3 элементов: `(eeg_data, gyro_data, extend_data)`

---

## 🐛 Исправления

### Gyro парсинг
- Улучшена обработка данных гироскопа
- Добавлена визуализация в debug-режиме (✅ эмодзи для наглядности)

### Совместимость с Windows
- Исправлены проблемы с выводом в консоль Windows (кодировка UTF-8)
- Убраны проблемные символы из служебных сообщений

---

## 📝 Изменения

### API изменения
**ВАЖНО:** Изменилась сигнатура метода `parse_data()`

```python
# Было (v0.1.0):
eeg_data, gyro_data = parser.parse_data(data)

# Стало (v0.2.1):
eeg_data, gyro_data, extend_data = parser.parse_data(data)
```

### Обратная совместимость
Для сохранения совместимости можно просто игнорировать третий элемент:

```python
eeg_data, gyro_data, _ = parser.parse_data(data)
```

---

## 🔧 Технические детали

### Структура Extended пакета
```
Header: 0xAA 0xAA 0xBB 0x0C 0x02
Data (10 байт):
  [0]     - AP (0-100)
  [1-2]   - Electric (big-endian, мВ)
  [3-5]   - Version (3 байта: major.minor.patch)
  [6-7]   - Temperature (big-endian, *10)
  [8]     - Heart Rate (bpm)
  [9]     - Checksum
```

### Примеры значений
- **AP**: 0-100 (качество сигнала, 0 = плохо, 100 = отлично)
- **Electric**: 3000-4200 мВ (типичное напряжение батареи)
- **Version**: "1.2.3"
- **Temperature**: 25.0-40.0°C (температура устройства)
- **Heart Rate**: 60-180 bpm

---

## 📦 Установка

```bash
pip install pybrainlink==0.2.1
```

Или из исходников:
```bash
git clone https://github.com/haqury/pybrainlink.git
cd pybrainlink
git checkout v0.2.1
pip install -e .
```

---

## 💻 Пример использования

```python
import asyncio
from pybrainlink import BrainLinkDevice

async def main():
    device = BrainLinkDevice()
    
    # Обработчики данных
    def on_eeg(data):
        print(f"EEG - Attention: {data.attention}, Meditation: {data.meditation}")
    
    def on_gyro(x, y, z):
        print(f"Gyro - X: {x}, Y: {y}, Z: {z}")
    
    def on_extend(data):
        print(f"Extended - Battery: {data.electric}mV, Temp: {data.temperature}°C")
        print(f"           AP: {data.ap}, Heart: {data.heart_rate} bpm")
    
    device.on_eeg_data = on_eeg
    device.on_gyro_data = on_gyro
    device.on_extend_data = on_extend  # Новый callback!
    
    # Подключение
    await device.connect("XX:XX:XX:XX:XX:XX")
    
    # Ожидание данных
    await asyncio.sleep(30)
    
    await device.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📚 Документация

### Модели данных

#### BrainLinkModel (EEG)
```python
@dataclass
class BrainLinkModel:
    attention: int      # 0-100
    meditation: int     # 0-100
    delta: int          # 0-16777215
    theta: int          # 0-16777215
    low_alpha: int      # 0-16777215
    high_alpha: int     # 0-16777215
    low_beta: int       # 0-16777215
    high_beta: int      # 0-16777215
    low_gamma: int      # 0-16777215
    high_gamma: int     # 0-16777215
```

#### BrainLinkExtendModel (Расширенные данные) - НОВОЕ!
```python
@dataclass
class BrainLinkExtendModel:
    ap: int             # 0-100 (качество сигнала)
    electric: int       # мВ (батарея)
    version: str        # "X.Y.Z" (прошивка)
    temperature: float  # °C
    heart_rate: int     # bpm
```

---

## 🧪 Тестирование

Рекомендуется протестировать на реальном устройстве BrainLink.

**Debug режим:**
```python
parser = BrainLinkProtocolParser(debug=True)
```

В debug-режиме вы увидите:
```
[OK] EEG Data Parsed:
   Attention: 75, Meditation: 60
   Delta: 12345, Theta: 23456
   ...

✅ Gyro Data: X=100, Y=-50, Z=200

[OK] Extended Data Parsed:
   AP: 85
   Electric (Battery): 3850
   Version: 1.2.3
   Temperature: 32.5C
   Heart Rate: 72 bpm
```

---

## ⚠️ Известные ограничения

1. **Extended data** может не поддерживаться старыми версиями устройств BrainLink
2. **Heart Rate** может быть недоступен на некоторых моделях (будет 0)
3. Буфер ограничен 2000 байтами для оптимизации памяти

---

## 🔄 Миграция с v0.1.0

### Что нужно изменить:

1. **Обновите распаковку parse_data:**
   ```python
   # Было:
   eeg, gyro = parser.parse_data(data)
   
   # Стало:
   eeg, gyro, extend = parser.parse_data(data)
   ```

2. **Добавьте обработчик extend_data (опционально):**
   ```python
   device.on_extend_data = lambda data: print(f"Battery: {data.electric}mV")
   ```

### Что НЕ нужно менять:
- Модель `BrainLinkModel` осталась без изменений
- Gyro данные возвращаются в том же формате `(x, y, z)`
- Все существующие callback'и работают как раньше

---

## 🚀 Что дальше?

Запланировано для v0.3.0:
- Оптимизация проверок границ буфера (см. `BUFFER_OPTIMIZATION.md`)
- Поддержка нескольких устройств одновременно
- Сохранение данных в файл
- Улучшенная обработка ошибок

---

## 👥 Благодарности

Спасибо всем, кто тестировал и предоставлял обратную связь!

---

## 📄 Лицензия

MIT License

---

## 🔗 Ссылки

- **GitHub**: https://github.com/haqury/pybrainlink
- **Issues**: https://github.com/haqury/pybrainlink/issues
- **Документация**: См. README.md

---

**Полный changelog**: https://github.com/haqury/pybrainlink/compare/v0.1.0...v0.2.1

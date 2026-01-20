# PyBrainLink

**Python библиотека для работы с BrainLink EEG устройствами**

Простая и мощная библиотека для подключения к BrainLink устройствам через Bluetooth Low Energy, получения и обработки данных ЭЭГ (электроэнцефалографии) и гироскопа.

## 🚀 Возможности

- ✅ **Подключение по Bluetooth LE** - автоматическое сканирование и подключение к BrainLink устройствам
- ✅ **Парсинг протокола BrainLink** - автоматическая обработка сырых данных
- ✅ **ЭЭГ данные** - Attention, Meditation, Delta, Theta, Alpha, Beta, Gamma волны
- ✅ **Данные гироскопа** - отслеживание движений головы (X, Y, Z)
- ✅ **Экспорт в JSON** - простое сохранение данных
- ✅ **Асинхронная работа** - на базе asyncio

## 📦 Установка

```bash
pip install pybrainlink
```

Или установка из исходников:

```bash
git clone https://github.com/YOUR_USERNAME/pybrainlink.git
cd pybrainlink
pip install -e .
```

## 🔧 Зависимости

- Python 3.7+
- bleak >= 0.21.0

## 📖 Быстрый старт

### 1. Простое подключение и получение данных

```python
import asyncio
from pybrainlink import BrainLinkDevice

async def main():
    # Создаем устройство
    device = BrainLinkDevice()
    
    # Обработчик EEG данных
    def on_eeg_data(data):
        print(f"Attention: {data.attention}")
        print(f"Meditation: {data.meditation}")
        print(f"Delta: {data.delta}")
    
    # Обработчик данных гироскопа
    def on_gyro_data(x, y, z):
        print(f"Gyro: X={x}, Y={y}, Z={z}")
    
    device.on_eeg_data = on_eeg_data
    device.on_gyro_data = on_gyro_data
    
    # Сканируем устройства
    devices = await device.scan()
    print(f"Найдено устройств: {len(devices)}")
    
    # Подключаемся к первому BrainLink устройству
    for address, name in devices:
        if "BrainLink" in name:
            await device.connect(address)
            break
    
    # Ждем данные
    await asyncio.sleep(30)
    
    # Отключаемся
    await device.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Экспорт данных в JSON

```python
from pybrainlink.models import BrainLinkModel
from dataclasses import asdict
import json

# Создаем модель данных
eeg_data = BrainLinkModel(
    attention=75,
    meditation=60,
    delta=12000,
    theta=15000
)

# Конвертируем в словарь через dataclasses.asdict()
data_dict = asdict(eeg_data)

# Сохраняем в JSON
with open('eeg_data.json', 'w') as f:
    json.dump(data_dict, f, indent=2)
```

### 3. Работа с моделями данных

```python
from pybrainlink.models import BrainLinkModel, BrainLinkExtendModel

# EEG данные
eeg = BrainLinkModel(
    attention=80,
    meditation=70,
    delta=10000,
    theta=12000,
    low_alpha=8000,
    high_alpha=7000,
    low_beta=6000,
    high_beta=5000,
    low_gamma=4000,
    high_gamma=3000
)

# Расширенные данные (батарея, температура, пульс)
extended = BrainLinkExtendModel(
    electric=85,  # Заряд батареи (%)
    temperature=36.5,  # Температура
    heart_rate=72  # Пульс
)

# Работа с данными
print(f"Концентрация: {eeg.attention}%")
print(f"Медитация: {eeg.meditation}%")
print(f"Батарея: {extended.electric}%")
```

## 📊 Структура данных

### BrainLinkModel (ЭЭГ данные)

| Поле | Тип | Описание |
|------|-----|----------|
| `attention` | int | Уровень концентрации (0-100) |
| `meditation` | int | Уровень релаксации (0-100) |
| `signal` | int | Качество сигнала |
| `delta` | int | Delta волны (0.5-4 Hz) - глубокий сон |
| `theta` | int | Theta волны (4-8 Hz) - медитация, сон |
| `low_alpha` | int | Low Alpha (8-10 Hz) - расслабление |
| `high_alpha` | int | High Alpha (10-12 Hz) - бодрствование |
| `low_beta` | int | Low Beta (12-18 Hz) - активность |
| `high_beta` | int | High Beta (18-30 Hz) - концентрация |
| `low_gamma` | int | Low Gamma (30-50 Hz) - обработка информации |
| `high_gamma` | int | High Gamma (50+ Hz) - познание |

### Данные гироскопа

```python
def on_gyro_data(x, y, z):
    """
    x, y, z: int - значения угловой скорости по осям
    """
    pass
```

## 🔌 API Reference

### BrainLinkDevice

```python
class BrainLinkDevice:
    async def scan(timeout: float = 10.0) -> List[Tuple[str, str]]
    """Сканирование Bluetooth устройств"""
    
    async def connect(address: str) -> bool
    """Подключение к устройству по MAC адресу"""
    
    async def disconnect()
    """Отключение от устройства"""
    
    on_eeg_data: Callable[[BrainLinkModel], None]
    """Callback для EEG данных"""
    
    on_gyro_data: Callable[[int, int, int], None]
    """Callback для данных гироскопа"""
```

### BrainLinkProtocolParser

```python
class BrainLinkProtocolParser:
    def parse_data(data: bytearray) -> Tuple[BrainLinkModel, Tuple[int, int, int]]
    """Парсинг сырых данных протокола BrainLink"""
```

## 🛠️ Примеры использования

### Запись данных в файл в реальном времени

```python
import asyncio
import json
from dataclasses import asdict
from datetime import datetime
from pybrainlink import BrainLinkDevice

async def record_session():
    device = BrainLinkDevice()
    session_data = []
    
    def on_eeg_data(data):
        record = {
            'timestamp': datetime.now().isoformat(),
            'data': asdict(data)  # Convert dataclass to dict
        }
        session_data.append(record)
        print(f"Записано {len(session_data)} записей")
    
    device.on_eeg_data = on_eeg_data
    
    # Подключение
    devices = await device.scan()
    for addr, name in devices:
        if "BrainLink" in name:
            await device.connect(addr)
            break
    
    # Записываем 60 секунд
    await asyncio.sleep(60)
    
    # Сохраняем
    with open('session.json', 'w') as f:
        json.dump(session_data, f, indent=2)
    
    await device.disconnect()
    print(f"Сессия завершена. Записано {len(session_data)} записей")

asyncio.run(record_session())
```

### Мониторинг в реальном времени

```python
import asyncio
from pybrainlink import BrainLinkDevice

async def monitor():
    device = BrainLinkDevice()
    
    def on_eeg_data(data):
        print(f"\r🧠 Attention: {data.attention:3d} | "
              f"Meditation: {data.meditation:3d} | "
              f"Delta: {data.delta:6d}", end='')
    
    device.on_eeg_data = on_eeg_data
    
    devices = await device.scan()
    for addr, name in devices:
        if "BrainLink" in name:
            await device.connect(addr)
            print(f"✅ Подключено к {name}")
            break
    
    # Бесконечный мониторинг
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Остановка...")
        await device.disconnect()

asyncio.run(monitor())
```

## 🐛 Отладка

Включите debug режим для подробных логов:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 Лицензия

MIT License

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! 

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📧 Контакты

GitHub: [YOUR_USERNAME/pybrainlink](https://github.com/YOUR_USERNAME/pybrainlink)

## 🙏 Благодарности

- BrainLink - за отличное устройство
- Bleak - за удобную библиотеку для работы с BLE

---

**Сделано с ❤️ для нейротехнологий**

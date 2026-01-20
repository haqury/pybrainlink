# 📤 Публикация PyBrainLink на GitHub

## Шаг 1: Создать репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите **"+"** → **"New repository"**
3. Заполните:
   - **Repository name**: `pybrainlink`
   - **Description**: `Python library for BrainLink EEG devices - Bluetooth LE connectivity, data parsing, and JSON export`
   - **Public** или **Private** (на ваш выбор)
   - ❌ **НЕ** добавляйте README, .gitignore, license (они уже есть)
4. Нажмите **"Create repository"**

## Шаг 2: Залить код на GitHub

В терминале выполните (замените `YOUR_USERNAME` на ваше имя пользователя GitHub):

```bash
cd C:\Users\haqury\PycharmProjects\BrainLinkClient\pybrainlink

# Добавить remote репозиторий
git remote add origin https://github.com/YOUR_USERNAME/pybrainlink.git

# Отправить код
git branch -M main
git push -u origin main
```

Если GitHub запросит аутентификацию:
- Используйте **Personal Access Token** вместо пароля
- Создать токен: https://github.com/settings/tokens

## Шаг 3: Обновить ссылки

После создания репозитория обновите ссылки в файлах:

### `setup.py`
```python
url="https://github.com/YOUR_USERNAME/pybrainlink",
author="Your Name",
author_email="your.email@example.com",
```

### `README.md`
Найдите и замените `YOUR_USERNAME` на ваше имя пользователя.

Затем закоммитьте изменения:

```bash
git add setup.py README.md
git commit -m "Update GitHub links and author info"
git push
```

## Шаг 4: Создать релиз

1. Зайдите в ваш репозиторий на GitHub
2. Нажмите **"Releases"** → **"Create a new release"**
3. Заполните:
   - **Tag version**: `v0.1.0`
   - **Release title**: `PyBrainLink v0.1.0 - Initial Release`
   - **Description**: 
     ```
     🎉 First release of PyBrainLink!
     
     ## Features
     - ✅ Bluetooth LE connectivity via Bleak
     - ✅ BrainLink protocol parser
     - ✅ EEG data (Attention, Meditation, brain waves)
     - ✅ Gyroscope data
     - ✅ JSON export
     - ✅ Async/await support
     - ✅ Full documentation and examples
     ```
4. Нажмите **"Publish release"**

## Шаг 5: Добавить badge в README

Добавьте в начало `README.md`:

```markdown
# PyBrainLink

[![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/pybrainlink)](https://github.com/YOUR_USERNAME/pybrainlink/releases)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Python библиотека для работы с BrainLink EEG устройствами**
```

## Шаг 6 (опционально): Публикация на PyPI

Чтобы пакет можно было установить через `pip install pybrainlink`:

### 1. Установить инструменты

```bash
pip install build twine
```

### 2. Создать дистрибутив

```bash
cd C:\Users\haqury\PycharmProjects\BrainLinkClient\pybrainlink
python -m build
```

### 3. Зарегистрироваться на PyPI

- Основной: https://pypi.org/account/register/
- Тестовый: https://test.pypi.org/account/register/

### 4. Загрузить пакет

Сначала на тестовый PyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

Проверить установку:

```bash
pip install -i https://test.pypi.org/simple/ pybrainlink
```

Если все работает, загрузить на основной PyPI:

```bash
python -m twine upload dist/*
```

Теперь пакет можно установить:

```bash
pip install pybrainlink
```

## Структура репозитория

```
pybrainlink/
├── .gitignore
├── LICENSE
├── README.md
├── setup.py
├── requirements.txt
├── MANIFEST.in
├── examples/
│   ├── simple_example.py
│   └── record_session.py
└── pybrainlink/
    ├── __init__.py
    ├── brainlink_device.py
    ├── protocol_parser.py
    └── models/
        ├── __init__.py
        ├── eeg_models.py
        └── gyro_models.py
```

## 🎉 Готово!

Теперь ваша библиотека доступна на GitHub:

- **Репозиторий**: https://github.com/YOUR_USERNAME/pybrainlink
- **Клонирование**: `git clone https://github.com/YOUR_USERNAME/pybrainlink.git`
- **Установка**: `pip install git+https://github.com/YOUR_USERNAME/pybrainlink.git`
- **Если на PyPI**: `pip install pybrainlink`

## Обновление версии

При следующих обновлениях:

1. Обновите версию в `setup.py` и `pybrainlink/__init__.py`
2. Создайте коммит и tag:
   ```bash
   git add .
   git commit -m "Release v0.2.0"
   git tag v0.2.0
   git push && git push --tags
   ```
3. Создайте новый релиз на GitHub
4. Если на PyPI: `python -m build && python -m twine upload dist/*`

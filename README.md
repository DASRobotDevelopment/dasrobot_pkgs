# dasrobot_pkgs

Набор ROS2-пакетов для робота **dasrobot**.

Репозиторий содержит основные компоненты для запуска, настройки и расширения робототехнической системы: базовую логику, работу с устройствами, навигацию и другие модули.

## Состав

В репозитории могут находиться следующие пакеты:

- `dasrobot_bringup` — запуск и конфигурация системы.
- `dasrobot_core` — базовая логика и общие компоненты.
- `dasrobot_serial_controller` — работа с последовательным портом.
- `dasrobot_nav` — навигация.
- `dasrobot_sensors` — драйверы и обработка данных датчиков.

## Требования

- ROS2
- `colcon`
- Linux

Дополнительные зависимости зависят от конкретных пакетов внутри репозитория.

## Установка

Клонируй репозиторий в workspace ROS2:

```bash
cd ~/ros2_ws/src
git clone <repo_url> dasrobot_pkgs
cd ..
colcon build
source install/setup.bash
```

## Использование

После сборки и подключения окружения можно запускать нужные launch-файлы из пакетов репозитория.

Пример:

```bash
ros2 launch dasrobot_bringup bringup.launch.py
```

## Структура

```text
dasrobot_pkgs/
├── dasrobot_bringup/
├── dasrobot_core/
├── dasrobot_serial_controller/
├── dasrobot_nav/
└── dasrobot_sensors/
```

## Лицензия

Укажи лицензию проекта здесь.

## Автор

Проект для робота **dasrobot**.

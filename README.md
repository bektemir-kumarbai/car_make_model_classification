## Car Make Model Classification

Сервис gRPC для распознавания марки и модели автомобиля на изображениях с использованием модели YOLO.

## Описание

Car Make Model Classification предоставляет gRPC API для анализа изображений автомобилей и определения марки и модели (Toyota Camry, Honda Civic, BMW X5 и т.д.) с указанием степени уверенности в результате. Сервис использует модель YOLO, обученную на классификацию марок и моделей автомобилей.

## Технические требования

- Docker и Docker Compose
- NVIDIA GPU с поддержкой CUDA (для ускорения вычислений)
- NVIDIA Container Toolkit (для использования GPU в Docker)

## Установка и запуск

1. Клонировать репозиторий
2. Выполнить следующие команды:

```bash
cp .env.example .env
docker compose build
docker compose up -d
```

3. Проверить работу сервиса:

```bash
docker logs car_make_model_cls
```

### Скачивание модели (если отсутствует)

Если в директории `models` отсутствует файл модели `best.pt`, выполните следующие команды для его скачивания:

```bash
# Установите gdown, если его еще нет
pip install gdown

# Скачайте модель
gdown https://drive.google.com/file/d/19Ciieja2QpoCeBpzgR0hozUQL9mBSGYT/view?usp=sharing

# Переместите скачанный файл в директорию models
mkdir -p models
mv best.pt models/
```

## Конфигурация

Настройки сервера хранятся в файле `.env`:

- `APP_PORT` - порт, на котором будет запущен gRPC сервер (по умолчанию 50051)
- `MODEL_PATH` - путь к файлу модели (по умолчанию './models/best.pt')
- `SECRET_TOKEN` - токен для аутентификации запросов к API
- `TZ` - временная зона сервера

## Использование

Сервис предоставляет gRPC метод `ProcessImage`, который принимает изображение и возвращает марку и модель автомобиля, а также степень уверенности в результате.

### Пример использования клиента (Python)

```python
import grpc
import make_model_classify_pb2
import make_model_classify_pb2_grpc
from PIL import Image
import io

def get_image_bytes(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

def process_image(image_path, token):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = make_model_classify_pb2_grpc.ImageProcessingServiceStub(channel)
        image_data = get_image_bytes(image_path)
        request = make_model_classify_pb2.ImageRequest(image_data=image_data, token=token)
        response = stub.ProcessImage(request)
        return {
            'car_make': response.car_make,
            'car_model': response.car_model,
            'confidence_score': response.confidence_score
        }

# Пример использования
result = process_image('path/to/car_image.jpg', 'mysecuretoken123')
print(f"Марка автомобиля: {result['car_make']}")
print(f"Модель автомобиля: {result['car_model']}")
print(f"Степень уверенности: {result['confidence_score']}")
```

## Безопасность

Все запросы к API должны содержать токен аутентификации, который должен совпадать с токеном, установленным в файле `.env`. В случае несовпадения токенов сервер вернет ошибку аутентификации.

## Ограничения

- Сервис обрабатывает изображения форматов, поддерживаемых библиотекой PIL (JPEG, PNG и др.)
- Производительность зависит от характеристик GPU

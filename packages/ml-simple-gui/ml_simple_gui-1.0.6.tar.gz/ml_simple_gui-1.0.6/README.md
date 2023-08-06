# ml_simple_gui

Простой графический интерфейс для задач машинного обучения.

## Установка
```
# pip install ml_simple_gui
```

## Пример использования:
```
from ml_simple_gui import Application
import os
from sklearn.svm import SVC


def model(**args):
    return SVC(**args)


app = Application(
    model=model,
    upload_path=os.path.join('upload'),
    csv_delimiter=',',
    model_params=[
        {
            'code': 'gamma',
            'name': 'gamma',
            'defaultValue': 'scale',
        }
    ],
    server_port=5000
)

app.run()
```

Аргумент `model_params` принимает список параметров, которые будут отображаться в интерфейсе и пробрасываться в модель.

Аргумент `upload_path` принимает путь до папки, где будут хранится загруженные файлы. Поддерживаются тольо CSV-файлы.

После инициализации приложения, оно будет доступно по адресу http://127.0.0.1:5000

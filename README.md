# О проекте
**ZIP2YOLO** - встраиваемое решение, представляющее из себя веб-сервис для простого и быстрого обучения неиронных сетей.
## Главная страница
Главная страница представляет собой сайт, где вы можете загрузить zip-архив с датасетом, выбрать количество эпох и указать требуемое разрешение.
![Главная страница](https://github.com/alexmihalyk23/YPPRO/raw/actions_test/readme_img/Start.png)
## Обучение
В процессе обучения виден прогресс-бар, показывающий текущий статус выполнения.
![Обучение](https://github.com/alexmihalyk23/YPPRO/raw/actions_test/readme_img/Train.png)
## Завершение
После обучения можно загрузить полученную модель, а также быстро проверить её работу, задав показатель **confidence**, что поможет выяснить, достаточно ли обучилась модель.
![Завершение](https://github.com/alexmihalyk23/YPPRO/raw/actions_test/readme_img/End1.png)

# Установка и запуск

**На сервере должен быть установлен Python 3**

```bash
git clone https://github.com/alexmihalyk23/YPPRO
cd YPPRO
pip3 install -r requirements.txt
```

## Запуск
`python3 app.py`

# Руководство по использованию

## Главная страница

![Главная страница](https://github.com/alexmihalyk23/YPPRO/raw/actions_test/readme_img/Start.png)
Для обучения модели проделать следующие шаги:
1. Нажать на кнопку **Choose file** и выбрать zip-архив с датасетом
2. Выбрать количество эпох(**Epochs number**) и разрешение картинки(**Choose resolution**)
3. Нажать на кнопку **Start training**

## Завершение
![Завершение](https://github.com/alexmihalyk23/YPPRO/raw/actions_test/readme_img/End1.png)
- Чтобы загрузить модель, нажать на кнопку **Download**.
- Для повторного обучения нажать на кнопку **Back**, она вернет на главную страницу.
- Чтобы проверить точность модели, нужно выбрать **confidence** c помощью слайдера, а затем нажать на кнопку **Check model**, после чего будет показана картинка с bounding box, confidence которого больше, либо равна заданному ранее.
![Завершение2](https://github.com/alexmihalyk23/YPPRO/raw/actions_test/readme_img/End2)

## Участие
- Михайлюк Алексей: сервер
- Романченко Егор: документация, тесты, оформление
- Рубан Василина: оформление

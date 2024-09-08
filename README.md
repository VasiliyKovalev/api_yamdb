## API_YamDB
REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.
### Описание
*  Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
*  Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
*  Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
*  Добавлять произведения, категории и жанры может только администратор.
*  Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
*  Пользователи могут оставлять комментарии к отзывам.
*  Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
### Технологии:
1. Python 3.9
2. Django
3. DRF
4. Simple JWT
### Как запустить проект:
1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:VasiliyKovalev/api_yamdb.git
```

```
cd api_yamdb
```

2. Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

3. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python3 manage.py migrate
```

5. Запустить проект:

```
python3 manage.py runserver
```

### После запуска проекта, документация будет доступна по адресу:
http://127.0.0.1:8000/redoc/

### База данных
В директории ``` /api_yamdb/static/data ``` подготовлены несколько файлов в формате csv с контентом для ресурсов Users, Titles, Categories, Genres, Reviews и Comments.

### Ресурсы API YaMDb:
* AUTH: аутентификация.
* USERS: пользователи.
* TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песня).
* CATEGORIES: категории произведений («Фильмы», «Книги», «Музыка»).
* GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
* REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
* COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Примеры запросов к API:
* Регистрация нового пользователя. Получение кода подтверждения на переданный email.
```
POST /api/v1/auth/signup/
```
* Получение списка всех категорий.
```
GET /api/v1/categories/
```
* Получение списка всех жанров.
```
GET /api/v1/genres/
```
* Получение информации о произведении.
```
GET /api/v1/titles/{titles_id}/
```
* Добавление нового отзыва на произведение.
```
POST /api/v1/titles/{title_id}/reviews/
```
* Добавление комментария к отзыву.
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
* Получение данных своей учетной записи.
```
GET /api/v1/users/me/
```


### Авторы проекта:
*  [Василий Ковалев](https://github.com/VasiliyKovalev)

*  [Анна Аржакова](https://github.com/arzhakova)


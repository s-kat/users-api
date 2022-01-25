# Методы:


# Auth:


### `POST /login`

В случае успешного входа в систему устанавливает Cookies

Body:
```json
{
  "login": "string",
  "password": "string"
}
```

Response:

Status_code 200
Body:
```json
{
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "mail@exmaple.com",
  "phone": "string",
  "birthday": "01-02-1999"
}
```


Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

---
### `GET /logout`

При успешном выходе удаляет установленные Cookies

Response:

Status code 200

# Admin:
> Команды доступные только администраторам

`POST private/users`

Создание нового пользователя

Body:

```json
{
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-01-25",
  "city": 0,
  "additional_info": "string",
  "is_admin": true,
  "password": "string"
}
```

Response:

Status code 201 Body:
```json
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-01-25",
  "city": 0,
  "additional_info": "string",
  "is_admin": true
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

---
### `GET private/users/{pk}`

Получение полной информации о пользователе с id=pk

Response:

Status code 200 Body:
```json
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-01-25",
  "city": 0,
  "additional_info": "string",
  "is_admin": true
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

Status code 404 - UserNotFound

---
### `DELETE /private/users/{pk}`

Удаляет пользователя с id=pk


Response:

Status code 204


Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

Status code 404 - UserNotFound

---
### `PATCH /private/users/{pk}`

Изменяет информацию о пользователе с id=pk.
В шаблоне подразумевалась возможность изменять id пользователя в системе через этот запрос.
При этом сам id должен задаваться системой при создании пользователя автоматически.
Будем считать, что id пользователя неизменяем, чтобы для каждого пользователя существовал неизменный идентификатор.

Также в качестве логина пользователя используем его email, так что если новый email уже есть в системе, то запрос с ним вызовет исключение с кодом 422


Body:

```json
{
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-01-25",
  "city": 0,
  "additional_info": "string",
  "is_admin": true
}
```

Response:

Status code 200 Body:
```json
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-01-25",
  "city": 0,
  "additional_info": "string",
  "is_admin": true
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

Status code 404 - UserNotFound

---
### `GET /private/users`
Постраниченое получение информации о пользователях.

В шаблоне этот запрос отдавал только краткую информацию о пользователях.
Такой же функционал предусмотрен и для обычных пользователей.
Добавим для администраторов возможность получать полную постраничную информацию о пользователях.

Также в шаблоне был отдельное поле для метаинформации. Так как никаких метаданных, кроме параметров пагинации нам не предоставляется,
то будем использовать стандартный формат ответа из `fastapi-pagination`. В будущем при необходимости можно будет легко
добавить поля с метаинформацией.

Body:
```json
{
    "page" : 1,
    "size": 50
}
```

Reponse: Status code 200 Body:
```json
{
  "items": [
    {
      "first_name": "vasya",
      "last_name": "ivanov",
      "other_name": "string",
      "email": "admin@mail.com",
      "phone": "string",
      "birthday": "01-02-1999",
      "id": 61,
      "additional_info": "string",
      "city": 0,
      "is_admin": true
    },
    {
      "first_name": "string",
      "last_name": "string",
      "other_name": "string",
      "email": "a@a.com",
      "phone": "string",
      "birthday": "01-08-1995",
      "id": 62,
      "additional_info": "string",
      "city": 0,
      "is_admin": false
    },
    {
      "first_name": "vvv",
      "last_name": "sss",
      "other_name": "string",
      "email": "fsd@a.com",
      "phone": "string",
      "birthday": "01-12-1790",
      "id": 63,
      "additional_info": "string",
      "city": 12,
      "is_admin": true
    },
    {
      "first_name": "string",
      "last_name": "string",
      "other_name": "string",
      "email": "dssad@example.com",
      "phone": "string",
      "birthday": "10-04-1990",
      "id": 64,
      "additional_info": "string",
      "city": 0,
      "is_admin": true
    }
  ],
  "total": 4,
  "page": 1,
  "size": 50
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException


---
# User:
> Команды доступные как пользователям, так и администраторам

### `GET /users/current`

Получение информации пользователем о самом себе

Response:

Status code 200 Body:

```json
{
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-01-25",
  "is_admin": true
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

---
### `GET /users`
Получение краткой постраничной информации о всех пользователях.

Response:

Status code 200 Body:
```json
{
  "items": [
    {
      "id": 61,
      "first_name": "vasya",
      "last_name": "ivanov",
      "email": "admin@mail.com"
    },
    {
      "id": 62,
      "first_name": "string",
      "last_name": "string",
      "email": "a@a.com"
    },
    {
      "id": 63,
      "first_name": "vvv",
      "last_name": "sss",
      "email": "fsd@a.com"
    },
    {
      "id": 64,
      "first_name": "string",
      "last_name": "string",
      "email": "dssad@example.com"
    }
  ],
  "total": 4,
  "page": 1,
  "size": 50
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException

---
### `PATCH /users`

Изменить информацию о текущем пользователе. Требование у уникальности email аналогично приватному запросу.

Body:
```json
{
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "user@example.com",
  "phone": "string",
  "birthday": "string"
}
```

Response:

Status code 200 Body:
```json
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "user@example.com",
  "phone": "string",
  "birthday": "string"
}
```

Exceptions:

Status code 422 - Validation Error

Status code 401 - InvalidCredentialsException
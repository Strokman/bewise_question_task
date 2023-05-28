# Question service. Task 1

Для работы сервиса необходимы установленные docker, docker-compose, curl, git, аккаунт на Github

Клонируйте репозиторий:



**Пример запроса к сервису с помощью утилиты curl**
```
curl -iX POST -H "Content-Type: application/json" -d '{"questions_num": integer}' http://127.0.0.1:5000/count
```

Вместо integer в команде укажите количество запрашиваемых вопросов - от 1 до 100 - так как JService принимает запросы
не более чем на 100 вопросов единовременно. Если необходимо большее количество вопросов - сделайте несколько запросов.


$ chmod +x create_service.sh

$ ./create_service.sh
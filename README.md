# Api documentation
Using Localhost

POST `localhost:8000/user/login/`

body:

```
{
    "username":"samandar",
    "password":"1234"
}
```

response:

```
"Logged in"
```

POST `localhost:8000/user/logout/`

```
"Logged out"
```

GET `localhost:8000/api/songs/`

response:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "audio": "http://localhost:8000/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
            "title": "over the moon of the horizon",
            "created_at": "2023-06-11T15:44:39.649826Z",
            "updated_at": "2023-06-11T15:48:12.167141Z",
            "artist": 1,
            "listened": [],
            "likes": [],
            "dislikes": []
        },
        {
            "id": 2,
            "audio": "http://localhost:8000/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt_PbAPob4.mp3",
            "title": "Kechikkan kunim",
            "created_at": "2023-06-11T16:26:36.408167Z",
            "updated_at": "2023-06-11T16:26:36.408195Z",
            "artist": 2,
            "listened": [],
            "likes": [],
            "dislikes": []
        }
    ]
}
```
GET `localhost:8000/api/songs/{id}/`

body:

```
{
    "id": 1,
    "audio": "http://localhost:8000/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
    "title": "Qishloqdan yo'q bo'l",
    "created_at": "2023-06-11T15:44:39.649826Z",
    "updated_at": "2023-06-11T15:48:12.167141Z",
    "artist": 1,
    "listened": [],
    "likes": [],
    "dislikes": []
}
```

POST `localhost:8000/api/songs/1/like/`

response:
```
{
    "id": 1,
    "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
    "title": "Qishloqdan yo'q bo'l",
    "created_at": "2023-06-11T15:44:39.649826Z",
    "updated_at": "2023-06-11T15:48:12.167141Z",
    "artist": 1,
    "listened": [],
    "likes": [1],
    "dislikes": []
}
```

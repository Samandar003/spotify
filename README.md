# Spotify Api documentation
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
    "title": "over the horizon",
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
    "title": "over the horizon",
    "created_at": "2023-06-11T15:44:39.649826Z",
    "updated_at": "2023-06-11T15:48:12.167141Z",
    "artist": 1,
    "listened": [],
    "likes": [1],
    "dislikes": []
}
```

POST `localhost:8000/api/songs/1/dislike/`

response:
```
{
    "id": 1,
    "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
    "title": "over the horizon",
    "created_at": "2023-06-11T15:44:39.649826Z",
    "updated_at": "2023-06-11T15:48:12.167141Z",
    "artist": 1,
    "listened": [],
    "likes": [],
    "dislikes": [1]
}
```

POST `localhost:8000/api/songs/1/listen/`

response:
```
{
    "id": 1,
    "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
    "title": "over the horizon",
    "created_at": "2023-06-11T15:44:39.649826Z",
    "updated_at": "2023-10-09T11:03:43.012804Z",
    "artist": 1,
    "listened": [1],
    "likes": [],
    "dislikes": [1]
}
```

GET `localhost:8000/api/songs/top_listened/`

response:
```
[
    {
        "id": 1,
        "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
        "title": "over the horizon",
        "created_at": "2023-06-11T15:44:39.649826Z",
        "updated_at": "2023-10-09T11:05:41.681513Z",
        "artist": 1,
        "listened": [1],
        "likes": [],
        "dislikes": [1]
    },
    {
        "id": 2,
        "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt_PbAPob4.mp3",
        "title": "Kechikkan sevgim",
        "created_at": "2023-06-11T16:26:36.408167Z",
        "updated_at": "2023-06-11T16:26:36.408195Z",
        "artist": 2,
        "listened": [],
        "likes": [],
        "dislikes": []
    }
]
```
GET `localhost:8000/api/songs/top_liked/`

response:
```
[
    {
        "id": 2,
        "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt_PbAPob4.mp3",
        "title": "Kechikkan sevgim",
        "created_at": "2023-06-11T16:26:36.408167Z",
        "updated_at": "2023-06-11T16:26:36.408195Z",
        "artist": 2,
        "listened": [],
        "likes": [],
        "dislikes": []
    },
    {
        "id": 1,
        "audio": "/media/audios/Xamdam_Sobirov_-_Qishloqqa_qayt.mp3",
        "title": "over the horizon",
        "created_at": "2023-06-11T15:44:39.649826Z",
        "updated_at": "2023-10-09T11:05:41.681513Z",
        "artist": 1,
        "listened": [1],
        "likes": [],
        "dislikes": [1]
    }
]
```

POST `localhost:8000/api/songs/1/add_comment/`

body:
```
{
    "text":"Good song I have ever listened to"
}
```
response:
```
{
    "id": 3,
    "song": 1,
    "text": "Good song I have ever listened to",
    "reply": null
}
```

GET `localhost:8000/api/songs/1/view_comments/`

response:
```
[
    {
        "id": 1,
        "song": 1,
        "text": "He fantastic song I have ever heard",
        "reply": null
    },
    {
        "id": 2,
        "song": 1,
        "text": "He bad song I have ever heard",
        "reply": null
    },
    {
        "id": 3,
        "song": 1,
        "text": "Good song I have ever listened to",
        "reply": null
    }
]
```

POST `localhost:8000/api/songs/1/add_comment/`
body:
```
{
    "text":"it is reply to another comment",
    "reply":3
}
```

response:
```
{
    "id": 4,
    "song": 1,
    "text": "it is reply to another comment",
    "reply": 3
}
```

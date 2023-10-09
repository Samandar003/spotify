# Api documentation
Using Localhost

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
            "title": "Qishloqdan yo'q bo'l",
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
            "title": "Kechikkan sevgim",
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



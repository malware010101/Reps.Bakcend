TORTOISE_ORM = {
    "connections": {
        "default": "postgres://reps_user:admin123@localhost:5432/reps_db"
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        },
    },
}

from celery import Celery


celery_app = Celery(
    "acetone",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=[
        "Blockchain.tasks.blockchain_tasks"
    ],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


celery_app.conf.beat_schedule = {
    "poll-watched-wallets-every-15-seconds": {
        "task": "Blockchain.tasks.blockchain_tasks.poll_watched_wallets",
        "schedule": 15.0,
    },
}
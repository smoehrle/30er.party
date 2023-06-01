"""This is the init class of Celery"""
import itertools
import threading
from pathlib import Path

from celery import Celery
from celery.worker import worker

from website.settings import CELERY_BROKER_URL, INSTALLED_APPS, CELERY_BROKER_INLINE

app = Celery("website", broker=CELERY_BROKER_URL)


def _find_tasks(app_str: str) -> list[str]:
    """Return a list of modules with tasks"""
    if not app_str.startswith("website"):
        return []

    app_dir = Path(".", *app_str.split("."))

    task_file = app_dir / "tasks.py"
    if task_file.exists():
        return [f"{app_str}.tasks"]

    results = []
    task_module = app_dir / "tasks"
    if not task_module.exists():
        return []
    for item in task_module.iterdir():
        if item.is_dir() or item.name.startswith("__"):
            continue
        results.append(f"{app_str}.tasks.{item.stem}")

    return results


class Config:  # pylint: disable=too-few-public-methods
    """This is the config for celery

    https://docs.celeryq.dev/en/stable/userguide/configuration.html
    """

    accept_content = ["json", "pickle"]
    soft_time_limit = 300

    timezone = "Europe/Berlin"
    imports = list(itertools.chain(*[_find_tasks(item) for item in INSTALLED_APPS]))
    broker_transport_options = {"visibility_timeout": 4200}  # 70 min


app.config_from_object(Config)

if CELERY_BROKER_INLINE:
    worker_ = worker.WorkController(app=app)
    thread_ = threading.Thread(target=worker_.start, daemon=True)
    thread_.start()

from datetime import datetime
from app.database import db
from app.models.task import Task


def create_task(data):
    due_date = _parse_date(data.get("due_date"))

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        due_date=due_date,
        priority=data.get("priority", "Medium"),
    )
    db.session.add(task)
    db.session.commit()
    return task.to_dict()


def get_all_tasks(status=None, priority=None):
    query = Task.query

    if status == "completed":
        query = query.filter_by(is_completed=True)
    elif status == "pending":
        query = query.filter_by(is_completed=False)

    if priority:
        query = query.filter_by(priority=priority)

    tasks = query.order_by(Task.due_date.asc().nullslast()).all()
    return [t.to_dict() for t in tasks]


def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    return task.to_dict() if task else None


def update_task(task_id, data):
    task = Task.query.get(task_id)
    if not task:
        return None

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "due_date" in data:
        task.due_date = _parse_date(data["due_date"])
    if "priority" in data:
        task.priority = data["priority"]
    if "is_completed" in data:
        task.is_completed = data["is_completed"]

    db.session.commit()
    return task.to_dict()


def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return False

    db.session.delete(task)
    db.session.commit()
    return True


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()
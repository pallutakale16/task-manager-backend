from flask import Blueprint, request, jsonify
from app.services import task_service

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@task_bp.route("", methods=["GET"])
def list_tasks():
    status = request.args.get("status")      # all / completed / pending
    priority = request.args.get("priority")  # Low / Medium / High
    tasks = task_service.get_all_tasks(status=status, priority=priority)
    return jsonify(tasks), 200


@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_service.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@task_bp.route("", methods=["POST"])
def add_task():
    data = request.get_json()
    task = task_service.create_task(data)
    return jsonify(task), 201


@task_bp.route("/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    data = request.get_json()
    task = task_service.update_task(task_id, data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@task_bp.route("/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    success = task_service.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"}), 200
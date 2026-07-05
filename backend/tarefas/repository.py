from .database import users, projects, tasks, comments


""" gerar proximo ID sequencial """
def _next_id(collection, field):
    last = collection.find_one(sort=[(field, -1)])
    return (last[field] + 1) if last else 1

""" Remover o _id do Mongo """
def _clean(doc):
    if doc:
        doc.pop("_id", None)
    return doc


# ---------------- HELPERS DE REGRAS DE NEGÓCIO ----------------

def user_exists(user_id: int) -> bool:
    return users.find_one({"userId": user_id}) is not None


def project_exists(project_id: int) -> bool:
    return projects.find_one({"projectId": project_id}) is not None


def task_exists(task_id: int) -> bool:
    return tasks.find_one({"taskId": task_id}) is not None


def username_or_email_taken(username: str, email: str, exclude_user_id: int = None) -> bool:
    or_query = {"$or": [{"username": username}, {"email": email}]}
    if exclude_user_id is not None:
        query = {"$and": [or_query, {"userId": {"$ne": exclude_user_id}}]}
    else:
        query = or_query
    return users.find_one(query) is not None


def user_owns_any_project(user_id: int) -> bool:
    return projects.find_one({"owner": user_id}) is not None


def is_project_member(project: dict, user_id) -> bool:
    if project is None or user_id is None:
        return False
    return user_id == project.get("owner") or user_id in project.get("users", [])


def adjust_completed_tasks_count(user_id, delta: int):
    if not user_id:
        return
    users.update_one({"userId": user_id}, {"$inc": {"completedTasksCount": delta}})
    user = users.find_one({"userId": user_id})
    if user and user.get("completedTasksCount", 0) < 0:
        users.update_one({"userId": user_id}, {"$set": {"completedTasksCount": 0}})


def delete_project_cascade(project_id: int) -> bool:
    task_ids = [t["taskId"] for t in tasks.find({"project": project_id}, {"taskId": 1})]
    if task_ids:
        comments.delete_many({"task": {"$in": task_ids}})
    tasks.delete_many({"project": project_id})
    return projects.delete_one({"projectId": project_id}).deleted_count > 0


def delete_task_cascade(task_id: int) -> bool:
    comments.delete_many({"task": task_id})
    return tasks.delete_one({"taskId": task_id}).deleted_count > 0


# ---------------- USERS ----------------

def create_user(data: dict) -> dict:
    data["userId"] = _next_id(users, "userId")
    data.setdefault("completedTasksCount", 0)
    users.insert_one(data)
    return _clean(data)


def list_users() -> list:
    return [_clean(u) for u in users.find()]


def get_user(user_id: int):
    return _clean(users.find_one({"userId": user_id}))


def update_user(user_id: int, data: dict):
    users.update_one({"userId": user_id}, {"$set": data})
    return get_user(user_id)


def delete_user(user_id: int) -> bool:
    result = users.delete_one({"userId": user_id})
    return result.deleted_count > 0


# ---------------- PROJECTS ----------------

def create_project(data: dict) -> dict:
    data["projectId"] = _next_id(projects, "projectId")
    projects.insert_one(data)
    return _clean(data)


def list_projects() -> list:
    return [_clean(p) for p in projects.find()]


def get_project(project_id: int):
    return _clean(projects.find_one({"projectId": project_id}))


def update_project(project_id: int, data: dict):
    projects.update_one({"projectId": project_id}, {"$set": data})
    return get_project(project_id)


def delete_project(project_id: int) -> bool:
    result = projects.delete_one({"projectId": project_id})
    return result.deleted_count > 0


# ---------------- TASKS ----------------

def create_task(data: dict) -> dict:
    data["taskId"] = _next_id(tasks, "taskId")
    tasks.insert_one(data)
    return _clean(data)


def list_tasks() -> list:
    return [_clean(t) for t in tasks.find()]


def get_task(task_id: int):
    return _clean(tasks.find_one({"taskId": task_id}))


def update_task(task_id: int, data: dict):
    tasks.update_one({"taskId": task_id}, {"$set": data})
    return get_task(task_id)


def delete_task(task_id: int) -> bool:
    result = tasks.delete_one({"taskId": task_id})
    return result.deleted_count > 0


# ---------------- COMMENTS ----------------

def create_comment(data: dict) -> dict:
    data["commentId"] = _next_id(comments, "commentId")
    comments.insert_one(data)
    return _clean(data)


def list_comments() -> list:
    return [_clean(c) for c in comments.find()]


def get_comment(comment_id: int):
    return _clean(comments.find_one({"commentId": comment_id}))


def update_comment(comment_id: int, data: dict):
    comments.update_one({"commentId": comment_id}, {"$set": data})
    return get_comment(comment_id)


def delete_comment(comment_id: int) -> bool:
    result = comments.delete_one({"commentId": comment_id})
    return result.deleted_count > 0
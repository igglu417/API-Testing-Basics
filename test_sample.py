import requests
import json
import uuid

ENDPOINT = "https://todo.pixegami.io/"
# response = requests.get(ENDPOINT)
# print(response)

# data = response.json()
# print(data)

# status_code_test = response.status_code
# print(status_code_test)

# GET
# def test_can_call_endpoint():
#     response = requests.get(ENDPOINT)
#     assert response.status_code == 200

# PUT
def test_can_create_task():
    payload = new_task_payload()
    response_put = create_task(payload)
    assert response_put.status_code == 200
    data = response_put.json()
    # print(data)

    task_id = data["task"]["task_id"]
    response_get_put = get_task(task_id)
    assert response_get_put.status_code == 200
    get_task_data = response_get_put.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    # print(get_task_data)


def test_can_update_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    # update the task
    new_payload = {
        "user_id" : payload["user_id"],
        "task_id" : task_id,
        "content" : "my updated content",
        "is_done" : True
                            }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_user():
    # creating n tasks
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # list tasks and check there are n items
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    tasks = data["tasks"]
    assert len(tasks) == n
    # print(data)

def test_can_delete_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    # delete task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    # get the deleted task
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
    # print(get_task_response.status_code)


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    print(f"creating task for user {user_id} with content {content}")
    return {
  "content": content,  # add fake content
  "user_id": user_id,
  "is_done": False
    }

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)


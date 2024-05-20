import requests
import uuid

def test_create_task():
    base_url = "https://todo.pixegami.io"
    user_id = str(uuid.uuid4())
    task_data = {"user_id": user_id, "content": "Finish integration testing", "is_done": False}

    response_put = requests.put(f"{base_url}/create-task", json=task_data)
    assert response_put.status_code == 200
    print(response_put.json())
    task_id = response_put.json()['task']['task_id']

    response_get = requests.get(f"{base_url}/get-task/{task_id}")
    print(response_get.json())
    assert response_get.status_code == 200

    expected_response = {
        "user_id": user_id,
        "content": "Finish integration testing",
        "is_done": False,
        "task_id": task_id,
        "created_time": response_get.json()['created_time'],
        "ttl": response_get.json()['ttl']
    }
    
    assert response_get.json() == expected_response, "GET response mismatch"

    print("Test for creating a task passed successfully.")
    return task_id

task_id = test_create_task()

def test_update_task():
    base_url = "https://todo.pixegami.io"
    user_id = str(uuid.uuid4())
    initial_task_data = {"user_id": user_id, "content": "Initial task", "is_done": False}
    
    response_create = requests.put(f"{base_url}/create-task", json=initial_task_data)
    assert response_create.status_code == 200
    task_id = response_create.json()['task']['task_id']

    updated_data = {"task_id": task_id, "user_id": user_id, "content": "Updated task", "is_done": True}
    response_update = requests.put(f"{base_url}/update-task", json=updated_data)
    print(response_update.json())
    assert response_update.status_code == 200

    response_get = requests.get(f"{base_url}/get-task/{task_id}")
    assert response_get.status_code == 200

    expected_data = {
        "task_id": task_id,
        "user_id": user_id,
        "content": "Updated task",
        "is_done": True,
        "created_time": response_get.json()['created_time'],
        "ttl": response_get.json()['ttl']
    }

    assert response_get.json() == expected_data, "Updated task data does not match expected"

    print("Test for updating a task passed successfully.")

test_update_task()

def test_list_tasks():
    base_url = "https://todo.pixegami.io"
    user_id = str(uuid.uuid4())
    
    created_tasks = []

    for i in range(3):
        task_data = {"user_id": user_id, "content": f"Task {i+1}", "is_done": False}
        response_create = requests.put(f"{base_url}/create-task", json=task_data)
        assert response_create.status_code == 200, "Failed to create task"
        created_task_id = response_create.json().get('task', {}).get('task_id')
        if created_task_id:
            created_tasks.append({
                "task_id": created_task_id,
                "content": task_data['content'],
                "is_done": task_data['is_done']
            })
        else:
            print(f"Task {i+1} creation did not return a valid task ID.")

    response_list = requests.get(f"{base_url}/list-tasks/{user_id}")
    assert response_list.status_code == 200, "Failed to list tasks"
    tasks = response_list.json()['tasks']
    print(tasks)
    assert len(tasks) == len(created_tasks), f"Expected {len(created_tasks)} tasks, got {len(tasks)}"

    listed_task_ids = {task['task_id'] for task in tasks}
    for task in created_tasks:
        assert task['task_id'] in listed_task_ids, f"Task ID {task['task_id']} not listed."

    print("Test for listing tasks passed successfully.")

test_list_tasks()

def test_delete_task():
    base_url = "https://todo.pixegami.io"
    user_id = str(uuid.uuid4())

    task_data = {"user_id": user_id, "content": "Task to be deleted", "is_done": False}
    response_create = requests.put(f"{base_url}/create-task", json=task_data)
    assert response_create.status_code == 200, "Failed to create task for deletion"
    task_id = response_create.json().get('task', {}).get('task_id')
    if not task_id:
        print("Task creation did not return a valid task ID, cannot proceed with delete test.")
        return

    response_delete = requests.delete(f"{base_url}/delete-task/{task_id}")
    assert response_delete.status_code == 200, "Failed to delete task"

    response_get = requests.get(f"{base_url}/get-task/{task_id}")
    assert response_get.status_code == 404, "Task still exists after deletion"

    print("Test for deleting a task passed successfully.")

test_delete_task()
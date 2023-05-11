
import requests
import json
from datetime import timedelta
from datetime import datetime
import os

api_key = os.environ['API_KEY']
time_delta = int(os.environ['TIME_DELTA'])


def load_vm_list():
    with open("vm_list.txt", 'r') as f:
        vm_list = f.read().splitlines()
    return vm_list


def create_snapshot(vm_id):
    vm_info = get_vm_info(vm_id)
    response = requests.post(
        f"https://api.cloudvps.reg.ru/v1/reglets/{vm_id}/actions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "type": "snapshot",
            "name": f'{vm_info["name"]}',
            "offline": 0
        })
    )

    # Обработка ответа
    if response.status_code == 200:
        print(f'Создание снепшота для {vm_info["name"]} запущено')
    else:
        print("Ошибка при создании снепшота:", response.json())


def get_snapshot_list():
    response = requests.get(
        "https://api.cloudvps.reg.ru/v1/snapshots",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )

    snapshots = response.json()

    if 'snapshots' in snapshots:
        return snapshots['snapshots']
    else:
        return None


def delete_snapshot(snapshot_id):
    response = requests.delete(
        f"https://api.cloudvps.reg.ru/v1/snapshots/{snapshot_id}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )

    if response.status_code == 204:
        print(f"Снепшот {snapshot_id} удален")
    else:
        print(f"Снепшот не удален: {response.json()}")


def delete_old_snapshots(time_delta):
    snapshots = get_snapshot_list()
    if snapshots:
        for snapshot in snapshots:
            creation_time = datetime.strptime(
                snapshot["created_at"], "%Y-%m-%d %H:%M:%S")
            print(
                f'[ {snapshot["id"]} ] [ {snapshot["created_at"]} ] {snapshot["name"]}')
            if creation_time < (datetime.now() - timedelta(days=time_delta)):
                delete_snapshot(snapshot['id'])
            else:
                print("Снепшотов для удаления нет")


def get_vm_info(vm_id):
    response = requests.get(
        f"https://api.cloudvps.reg.ru/v1/reglets/{vm_id}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )

    if response.status_code == 200:
        return response.json()['reglet']
    else:
        return None


vm_ids = load_vm_list()

for vm_id in vm_ids:
    create_snapshot(vm_id)

delete_old_snapshots(time_delta)

from nornir import InitNornir
from nornir.core.task import Task, Result, MultiResult
from pprint import pprint as pp
from nornir_napalm.plugins.tasks import napalm_get


def netauto():
    nr = InitNornir(config_file="config.yaml")
    pp(f'''Fulford Devices: {nr.filter(location="fulford").inventory.hosts.keys()}''')
    pp(f'''prd Devices: {nr.filter(env="prd").inventory.hosts}''')
    pp(f'''sbx Devices: {nr.filter(env="sbx").inventory.hosts}''')
    pp(f'''IOS Devices: {nr.filter(net_os="ios").inventory.hosts}''')
    sbx_devices = nr.filter(env="sbx")
    sbx_devices.run(task=backup_config)



def backup_config(task):
    result = task.run(task=napalm_get, getters=["config"])
    running_config = result.result.get("config", {}).get("running", "")

    if running_config:
        print(f"Backup for {task.host}:")
        with open(f"backup_{task.host}.txt", "w") as f:
            f.write(running_config)
    else:
        print(f"No config retrieved for {task.host}")


if __name__ == "__main__":
    netauto()
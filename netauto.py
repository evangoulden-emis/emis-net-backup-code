from pprint import pprint as pp
from nornir import InitNornir
from nornir.core.inventory import ConnectionOptions
from nornir_napalm.plugins.tasks import napalm_get
from git_repo import get_github_instance, upload_file_to_github


def netauto():
    g, repo, backup_dir = get_github_instance()
    nr = InitNornir(config_file="config.yaml")
    sbx_devices = nr.filter(env="sbx")
    sbx_devices.run(task=backup_config)
    upload_file_to_github(g, repo, backup_dir)

def backup_config(task):
    secret = ""
    if task.host.platform == "ios":
        secret = task.host.get("secret")
        if not secret:
            raise ValueError("No secret set for device")
        task.host.connection_options["napalm"] = ConnectionOptions(
            extras={
                "optional_args": {
                    "secret": secret,
                }
            },
            hostname=task.host.hostname,
            username=task.host.username,
            password=task.host.password,
            platform=task.host.platform,
            port=task.host.port,
        )


    result = task.run(task=napalm_get, getters=["config"])
    running_config = result.result.get("config", {}).get("running", "")

    if running_config:
        print(f"Backup for {task.host}:")
        with open(f"./backups/backup_{task.host}.txt", "w") as f:
            f.write(running_config)
    else:
        print(f"No config retrieved for {task.host}")


if __name__ == "__main__":
    netauto()
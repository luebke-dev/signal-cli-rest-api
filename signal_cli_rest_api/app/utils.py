import subprocess
from subprocess import CalledProcessError
from fastapi import HTTPException
from typing import Any, List
from .schemas import AttachmentIn
from .config import settings
import requests
import base64

ALGORITHM = "HS256"


def read_groups(groups_string: str):
    groups = []
    for group in groups_string.split("\n"):
        if group == "":
            continue

        # remove unwanted characters
        chars_to_remove = ["[", "]", ","]

        for char in chars_to_remove:
            group = group.replace(char, "")

        splitted = group.split(" ")
        active_index = splitted.index("Active:")

        id = splitted[1]
        name = " ".join(splitted[3 : active_index - 1])
        active = True if splitted[active_index + 1] == "true" else False
        blocked = True if splitted[active_index + 3] == "true" else False
        members = []

        try:
            members_index = splitted.index("Members:")
            members = splitted[members_index + 1 :]
        except ValueError:
            pass

        groups.append(
            {
                "id": id,
                "name": name,
                "active": active,
                "blocked": blocked,
                "members": members,
            }
        )

    return groups


def save_attachment(attachment: AttachmentIn):
    if attachment.url is None and attachment.content is None:
        raise HTTPException(status_code=422)
    with open(f"{settings.signal_upload_path}{attachment.filename}", "wb") as file:
        content = b""
        if attachment.url:
            r = requests.get(attachment.url, allow_redirects=True)
            if r.status_code != 200:
                raise HTTPException(status_code=400, detail="Downloading image failed")
            content = r.content
        elif attachment.content:
            content = base64.b64decode(attachment.content)

        file.write(content)


def run_signal_cli_command(cmd: List[str], wait: bool = True) -> Any:
    base_cmd = ["signal-cli", "--config", settings.signal_config_path]

    full_cmd = base_cmd + cmd

    if wait:
        try:
            process = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT)
        except CalledProcessError as e:
            raise HTTPException(status_code=422, detail=e.output.decode())
        return process.decode()
    else:
        process = subprocess.Popen(
            full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return process.stdout.readline()

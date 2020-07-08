from signal_cli_rest_api.app.schemas import ProfileUpdate
from signal_cli_rest_api.app.utils import run_signal_cli_command, save_attachment
from signal_cli_rest_api.app.config import settings
from typing import Any, List
from fastapi import APIRouter, Depends

router = APIRouter()


@router.put("/{number}", response_model=ProfileUpdate)
def update_profile(profile: ProfileUpdate, number: str) -> Any:
    """
    Edit a group. You can't remove a member from a group
    """

    cmd = ["-u", number, "updateProfile"]

    if profile.name:
        cmd += ["--n", profile.name]

    if profile.remove_avatar:
        cmd.append("--remove-avatar")
    elif profile.avatar:
        cmd.append("--avatar")
        save_attachment(profile.avatar)
        cmd.append(
            f"{settings.signal_upload_path}{profile.avatar.filename}")

    run_signal_cli_command(cmd)

    return profile

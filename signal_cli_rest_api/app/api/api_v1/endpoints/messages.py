from typing import Any, List
from fastapi import APIRouter
from signal_cli_rest_api.app.schemas import MessageIncoming, MessageOutgoing, MessageSent, ReactionOut
from signal_cli_rest_api.app.utils import run_signal_cli_command, save_attachment
from signal_cli_rest_api.app.config import settings
import json

router = APIRouter()


@router.get("/{number}", response_model=List[MessageIncoming])
def get_messages(number: str) -> Any:
    """
    get messages
    """

    response = run_signal_cli_command(["-u", number, "receive", "--json"])
    return [json.loads(m) for m in response.split("\n") if m != ""]


@router.post("/{number}", response_model=MessageSent, status_code=201)
def send_message(message: MessageOutgoing, number: str) -> Any:
    """
    send message
    """

    cmd = ["-u", number, "send", "-m", message.text]

    cmd += message.receivers

    if len(message.attachments) > 0:
        cmd.append("-a")
        for attachment in message.attachments:
            save_attachment(attachment)
            cmd.append(f"{settings.signal_upload_path}{attachment.filename}")

    if message.group:
        cmd.append("-g")

    response = run_signal_cli_command(cmd)

    return MessageSent(**message.dict(), timestamp=response.split("\n")[0])


@router.post("/{number}/reaction")
def send_reaction(number: str, reaction: ReactionOut) -> Any:
    """
    send a reaction

    https://emojipedia.org/
    """
    cmd = ["-u", number, "sendReaction"]

    if reaction.group:
        cmd += ["-g", reaction.receiver]
    else:
        cmd.append(reaction.receiver)

    cmd += ["-a", reaction.target_number, "-t",
            reaction.target_timestamp, "-e", reaction.emoji]

    run_signal_cli_command(cmd)


@router.delete("/{number}/reaction")
def delete_reaction(number: str, reaction: ReactionOut) -> Any:
    """
    remove a reaction
    """
    cmd = ["-u", number, "sendReaction"]

    if reaction.group:
        cmd += ["-g", reaction.receiver]
    else:
        cmd.append(reaction.receiver)

    cmd += ["-a", reaction.target_number, "-t",
            reaction.target_timestamp, "-e", reaction.emoji, "-r"]

    run_signal_cli_command(cmd)

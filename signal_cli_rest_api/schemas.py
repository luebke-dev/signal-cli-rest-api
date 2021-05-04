from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class AttachmentIn(BaseModel):
    url: Optional[str] = None
    filename: str
    content: Optional[Any] = None


class MessageOutgoing(BaseModel):
    text: str
    receivers: List[str]
    group: bool = False
    groupId: str
    attachments: List[AttachmentIn] = []


class MessageSent(MessageOutgoing):
    timestamp: datetime


class AttachmentOut(BaseModel):
    contentType: str
    filename: Optional[str] = None
    id: str
    size: int


class GroupInfo(BaseModel):
    groupId: str
    members: Optional[List[str]] = None
    name: Optional[str] = None


class DataMessage(BaseModel):
    timestamp: str
    message: Optional[str] = None
    expiresInSeconds: int
    attachments: Optional[List[AttachmentOut]] = None
    groupInfo: Optional[GroupInfo] = None


class Envelope(BaseModel):
    source: str
    sourceDevice: int
    relay: Any
    timestamp: str
    dataMessage: Optional[DataMessage] = None


class MessageIncoming(BaseModel):
    envelope: Envelope
    syncMessage: Any
    callMessage: Any
    receiptMessage: Any


class ReactionOut(BaseModel):
    receiver: str
    group: bool = False
    target_number: str
    target_timestamp: str
    emoji: str


class Block(BaseModel):
    numbers: List[str]
    group: Optional[bool] = False


class GroupCreate(BaseModel):
    name: str
    members: List[str] = []
    avatar: Optional[AttachmentIn] = None


class GroupUpdate(BaseModel):
    name: Optional[str]
    members: List[str] = []
    avatar: Optional[AttachmentIn] = None


class GroupOut(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    members: List[str] = []
    blocked: bool = False
    active: bool = True


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[AttachmentIn] = None
    remove_avatar: Optional[bool] = False


class Verification(BaseModel):
    verification_code: str
    pin: Optional[str] = None

    class Config:
        schema_extra = {"example": {"verification_code": "123456", "pin": None}}


class Registration(BaseModel):
    voice_verification: bool = False
    captcha: Optional[str] = None

    class Config:
        schema_extra = {"example": {"voice_verification": True, "captcha": ""}}

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Tag(BaseModel):
    Name: str
    Id: str


class Organization(BaseModel):
    Id: str


class Contact(BaseModel):
    LastActiveUTC: datetime
    PhoneNumber: str
    ProfilePictureUrl: Optional[str]
    IsBlocked: bool
    ScheduledMessages: List = []
    GroupIdentifier: Optional[str]
    ContactType: str
    Tags: List[Tag]
    Name: str
    Id: str


class Channel(BaseModel):
    _t: str
    ChannelType: str
    Platform: str
    PhoneNumber: str
    Name: str
    Id: str


class Sector(BaseModel):
    Default: bool
    Order: int
    GroupIds: List[str]
    Name: str
    Id: str


class OrganizationMember(BaseModel):
    Muted: bool
    Id: str


class ChatRef(BaseModel):
    Id: str


class SentByOrganizationMember(BaseModel):
    Id: str


class LastMessage(BaseModel):
    Prefix: Optional[str]
    HeaderContent: Optional[str]
    Content: Optional[str]
    Footer: Optional[str]
    File: Optional[str]  # usado para áudio, imagem, documento
    Thumbnail: Optional[str]  # imagens e vídeos
    FileId: Optional[str]  # referência interna
    MessageType: str  # "Text", "Audio", "Image", etc.
    SentByOrganizationMember: Optional[SentByOrganizationMember]
    IsPrivate: bool
    Source: str
    MessageState: str
    EventAtUTC: datetime
    CreatedAtUTC: datetime
    Id: str
    Chat: ChatRef
    Contacts: List = []
    QuotedStatusUpdate: Optional[str]
    Location: Optional[str]
    Question: Optional[str]
    InReplyTo: Optional[str]
    TemplateId: Optional[str]
    Buttons: List = []
    LatestEdit: Optional[str]
    BotInstance: Optional[str]
    ForwardedFrom: Optional[str]
    ScheduledMessage: Optional[str]
    BulkSendSession: Optional[str]
    Elements: Optional[str]
    Mentions: List = []
    Ad: Optional[str]
    Reactions: List = []
    DeductedAiCredits: Optional[str]
    FromContact: Optional[str]


class FirstMessageRef(BaseModel):
    EventAtUTC: datetime
    Id: str


class BotInstance(BaseModel):
    Status: str
    BotId: str
    BotInstanceId: str
    TriggerName: Optional[str]


class LastOrganizationMember(BaseModel):
    Id: str


class ContentModel(BaseModel):
    _t: str
    Organization: Organization
    Contact: Contact
    Channel: Channel
    Sector: Sector
    OrganizationMember: OrganizationMember
    OrganizationMembers: List[OrganizationMember]
    LastMessage: Optional[LastMessage]
    LastMessageReaction: Optional[str]
    RedactReason: Optional[str]
    UsingInactivityFlow: bool
    UsingWaitingFlow: bool
    InactivityFlowAt: Optional[str]
    WaitingFlowAt: Optional[str]
    Open: bool
    Private: bool
    Waiting: bool
    WaitingSinceUTC: Optional[str]
    TotalUnread: int
    ClosedAtUTC: Optional[str]
    EventAtUTC: datetime
    FirstMemberReplyMessage: FirstMessageRef
    FirstContactMessage: FirstMessageRef
    Bots: List[BotInstance]
    LastOrganizationMember: LastOrganizationMember
    Message: Optional[str]
    Visibility: Optional[str]
    Id: str
    CreatedAtUTC: datetime
    Tags: List = []


class PayloadModel(BaseModel):
    Type: str
    Content: ContentModel


class WebhookPayload(BaseModel):
    Type: str
    EventDate: datetime
    Payload: PayloadModel
    EventId: str

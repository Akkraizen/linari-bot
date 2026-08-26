from os import getenv

from aiogram.types import ChatPermissions

from struture.singleton import Singleton

RESTRICTION_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_edit_tag=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False
)


class Config(Singleton):
    def __init__(self):
        if not self.created:
            self.TOKEN = getenv("TOKEN")
            self.CHANNEL_ID = getenv("CHANNEL_ID")
            self.OWNERS = list(map(int, getenv("OWNERS").split(",")))
            self.DATABASE_URL = getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/linari")

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, Integer, String, DateTime, func, Enum
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import Config


class Base(DeclarativeBase):
    pass

class PunishmentAction(PyEnum):
    BAN = "ban"
    MUTE = "mute"
    WARN = "warn"
    UNBAN = "unban"
    UNMUTE = "unmute"
    UNWARN = "unwarn"

class ModeratorLevel(PyEnum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3

class Moderator(Base):
    __tablename__ = "moderators"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    level: Mapped[ModeratorLevel] = mapped_column(Enum(ModeratorLevel), default=ModeratorLevel.LEVEL_1)
    added_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class UserWarn(Base):
    __tablename__ = "user_warns"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    admin_id: Mapped[int] = mapped_column(BigInteger)
    reason: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class UserBan(Base):
    __tablename__ = "user_bans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    admin_id: Mapped[int] = mapped_column(BigInteger)
    reason: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class UserMute(Base):
    __tablename__ = "user_mutes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    admin_id: Mapped[int] = mapped_column(BigInteger)
    reason: Mapped[str] = mapped_column(String, nullable=True)
    until_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class PunishmentLog(Base):
    __tablename__ = "punishment_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    action: Mapped[PunishmentAction] = mapped_column(Enum(PunishmentAction))
    reason: Mapped[str] = mapped_column(String, nullable=True)
    admin_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

engine = create_async_engine(Config().DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


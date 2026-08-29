from functools import wraps
from datetime import timedelta, datetime

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatPermissions
from loguru import logger

from config import RESTRICTION_PERMISSIONS, Config
from services.moderation import ModerationService
from database.models import ModeratorLevel
from utils.time_utils import parse_time_string

router = Router()
moderation_service = ModerationService()
config = Config()

def check_permissions(level: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            if message.from_user.id in config.OWNERS:
                return await func(message, *args, **kwargs)
            
            moderator = await moderation_service.get_moderator(message.from_user.id)
            if not moderator:
                return
            
            if moderator.level.value < level:
                return await message.reply(f"У вас недостаточно прав. Требуется уровень {level}.")
                
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

async def is_moderator(message: Message):
    if message.from_user.id in config.OWNERS:
        return True
    return await moderation_service.is_moderator(message.from_user.id)

@router.message(Command("warn"))
@check_permissions(1)
async def warn_user(message: Message, command: CommandObject):
    if not message.reply_to_message:
        return await message.reply("Эту команду нужно использовать в ответ на сообщение.")
    
    target_user = message.reply_to_message.from_user
    reason = command.args if command.args else "Не указана"
    
    count = await moderation_service.warn_user(target_user.id, message.chat.id, message.from_user.id, reason)
    
    if count >= 3:
        await message.chat.ban(user_id=target_user.id)
        await moderation_service.ban_user(target_user.id, message.chat.id, message.from_user.id, "Превышено лимит варнов (3/3)")
        return await message.answer(f"Пользователь {target_user.full_name} забанен за достижение 3-х предупреждений.")
    return await message.answer(f"Пользователю {target_user.full_name} выдано предупреждение ({count}/3).\nПричина: {reason}")

@router.message(Command("ban"))
@check_permissions(3)
async def ban_user(message: Message, command: CommandObject):
    if not message.reply_to_message:
        return await message.reply("Эту команду нужно использовать в ответ на сообщение.")
    
    target_user = message.reply_to_message.from_user
    reason = command.args if command.args else "Не указана"
    
    try:
        await message.chat.ban(user_id=target_user.id)
        await moderation_service.ban_user(target_user.id, message.chat.id, message.from_user.id, reason)
        await message.answer(f"Пользователь {target_user.full_name} забанен.\nПричина: {reason}")
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        await message.reply("Не удалось забанить пользователя. Проверьте мои права.")

@router.message(Command("mute"))
@check_permissions(2)
async def mute_user(message: Message, command: CommandObject):
    if not message.reply_to_message:
        return await message.reply("Эту команду нужно использовать в ответ на сообщение.")
    
    target_user = message.reply_to_message.from_user

    until_delta = timedelta(minutes=5)
    reason = "Не указана"
    
    if command.args:
        args = command.args.split(maxsplit=1)
        time = parse_time_string(args[0])

        if time is not None:
            until_delta = time
            if len(args) > 1:
                reason = args[1]
        else:
            reason = command.args

    until_date = datetime.now() + until_delta
    
    try:
        await message.chat.restrict(
            user_id=target_user.id,
            permissions=RESTRICTION_PERMISSIONS,
            until_date=until_delta
        )
        time = command.args.split(maxsplit=1)[0] if command.args.split(maxsplit=1)[0] else "5м"
        await moderation_service.mute_user(target_user.id, message.chat.id, message.from_user.id, until_date, reason)
        await message.answer(f"Пользователь {target_user.full_name} замучен на {time}\nПричина: {reason}")
    except Exception as e:
        logger.error(f"Error muting user: {e}")
        await message.reply("Не удалось замутить пользователя. Проверьте мои права.")

@router.message(Command("unwarn"))
@check_permissions(1)
async def unwarn_user(message: Message, command: CommandObject):
    if not message.reply_to_message:
        return await message.reply("Эту команду нужно использовать в ответ на сообщение.")
    
    target_user = message.reply_to_message.from_user
    count = await moderation_service.unwarn_user(target_user.id, message.chat.id, message.from_user.id)
    await message.answer(f"С пользователя {target_user.full_name} снято предупреждение. Текущее количество: {count}/3")

@router.message(Command("unban"))
@check_permissions(3)
async def unban_user(message: Message, command: CommandObject):
    # Можно разбанить по реплаю или по ID
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif command.args:
        if command.args.isdigit():
            user_id = int(command.args)
    
    if not user_id:
        return await message.reply("Укажите ID пользователя или ответьте на его сообщение.")
    
    try:
        await message.chat.unban(user_id=user_id)
        await moderation_service.unban_user(user_id, message.chat.id, message.from_user.id)
        await message.answer(f"Пользователь с ID {user_id} разбанен.")
    except Exception as e:
        logger.error(f"Error unbanning user: {e}")
        await message.reply("Не удалось разбанить пользователя.")

@router.message(Command("unmute"))
@check_permissions(2)
async def unmute_user(message: Message, command: CommandObject):
    if not message.reply_to_message:
        return await message.reply("Эту команду нужно использовать в ответ на сообщение.")
    
    target_user = message.reply_to_message.from_user
    
    try:
        await message.chat.restrict(
            user_id=target_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
            )
        )
        await moderation_service.unmute_user(target_user.id, message.chat.id, message.from_user.id)
        await message.answer(f"Пользователь {target_user.full_name} размучен.")
    except Exception as e:
        logger.error(f"Error unmuting user: {e}")
        await message.reply("Не удалось размутить пользователя.")

@router.message(Command("setmod"))
async def set_moderator(message: Message, command: CommandObject):
    if message.from_user.id not in config.OWNERS:
        return
    
    user_id = None
    level = 1
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if command.args and command.args.isdigit():
            level = int(command.args)
    elif command.args:
        args = command.args.split()
        if args[0].isdigit():
            user_id = int(args[0])
            if len(args) > 1 and args[1].isdigit():
                level = int(args[1])
    
    if not user_id:
        return await message.reply("Укажите ID пользователя или ответьте на его сообщение.")
    
    if level < 1 or level > 3:
        return await message.reply("Уровень модератора должен быть от 1 до 3.")
    
    await moderation_service.add_moderator(user_id, level)
    await message.answer(f"Пользователь {user_id} назначен модератором {level} уровня.")

@router.message(Command("delmod"))
async def del_moderator(message: Message, command: CommandObject):
    if message.from_user.id not in config.OWNERS:
        return
    
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif command.args and command.args.isdigit():
        user_id = int(command.args)
        
    if not user_id:
        return await message.reply("Укажите ID пользователя или ответьте на его сообщение.")
        
    await moderation_service.remove_moderator(user_id)
    await message.answer(f"Пользователь {user_id} больше не является модератором.")

@router.message(Command("warns"))
async def list_warns(message: Message, command: CommandObject):
    target_user_id = None
    target_user_name = "Пользователь"
    
    if message.reply_to_message:
        target_user_id = message.reply_to_message.from_user.id
        target_user_name = message.reply_to_message.from_user.full_name
    elif command.args and command.args.isdigit():
        target_user_id = int(command.args)
        target_user_name = f"Пользователь ID {target_user_id}"
    
    if not target_user_id:
        target_user_id = int(message.from_user.id)
        
    warns = await moderation_service.get_user_warns(target_user_id, message.chat.id)
    
    if not warns:
        return await message.answer(f"У пользователя {target_user_name} нет предупреждений.")
        
    text = f"Предупреждения пользователя {target_user_name} ({len(warns)}/3):\n\n"
    for i, warn in enumerate(warns, 1):
        date_str = warn.created_at.strftime("%d.%m.%Y %H:%M")
        text += f"{i}. Причина: {warn.reason}\n   Дата: {date_str}\n"
        
    await message.answer(text)

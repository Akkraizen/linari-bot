from aiogram import Router

from config import Config

router = Router(name="message_router")
config = Config()


#@router.message(F.content_type.not_in({
#    'new_chat_members', 'left_chat_member',
#    'new_chat_title', 'new_chat_photo',
#    'delete_chat_photo', 'group_chat_created',
#    'pinned_message'
#}))
#async def default_handler(message: Message) -> None:
#    member_status = await get_member_status(message.bot, config.CHANNEL_ID, message.from_user.id)
#    logger.info(member_status)
#
#    if not isinstance(member_status, (ChatMemberLeft, ChatMemberBanned)):
#        return
#
#    await message.delete()
#    logger.info(f"Message from {message.from_user.full_name} was deleted")
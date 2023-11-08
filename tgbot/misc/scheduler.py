from datetime import datetime, timedelta

from create_bot import config, scheduler, bot, logger
from tgbot.services.vk_api import VkApi


admins = config.tg_bot.admin_ids


class CreateTask:

    @staticmethod
    async def __check_conversations():
        conversations = await VkApi.get_messages()
        for conv in conversations:
            conv_utc_dtime = datetime.fromtimestamp(conv["last_message"]["date"]) - timedelta(hours=3)
            logger.warning(conv_utc_dtime)
            logger.warning(datetime.utcnow() - timedelta(seconds=15.3))
            if conv_utc_dtime > datetime.utcnow() - timedelta(seconds=15.3):
                user_id = conv["conversation"]["peer"]["id"]
                username = await VkApi.get_user(user_id=user_id)
                text = conv["last_message"]["text"]
                msg_text = f"Новое сообщение от {username}\n---\n{text}"
                for admin in admins:
                    await bot.send_message(chat_id=admin, text=msg_text)
                    break

    @classmethod
    async def create_task(cls):
        scheduler.add_job(func=cls.__check_conversations,
                          trigger="interval",
                          seconds=15,
                          misfire_grace_time=None)

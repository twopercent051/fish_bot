from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from create_bot import scheduler
from .filters import AdminFilter
from ...misc.scheduler import CreateTask
from ...services.vk_api import VkApi

router = Router()
router.message.filter(AdminFilter())


@router.message(Command("start"))
async def main_block(message: Message):
    group_name = await VkApi.get_group_name()
    text = f"👀 Начали мониторить сообщения группы <code>{group_name}</code>"
    scheduler.remove_all_jobs()
    await CreateTask.create_task()
    scheduler.start()
    await message.answer(text)

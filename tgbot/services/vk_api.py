import asyncio
from typing import Optional, List

import aiohttp

from create_bot import config


class VkApi:
    TOKEN = config.vk.token
    GROUP = config.vk.group

    @classmethod
    async def _get_request(cls, url: str, data: Optional[dict] = None):
        headers = dict(Authorization=f"Bearer {cls.TOKEN}")
        data["v"] = 5.154
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=data) as resp:
                if resp.status < 400:
                    return await resp.json()

    @classmethod
    async def get_group_name(cls) -> str:
        url = f"https://api.vk.ru/method/groups.getById"
        data = dict(group_id=cls.GROUP)
        res = await cls._get_request(url=url, data=data)
        return res["response"]["groups"][0]["name"]

    @classmethod
    async def get_messages(cls) -> List[dict]:
        url = f"https://api.vk.ru/method/messages.getConversations"
        data = dict(offset=0, count=200, group_id=cls.GROUP)
        res = await cls._get_request(url=url, data=data)
        return res["response"]["items"]

    @classmethod
    async def get_user(cls, user_id: int):
        url = f"https://api.vk.ru/method/users.get"
        data = dict(user_ids=[user_id], name_case="gen")
        res = await cls._get_request(url=url, data=data)
        first_name = res["response"][0]["first_name"]
        last_name = res["response"][0]["last_name"]
        return f"{first_name} {last_name}"


async def main():
    await VkApi.get_group_name()
    # print(datetime.fromtimestamp(1698693211))
    # print(datetime.utcnow().timestamp())


if __name__ == "__main__":
    asyncio.run(main())


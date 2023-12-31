from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class RedisConfig:
    host: str
    port: str
    db: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Vk:
    token: str
    group: int


@dataclass
class Miscellaneous:
    admin_group: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    rds: RedisConfig
    misc: Miscellaneous
    vk: Vk


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        rds=RedisConfig(
            host=env.str('REDIS_HOST'),
            port=env.str('REDIS_PORT'),
            db=env.str('REDIS_DB')
        ),
        vk=Vk(
            token=env.str("VK_TOKEN"),
            group=env.int("VK_GROUP_ID")
        ),
        misc=Miscellaneous(
            admin_group=env.str('ADMIN_GROUP')
        )
    )

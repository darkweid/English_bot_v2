from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    redis_dsn: str
    postgres_dsn: str
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), redis_dsn=env('REDIS_DSN'), postgres_dsn=env('POSTGRES_DSN'),
                               admin_ids=env.list('ADMIN_IDS')))

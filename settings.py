from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, BaseModel, Field


class MyBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='allow')


class SmtpConf(MyBaseSettings):
    smtp_login: EmailStr = 'example@mail.com'
    smtp_pass: str = ''
    smtp_server: str = ''
    smtp_port: int = 123


class RabbitMQ(MyBaseSettings):
    rmq_host: str = ''
    rmq_port: int = ''
    rmq_user: str = ''
    rmq_pass: str = ''
    queue: str = ''


class Settings(MyBaseSettings):
    smtp: SmtpConf = SmtpConf()
    rmq: RabbitMQ = RabbitMQ()


settings = Settings()

if __name__ == '__main__':
    pass

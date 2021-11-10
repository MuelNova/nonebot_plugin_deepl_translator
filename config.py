from pydantic import BaseSettings


class Config(BaseSettings):
    api_keys = ['']  # 可以添加多个

    class Config:
        extra = "ignore"

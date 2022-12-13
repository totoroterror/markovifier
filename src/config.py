from pydantic import BaseSettings, Field, RedisDsn


class Config(BaseSettings):
    BOT_TOKEN: str = Field(..., env='BOT_TOKEN')
    REDIS_DSN: RedisDsn = Field(..., env='REDIS_DSN')
    MAX_OVERLAP_RATIO: float = Field(default=0.85, env='MAX_OVERLAP_RATIO')
    MAX_OVERLAP_TOTAL: int = Field(default=20, env='MAX_OVERLAP_TOTAL')
    MESSAGE_CHANCE: int = Field(default=10, env='MESSAGE_CHANCE')
    MESSAGE_RATE_LIMIT: int = Field(default=20, env='MESSAGE_RATE_LIMIT')

    class Config:
        case_sentive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()

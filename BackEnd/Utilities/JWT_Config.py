from pydantic_settings import BaseSettings , SettingsConfigDict

class JWT_Config(BaseSettings):
    model_config = SettingsConfigDict(env_file = "./env/.jwt.env")
    key : str
    token_expire_time : int
    algorithm : str
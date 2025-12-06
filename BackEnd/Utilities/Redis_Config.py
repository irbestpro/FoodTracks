from pydantic_settings import BaseSettings , SettingsConfigDict

class Redis_Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="./env/.env")
    host : str
    db : int # Data base ID in Cach
    password : str
    port: int
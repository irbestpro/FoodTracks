from pydantic_settings import BaseSettings , SettingsConfigDict

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file = './env/.db.env')

    Database : str
    DB_User : str| None = "postgres"
    password : str
    host : str
    port : int

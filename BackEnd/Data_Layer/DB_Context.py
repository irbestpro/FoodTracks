from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from Utilities.DB_Settings import Setting

setting = Setting()
connection_str = f"postgresql://{setting.DB_User}:{setting.password}@{setting.host}/{setting.Database}" # Connection String
Engine = create_engine(url = connection_str) # SqlConnection
Session = sessionmaker(autoflush=False , autocommit = False , bind=Engine) # SqlCommand
Base = declarative_base()
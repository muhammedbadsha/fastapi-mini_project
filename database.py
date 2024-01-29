from decouple import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import create_engine
from urllib.parse import quote_plus


username_mysql = config('MYSQL_USER')
password_mysql = config('MYSQL_PASSWORD')
database_mysql = config('MYSQL_DB')
localhost_mysql = config('MYSQL_HOST')
database_port = config('MYSQL_PORT')



DATABASE_URL = f"mysql+mysqlconnector://{username_mysql}:{password_mysql}@{localhost_mysql}:{database_port}/{database_mysql}"
print(DATABASE_URL)


engine = create_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()



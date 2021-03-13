# Configuration
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

config_file = open('./.config.json', "r")
config = json.load(config_file)
database = config["database"]
# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
engine = create_engine(database)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

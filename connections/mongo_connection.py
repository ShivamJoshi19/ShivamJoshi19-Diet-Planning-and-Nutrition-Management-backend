import os
import toml
from pymongo.mongo_client import MongoClient


class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            cls._instance.client = cls._connect_to_mongodb()
            cls._instance.db = cls._instance.client['dietManagement'] if cls._instance.client else None
        return cls._instance

    @staticmethod
    def _connect_to_mongodb():
        config_path = os.path.abspath("config.toml")
        try:
            with open(config_path, "r", encoding="utf-8") as toml_file:
                config = toml.load(toml_file)
                uri = config.get("Database")["db_mongo_url"]
            client = MongoClient(uri)
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return client
        except FileNotFoundError as e:
            print(f"Error: File not found: {e}")
        except (ValueError, TypeError) as e:
            print(f"Invalid input data: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    @classmethod
    def get_db(cls):
        instance = cls.__new__(cls)
        if instance.db is None:
            raise ConnectionError("Failed to connect to MongoDB.")
        return instance.db

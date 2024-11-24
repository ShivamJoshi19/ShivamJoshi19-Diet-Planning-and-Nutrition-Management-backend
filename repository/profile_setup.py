from datetime import datetime, timezone
from custom_utils import custom_utils
from connections.mongo_connection import MongoConnection
from models.user_authentication import UserProfileModel

db = MongoConnection.get_db()


class UserProfileRepository:

    @staticmethod
    def profile_set_up(collection_name: str, user_id: str, first_name: str,
                       last_name: str, age: str, weight: str, height: str, gender: str):
        try:
            collection = db[collection_name]
            now = datetime.now(timezone.utc)
            user_data = UserProfileModel(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                age=age,
                weight=weight,
                height=height,
                gender=gender,
                created_at=now,
                updated_at=now,
                is_active=True
            )
            collection.insert_one(user_data.dict())
            return user_id
        except custom_utils.CustomException as e:
            raise e
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while profile setup user: {str(e)}")

    @staticmethod
    def get_user_by_user_id(collection_name, user_id: str):
        collection = db[collection_name]
        return collection.find_one({"user_id": user_id})

    @staticmethod
    def get_user_email_by_id(collection_name, user_id: str):
        collection = db[collection_name]
        return collection.find_one({"user_id": user_id})

    @staticmethod
    def create_query(collection_name, query):
        try:
            collection = db[collection_name]
            query_data = query.dict()
            collection.insert_one(query_data)
        except Exception as e:
            raise Exception(f"Database operation failed: {str(e)}")

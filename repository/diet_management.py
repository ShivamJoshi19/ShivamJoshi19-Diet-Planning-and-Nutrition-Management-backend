from datetime import datetime, timezone
from connections.mongo_connection import MongoConnection
from custom_utils import custom_utils
from dto.response_dto.diet_management_response_dto import UserQueryResponse
from models.diet_management import DietPlanModel

db = MongoConnection.get_db()


class DietManagementRepositoy:
    @staticmethod
    def get_active_users_query(collection_name):
        collection = db[collection_name]

        active_queries = list(
            collection.find({"is_active": True}))

        if not active_queries:
            raise custom_utils.CustomException(
                status_code=404, message="No active user queries found")

        # Transform MongoDB documents to Pydantic model
        response = [
            UserQueryResponse(
                user_id=query["user_id"],
                first_name=query["first_name"],
                allergic_to_food=query.get("allergic_to_food"),
                preference=query["preference"],
                disease=query.get("disease"),
                diet_plan=query["diet_plan"],
                query_message=query.get("query_message"),
                status=query["status"],
                created_at=query["created_at"],
                updated_at=query["updated_at"],
                is_active=query["is_active"]
            )
            for query in active_queries
        ]

        return response

    @staticmethod
    def create_user_plan(user_id: str, breakfast: str,
                         lunch: str, dinner: str, water_intake: str,
                         exercise: str, plan_duration: str,
                         description: str, collection_name):
        try:
            collection = db[collection_name]
            now = datetime.now(timezone.utc)
            user_plan = DietPlanModel(
                user_id=user_id,
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
                water_intake=water_intake,
                exercise=exercise,
                plan_duration=plan_duration,
                description=description,
                created_at=now,
                updated_at=now,
                is_active=True
            )
            collection.insert_one(user_plan.dict())
            return user_id
        except custom_utils.CustomException as e:
            raise e
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while profile setup user: {str(e)}")

    @staticmethod
    def update_user_query(collection_name, user_id: str, update_data: dict):
        """
        Updates the UserQuery document in MongoDB for the given user_id.

        Args:
            user_id (str): The ID of the user whose query needs to be updated.
            update_data (dict): The data to update in the query document.

        Returns:
            UpdateResult: The result of the update operation.
        """
        collection = db[collection_name]
        return collection.update_one(
            {"user_id": user_id},  # Query filter
            {"$set": update_data}  # Update operation
        )

    @staticmethod
    def get_active_user_query(user_id: str, collection_name):
        """
        Fetches the active query for the given user_id.

        Args:
            user_id (str): The ID of the user whose active query needs to be fetched.

        Returns:
            dict: The active query document, or None if no active query is found.
        """
        collection = db[collection_name]
        return collection.find_one(
            {"user_id": user_id, "is_active": True}
        )

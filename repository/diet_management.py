from connections.mongo_connection import MongoConnection
from custom_utils import custom_utils
from dto.response_dto.diet_management_response_dto import UserQueryResponse

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

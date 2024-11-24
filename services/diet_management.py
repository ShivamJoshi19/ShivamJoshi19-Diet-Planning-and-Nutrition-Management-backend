from repository import diet_management

DIET_COLLECTION = "DietPlan"
USER_QUERY_COLLECTION = "UserQuery"


class DietManager:
    @staticmethod
    def get_active_user_queries():
        try:
            response = diet_management.DietManagementRepositoy.get_active_users_query(
                USER_QUERY_COLLECTION)
            return response
        except Exception as e:
            raise e

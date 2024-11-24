from datetime import datetime, timezone
from repository import diet_management, profile_setup
from custom_utils import custom_utils

DIET_COLLECTION = "DietPlan"
USER_QUERY_COLLECTION = "UserQuery"
USER_PROFILE_COLLECTION = "UserProfile"
USER_COLLECTION = "User"


class DietManager:
    @staticmethod
    def get_active_user_queries():
        try:
            active_queries = diet_management.DietManagementRepositoy.get_active_users_query(
                USER_QUERY_COLLECTION)
            enriched_responses = []
            for query in active_queries:
                user_id = query.user_id
                user_profile = profile_setup.UserProfileRepository.get_user_by_user_id(
                    USER_PROFILE_COLLECTION, user_id)
                if user_profile:
                    query.first_name = user_profile.get(
                        "first_name", query.first_name)
                    query.last_name = user_profile.get(
                        "last_name", "")
                    query.age = user_profile.get("age", "")
                    query.height = user_profile.get("height", "")
                    query.weight = user_profile.get("weight", "")
                    query.gender = user_profile.get("gender", "")
                    try:
                        height = query.height
                        weight = query.weight
                        if height and weight:
                            # Convert height (cm -> meters)
                            height_in_meters = float(height) / 100.0
                            # Convert weight to float (kg)
                            weight_in_kg = float(weight)
                            bmi = round(weight_in_kg /
                                        (height_in_meters ** 2), 2)
                            query.bmi = bmi
                        else:
                            query.bmi = None
                    except (ValueError, TypeError):
                        raise custom_utils.CustomException(
                            message="Invalid height or weight for BMI calculation",
                            status_code=400
                        )

                enriched_responses.append(query)
            return enriched_responses
        except Exception as e:
            raise e

    @staticmethod
    def create_user_plan(user_id: str, breakfast: str,
                         lunch: str, dinner: str, water_intake: str,
                         exercise: str, plan_duration: str,
                         description: str):
        try:
            user_document = profile_setup.UserProfileRepository.get_user_by_user_id(
                USER_PROFILE_COLLECTION, user_id)
            if not user_document:
                raise custom_utils.CustomException(
                    message="User not found", status_code=404)
            user_data = user_document
            user_doc = profile_setup.UserProfileRepository.get_user_email_by_id(
                USER_COLLECTION, user_id)
            user_email = user_doc.get('email')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            full_name = f"{first_name} {last_name}"
            active_query = diet_management.DietManagementRepositoy.get_active_user_query(
                user_id, USER_QUERY_COLLECTION)
            if not active_query:
                raise custom_utils.CustomException(
                    message="No active query found for the user",
                    status_code=404
                )
            # Create the user plan in the DietManagement repository
            diet_management.DietManagementRepositoy.create_user_plan(
                user_id, breakfast, lunch, dinner, water_intake,
                exercise, plan_duration, description, DIET_COLLECTION
            )

            # Update the UserQuery in MongoDB
            update_result = diet_management.DietManagementRepositoy.update_user_query(
                USER_QUERY_COLLECTION,
                user_id=user_id,
                update_data={
                    "is_active": False,
                    "status": "resolved",
                    "updated_at": datetime.now(timezone.utc)
                },
            )

            # Validate if the update was successful
            if not update_result.matched_count:
                raise custom_utils.CustomException(
                    message="Failed to find and update user query",
                    status_code=404
                )
            subject = "HealthQuest Diet Plan"
            html_content_for_user_query = custom_utils.render_template("diet_plan.html", {
                "full_name": full_name
            })
            email_response = custom_utils.send_email(
                user_email, subject, html_content_for_user_query)
            return {
                "email": email_response['email'],
                "user_id": user_id,
                "message": "Diet Plan created successfully"
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_diet_plan(user_id: str):
        diet_plan = profile_setup.UserProfileRepository.get_user_by_user_id(
            DIET_COLLECTION, user_id)
        if not diet_plan:
            raise custom_utils.CustomException(
                message="Diet plan not found", status_code=404)
        return diet_plan

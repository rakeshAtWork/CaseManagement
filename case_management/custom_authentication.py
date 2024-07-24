# dms_project/custom_authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        x_api_key = request.headers.get('X-API-KEY')

        if x_api_key:
            print(f"X-API-KEY: {x_api_key}")
            # You can add additional logic here if needed
            return None

        return super().authenticate(request)

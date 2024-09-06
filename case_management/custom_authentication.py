import json
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, timezone as dt_timezone
from rest_framework.authentication import BaseAuthentication
from decouple import config
import jwt
from rest_framework.exceptions import AuthenticationFailed
from user_management.models import TokenModule

UserModel = get_user_model()


def check_expiration(decoded_token):
    try:
        exp = decoded_token.get("exp")

        if exp:
            # Convert the expiration time from seconds to a datetime object
            exp_datetime = datetime.fromtimestamp(exp, dt_timezone.utc)
            current_datetime = datetime.now(dt_timezone.utc)

            # Check if the token has expired
            if exp_datetime < current_datetime:
                return True
            else:
                return False
        else:
            return True

    except Exception as e:
        print(e)
        return True


def get_token_from_request(request):
    header = request.META.get('HTTP_AUTHORIZATION', None)
    if header is None:
        return None

    parts = header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]


def validate_token(token):
    try:
        # Decode the token without verifying the signature
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        azure_ad = json.loads(config("AZURE_AD_DATA").replace("\'", "\""))
        tenant_id = azure_ad.get("tenant_id")

        # Check if 'iss' claim is present
        issuer = decoded_token.get('iss')
        if issuer is None:
            raise AuthenticationFailed('Token missing issuer claim')

        # Validate the issuer
        expected_issuer = f'https://sts.windows.net/{tenant_id}/'
        if issuer != expected_issuer:
            raise AuthenticationFailed('Invalid issuer')

        # Check if the token has expired
        expired_token = check_expiration(decoded_token)
        if expired_token:
            raise AuthenticationFailed('Token has expired')

        # Retrieve the email from the token
        email = decoded_token.get("upn") or decoded_token.get('unique_name')
        if email is None:
            raise AuthenticationFailed('Token missing email claim')

        # Update last login time
        UserModel.objects.filter(email=email).update(last_login=timezone.now())

        return email

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except Exception as e:
        print(e)
        raise AuthenticationFailed('Token validation failed')


class AzureJWTAuthenticationBackend(BaseAuthentication):
    def authenticate(self, request):
        x_api_key = request.headers.get('X-API-KEY')

        if x_api_key:
            try:
                token_object = TokenModule.objects.get(primary_token=x_api_key)
            except TokenModule.DoesNotExist:
                raise AuthenticationFailed('Invalid token')

            if token_object.expiry_time < timezone.now():
                raise AuthenticationFailed('Token expired')

            registered_user = token_object.user_id
            return registered_user, x_api_key

        token = get_token_from_request(request)
        if token is None:
            return None

        # Validate the token
        try:
            user_email = validate_token(token)
        except AuthenticationFailed:
            return None
        except Exception as e:

            print(e)
            return None

        # Retrieve the user object from the database
        try:
            user = UserModel.objects.get(email__iexact=user_email, is_active=True)
        except UserModel.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

        # Authentication succeeded
        return user, token
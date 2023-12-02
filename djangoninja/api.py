from cooking.api import router as cooking_router
from cooking.models import Token
from ninja.security import APIKeyHeader
from ninja import NinjaAPI


class ApiKey(APIKeyHeader):
    param_name = "Authorization"

    def authenticate(self, request, key):
        try:
            return Token.objects.get(token=key).user
        except Token.DoesNotExist:
            return None


header_key = ApiKey()
api = NinjaAPI()

api.add_router("/cooking", cooking_router, auth=header_key)
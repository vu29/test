from datetime import datetime
from functools import wraps

import jwt
import pytz
from jwt import DecodeError
from rest_framework import status
from rest_framework.response import Response

from comm_bidso.utils.datetime import parse_iso_format


def jwt_login_required(user_types=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            try:
                try:
                    token = request.META["HTTP_BEARER"]
                except KeyError:
                    return Response(
                        {
                            "message": "JWT token missing",
                            "status": "error",
                            "response": None,
                        },
                        status.HTTP_401_UNAUTHORIZED,
                    )

                with open("authbidso/apps/common/data/public_key.pem", "rb") as file:
                    public_key = file.read()

                decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])

                user = decoded_token["user"]
                expire_dt = decoded_token["expires_at"]

                if datetime.now(tz=pytz.UTC) >= parse_iso_format(expire_dt):
                    return Response(
                        {
                            "message": "Token expired",
                            "status": "error",
                            "response": None,
                        },
                        status.HTTP_401_UNAUTHORIZED,
                    )

                if not user or user.get("user_type") is None:
                    return Response(
                        {
                            "message": "Invalid Token",
                            "status": "error",
                            "response": None,
                        },
                        status.HTTP_401_UNAUTHORIZED,
                    )

                if user_types is not None and user.get("user_type") not in user_types:
                    return Response(
                        {
                            "message": "Unauthorized access of {}, method only allows {}".format(
                                user.get("user_type"), ", ".join(user_types)
                            ),
                            "status": "error",
                            "response": None,
                        },
                        status.HTTP_401_UNAUTHORIZED,
                    )

                return view_func(self, request, *args, **kwargs)
            except DecodeError:
                return Response(
                    {"message": "Invalid Token", "status": "error", "response": None},
                    status.HTTP_401_UNAUTHORIZED,
                )

        return wrapper

    return decorator

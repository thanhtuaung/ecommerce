from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User



class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs: Any):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            
        return None
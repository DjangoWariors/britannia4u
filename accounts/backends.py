from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class OTPBackend(ModelBackend):
    def authenticate(self, request, username=None, otp=None, **kwargs):
        UserModel = get_user_model()
        print('in custom')
        try:
            user = UserModel.objects.get(username=username, secrete_otp=otp)
            if user:
                return user
        except UserModel.DoesNotExist:
            return None
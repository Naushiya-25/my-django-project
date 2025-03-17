from django.contrib.auth.backends import BaseBackend
from .models import User  

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            
            if user.check_password(password):
                return user
            else:
                print("EmailBackend: Password check failed")
                return None
                
        except User.DoesNotExist:
            return None
        except Exception as e:
            print(f"EmailBackend: Unexpected error: {str(e)}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

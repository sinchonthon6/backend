from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, oauth_id, **kwargs):
        if not email:
            raise ValueError('The Email must be set')
        if not oauth_id:
            raise ValueError('The ID must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            oauth_id=oauth_id,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, oauth_id=0, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
            oauth_id=oauth_id,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save()
        return superuser
from django.contrib.auth.models import BaseUserManager, Permission

from account_app.models import Role

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_doctor(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        extra_fields.setdefault('is_staff', True)  # Assuming doctors can access admin panel
        user = self.create_user(username, email, password, **extra_fields)
        role, _ = Role.objects.get_or_create(name='doctor')
        user.roles.add(role)
        return self.create_user(username, email, password, **extra_fields)

    def create_patient(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        user = self.create_user(username, email, password, **extra_fields)
        role, _ = Role.objects.get_or_create(name='patient')
        user.roles.add(role)
        return self.create_user(username, email, password, **extra_fields)

    def create_admin(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        user = self.create_user(username, email, password, **extra_fields)
        role, _ = Role.objects.get_or_create(name='admin')
        user.roles.add(role)
        can_view_admin = Permission.objects.get(codename='view_admin')
        user.user_permissions.add(can_view_admin)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not extra_fields.get('phone_number'):
            raise ValueError('Superusers must have a phone number.')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

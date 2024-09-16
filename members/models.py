from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.crypto import get_random_string

ACCOUNT_STATUS_CHOICE = [
    ('Activated', 'Activated'),
    ('Deactivated', 'Deactivated'),
]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, address, contact, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, first_name=first_name, last_name=last_name, address=address, contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, first_name, last_name, address, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff user must have is_staff=True.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('Staff user must have is_superuser=False.')

        return self.create_user(username, first_name, last_name, address, contact, password, **extra_fields)

    def create_superuser(self, username, first_name, last_name, address, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(username, first_name, last_name, address, contact, password, **extra_fields)
        user.set_password(password)  # Explicitly hash the password here
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser, PermissionsMixin):
    mem_number = models.PositiveIntegerField(unique=True, editable=False)  # Unique and not editable
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    other_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    contact = models.CharField(max_length=11)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11, editable=False)
    password = models.CharField(max_length=128)  # Use set_password for hashing
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='member_images/', blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'contact']

    groups = models.ManyToManyField(
        Group,
        related_name='member_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='member_set',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the user is being created for the first time
            # Generate a unique mem_number before saving
            self.mem_number = self.generate_unique_mem_number()
        # Hash the password if it is not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):  
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def generate_unique_mem_number(self):
        while True:
            # Generate a 6-digit unique number
            new_mem_number = int(get_random_string(length=6, allowed_chars='0123456789'))
            if not Member.objects.filter(mem_number=new_mem_number).exists():
                return new_mem_number

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Message(models.Model):
    sender = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)  # To differentiate between initial messages and replies
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} - {self.subject}"


class Notification(models.Model):
    user = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user}'
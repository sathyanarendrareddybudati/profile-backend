from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email,name, phone_number,password=None,confirm_password=None):
        """
        Creates and saves a User with the given email, name ,tc and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    id = models.AutoField(db_column='uid', primary_key=True)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name=models.CharField(max_length=200,null=True)
    phone_regex = RegexValidator(
		regex=r"^\+?1?[6789]\d{9,12}$",
		message="Please enter a valid phone number. Up to 13 digits allowed.",
	)
    phone_number = models.CharField(
		validators=[phone_regex], max_length=20, blank=True, db_index=True, db_column='mobile_number'
	)  # validators should be a list
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone_number']

    def __str__(self):
        return "%s - %s" % (self.id, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: No, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=255)
    profile_picture = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.name
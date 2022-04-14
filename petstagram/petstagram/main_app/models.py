import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, EmailValidator
from django.db import models
from django.db.models import CASCADE

from petstagram.accounts.models import PetstagramUser
from petstagram.main_app.custom_validators import only_letters_validator, validate_file_max_size

UserModel = get_user_model()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Do not show', 'Do not show'),
    )
    first_name = models.CharField(
        verbose_name="First Name:",
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )
    last_name = models.CharField(
        verbose_name="Last Name:",
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )
    profile_picture = models.URLField(
        verbose_name="Link to Profile Picture:"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        validators=(EmailValidator,),
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=max([len(x) for x, _ in GENDER_CHOICES]),
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    user = models.OneToOneField(PetstagramUser, on_delete=CASCADE, primary_key=True)

    def __str__(self):
        return f" id:{self.id}- {self.first_name}"


class Pet(models.Model):
    TYPE_CHOICES = (
        ("Cat", "Cat"),
        ("Dog", "Dog"),
        ("Bunny", "Bunny"),
        ("Parrot", "Parrot"),
        ("Fish", "Fish"),
        ("Other", "Other"),
    )
    name = models.CharField(max_length=30, verbose_name='Pet Name:')
    type = models.CharField(
        max_length=max([len(x) for x, _ in TYPE_CHOICES]),
        choices=TYPE_CHOICES,
    )
    date_of_birth = models.DateField(
        verbose_name='Day of Birth:',
        null=True,
        blank=True,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class PetPhoto(models.Model):
    photo = models.ImageField(validators=[validate_file_max_size], verbose_name='Pet Image:')
    tagged_pets = models.ManyToManyField(Pet, verbose_name='Tag Pets:')
    description = models.TextField(
        null=True,
        blank=True,
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
    )
    likes = models.IntegerField(
        default=0,
    )
    user = models.ForeignKey(UserModel, on_delete=CASCADE)


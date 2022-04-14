from datetime import date, datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from petstagram.helpers import BootstrapFormMixin
from petstagram.main_app.custom_validators import MaxDateValidator
from petstagram.main_app.models import Profile, Pet, PetPhoto


class CreateProfileForm(UserCreationForm, BootstrapFormMixin):
    first_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LENGTH)
    profile_picture = forms.URLField()
    date_of_birth = forms.DateField()
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_picture=self.cleaned_data['profile_picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture', 'description')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'profile_picture': forms.TextInput(attrs={'placeholder': 'Enter URL'}),
        }


class CreatePetForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        pet = super().save(commit=False)
        pet.user = self.user
        if commit:
            pet.save()
        return pet

    class Meta:
        model = Pet
        fields = ('name', 'type', 'date_of_birth')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter pet name'}),
            'date_of_birth': forms.SelectDateWidget(
                years=range(1990, datetime.now().year + 1)),
        }

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('user')  # allow checking against the missing attribute

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e.message_dict)


class EditPetForm(forms.ModelForm, BootstrapFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def clean_date_of_birth(self):
        MaxDateValidator(date.today())(self.cleaned_data['date_of_birth'])
        return self.cleaned_data['date_of_birth']

    class Meta:
        model = Pet
        exclude = ('user',)
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1990, datetime.now().year + 1)),
        }


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = PetPhoto
        fields = ('photo', 'description', 'tagged_pets')
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter description.',
                                                 'rows': 3}),
            'tagged_pets': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = PetPhoto
        fields = ('description', 'tagged_pets')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'tagged_pets': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class EditProfileForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1920, datetime.now().year)),
            'description': forms.Textarea(
                attrs={'rows': 3})
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        pets = list(self.instance.pet_set.all())
        PetPhoto.objects.filter(tagged_pets__in=pets).delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        fields = ()

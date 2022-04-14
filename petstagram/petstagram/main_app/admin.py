from django.contrib import admin

from petstagram.main_app.models import Profile, Pet, PetPhoto


class PetInlineAdmin(admin.StackedInline):
    model = Pet


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    # list_display = ('id', 'first_name', 'last_name')
    # inlines = (PetInlineAdmin,)
    pass


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'user_profile')
    pass


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    pass

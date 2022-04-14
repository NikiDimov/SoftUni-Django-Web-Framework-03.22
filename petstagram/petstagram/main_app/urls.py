from django.urls import path

from petstagram.main_app.views import like_pet_photo, \
    HomeView, \
    DashboardView, CreatePetView, EditPetView, DeletePetView, PetPhotoDetailsView, CreatePetPhotoView, \
    ProfileDetailsView, EditPetPhotoView, EditProfileView, DeleteProfileView, DeletePetPhotoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/<int:pk>', ProfileDetailsView.as_view(), name='profile'),
    path('photo/details/<int:pk>', PetPhotoDetailsView.as_view(), name='photo details'),
    path('photo/like/<int:pk>', like_pet_photo, name='like pet photo'),

    path('pet/add/', CreatePetView.as_view(), name='add pet'),
    path('pet/edit/<int:pk>', EditPetView.as_view(), name='edit pet'),
    path('pet/delete/<int:pk>', DeletePetView.as_view(), name='delete pet'),
    path('photo/add/', CreatePetPhotoView.as_view(), name='add photo'),
    path('photo/edit/<int:pk>', EditPetPhotoView.as_view(), name='edit photo'),
    path('photo/delete/<int:pk>', DeletePetPhotoView.as_view(), name='delete photo'),
    path('profile/edit/<int:pk>', EditProfileView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>', DeleteProfileView.as_view(), name='delete profile'),

]

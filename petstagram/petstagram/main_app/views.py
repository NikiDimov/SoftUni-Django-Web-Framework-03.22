from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from petstagram.accounts.models import PetstagramUser
from petstagram.main_app.forms import CreatePetForm, EditPetForm, EditProfileForm, CreatePhotoForm, EditPhotoForm
from petstagram.main_app.models import PetPhoto, Profile, Pet


class HomeView(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(ListView):
    model = PetPhoto
    template_name = 'dashboard.html'
    context_object_name = 'pet_photos'


class CreatePetView(CreateView):
    template_name = 'pet_create.html'
    form_class = CreatePetForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPetView(UpdateView):
    model = Pet
    form_class = EditPetForm
    template_name = 'pet_edit.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user_id})


class DeletePetView(DeleteView):
    model = Pet
    template_name = 'pet_delete.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user_id})


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = list(Pet.objects.filter(user_id=self.object.user_id))
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()
        total_likes = sum(pp.likes for pp in pet_photos)
        context.update({
            'total_likes': total_likes,
            'pets': pets,
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context


class EditProfileView(UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'profile_edit.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user_id})


class DeleteProfileView(DeleteView):
    model = PetstagramUser
    template_name = 'profile_delete.html'
    success_url = reverse_lazy('home')


def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()
    return redirect('photo details', pk)


def show_401_error(request):
    return render(request, '401_error.html')


class PetPhotoDetailsView(DetailView):
    model = PetPhoto
    template_name = 'photo_details.html'
    context_object_name = 'pet_photo'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tagged_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class CreatePetPhotoView(LoginRequiredMixin, CreateView):
    model = PetPhoto
    form_class = CreatePhotoForm
    template_name = 'photo_create.html'

    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPetPhotoView(UpdateView):
    model = PetPhoto
    template_name = 'photo_edit.html'
    form_class = EditPhotoForm

    def get_success_url(self):
        return reverse_lazy('photo details', kwargs={'pk': self.object.id})


class DeletePetPhotoView(DeleteView):
    model = PetPhoto
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('dashboard')

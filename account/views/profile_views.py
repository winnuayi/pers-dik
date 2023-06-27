from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from account.forms import PasswordUpdateForm, ProfileForm
from account.models import CustomUser


class ProtectedView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'redirect_to'


class ProfileView(ProtectedView):
    def get(self, request):
        context = { 'app_account_active': 'active' }
        return render(request, 'account/profile/detail.html', context)

    def post(self, request):
        # validate form khusus untuk update
        instance = get_object_or_404(CustomUser, id=request.user.id)
        form = ProfileForm(request.POST, instance=instance)

        # tampilkan notifikasi error di setiap isian
        if not form.is_valid():
            context = {
                'error_message': "Isian tidak lengkap.",
                'errors': form.errors,
                'form': form,
            }
            return render(request, 'account/profile/detail.html', context)

        form.save()

        context = {
            'notification_message': "Profil berhasil diubah.",
            'username': request.POST['username'],
            'fullname': request.POST['fullname'],
        }

        return render(request, 'account/profile/detail.html', context)


class PasswordUpdateView(ProtectedView):
    def get(self, request):
        context = { 'app_account_active': 'active' }
        return render(request, 'account/profile/change-password.html', context)

    def post(self, request):
        instance = get_object_or_404(CustomUser, id=request.user.id)
        form = PasswordUpdateForm(request.POST, instance=instance,
                                  request=request)
        # form = PasswordUpdateForm(request.POST, instance=instance)

        if not form.is_valid():
            context = {
                'message': "Wrong input",
                'errors': form.errors,
            }
            return render(request, 'account/profile/change-password.html',
                          context)

        form.save()

        context = {
            'message': "Password has been changed successfully.",
        }

        return render(request, 'account/profile/change-password.html', context)

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View


class LoginView(View):
    """
    Login ke dalam aplikasi dengan database 'default' atau external database.

    Jika ingin login menggunakan external database.
    Gunakan account.backends.ExternalModelDatabase.
    """

    REDIRECT_TO = reverse_lazy('project:home')

    def get(self, request):
        # jika sudah terautentikasi, langsung redirect dari halaman login
        # ke halaman utama
        if request.user.is_authenticated:
            return redirect(self.REDIRECT_TO)

        return render(request, 'account/login/001-workspace.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if len(username) == 0 or len(password) == 0:
            context = {
                'error_message': "Isian tidak lengkap"
            }
            return render(request, 'account/login/001-workspace.html', context)

        user = authenticate(username=username, password=password)

        # cek apakah user sudah terdaftar
        if user is None:
            context = {
                'error_message': "Kombinasi email dan password tidak cocok. Atau belum diaktivasi."
            }
            return render(request, 'account/login/001-workspace.html', context)

        login(request, user)

        return redirect(self.REDIRECT_TO)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('account:login'))

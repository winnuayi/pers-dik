from django.shortcuts import render
from django.views.generic import View


class SessionExpiresView(View):
    def get(self, request):
        return render(request, 'account/extra/session-expires.html')

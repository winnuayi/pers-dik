from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from core.helpers.paginations import Pagination
from pendidikan.models import Jabatan


class HomeView(Pagination, View):
    url = reverse_lazy('pendidikan:home')

    def get(self, request):
        page = 1
        if 'page' in request.GET:
            page = int(request.GET['page'])

        rows = 50
        if 'rows' in request.GET:
            rows = int(request.GET['rows'])

        jabatan_list = self.get_jabatan_list(request)

        paginator = Paginator(jabatan_list, rows)
        current_page = paginator.page(page)

        context = {
            # filter
            'rows': rows,

            # 'jabatan_list': jabatan_list,

            'current_page': current_page,

            # pagination
            'first_page_url': self.get_first_page_url(request, current_page),
            'previous_page_url': self.get_previous_page_url(request, current_page),
            'next_page_url': self.get_next_page_url(request, current_page),
            'last_page_url': self.get_last_page_url(request, current_page),
        }

        if 'q' in request.GET:
            context.update({ 'q': request.GET['q'] })

        return render(request, "pendidikan/home.html", context)

    def get_jabatan_list(self, request):
        q = Q()

        if 'q' in request.GET and len(request.GET['q']) > 0:
            q |= Q(nama__icontains=request.GET['q'])
            q |= Q(personil__pangkat__nama__icontains=request.GET['q'])
            q |= Q(personil__nama__icontains=request.GET['q'])
            q |= Q(personil__personil_sumber_pa__sumber_pa__nama__icontains=request.GET['q'])
            q |= Q(personil__personil_dikmilti__dikmilti__nama__icontains=request.GET['q'])
            # q |= Q(personil__personil_dikbangspes__dikbangspes__nama__icontains=request.GET['q'])

        return Jabatan.objects.filter(q)

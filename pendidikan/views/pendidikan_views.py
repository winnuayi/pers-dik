from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from core.helpers.paginations import Pagination
from pendidikan.forms import PersonilForm
from pendidikan.models import Jabatan, Korps, Pangkat, Personil


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
            # menu
            'home_active': 'active',

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
            q |= Q(personil__nrp__icontains=request.GET['q'])
            q |= Q(personil__personil_sumber_pa__sumber_pa__nama__icontains=request.GET['q'])
            q |= Q(personil__personil_dikmilti__dikmilti__nama__icontains=request.GET['q'])
            # q |= Q(personil__personil_dikbangspes__dikbangspes__nama__icontains=request.GET['q'])

        return Jabatan.objects.filter(q)


class PersonilListView(Pagination, View):
    def get(self, request):
        page = 1
        if 'page' in request.GET:
            page = int(request.GET['page'])

        rows = 50
        if 'rows' in request.GET:
            rows = int(request.GET['rows'])

        personil_list = self.get_personil_list()

        paginator = Paginator(personil_list, rows)
        current_page = paginator.page(page)


        context = {
            # menu
            'personil_active': 'active',

            'current_page': current_page,
        }
        return render(request, 'pendidikan/personil-list.html', context)

    def get_personil_list(self):
        return Personil.objects.all().order_by('nama')


class PersonilCreateView(View):
    def get(self, request):
        pangkat_list = Pangkat.objects.all().order_by('counter')
        jabatan_list = Jabatan.objects.all().order_by('nama')
        korps_list = Korps.objects.all().order_by('nama')

        context = {
            'form_title': "Tambah Personil",

            'pangkat_list': pangkat_list,
            'jabatan_list': jabatan_list,
            'korps_list': korps_list,
        }

        return render(request, 'pendidikan/personil-form.html', context)

    def post(self, request):
        context = self.get_context(request)

        form = PersonilForm(request.POST)

        if not form.is_valid():
            context = self.get_error_context(context, request, form)
            return render(request, 'pendidikan/personil-form.html', context)

        form.save()

        # TODO redirect ke update form/personil detail
        
        return render(request, 'pendidikan/personil-form.html', context)

    def get_context(self, request):
        context = {
            'form_title': 'Tambah Personil',

            # populate dropdown
            'pangkat_list': Pangkat.objects.all().order_by('counter'),
            'jabatan_list': Jabatan.objects.all().order_by('nama'),
            'korps_list': Korps.objects.all().order_by('nama'),
        }

        return context

    def get_error_context(self, context, request, form):
        context.update({
            # render feedback message di setiap field
            'errors': form.errors,

            # render global message
            'message': "Isian tidak sesuai",
        })

        # jika field nama sudah diisi, tetap tampilkan nama di placeholder
        if 'nama' in request.POST:
            context['nama'] = request.POST['nama']

        # idem
        if 'nrp' in request.POST:
            context['nrp'] = request.POST['nrp']

        # idem
        if 'tgl_lahir' in request.POST:
            context['tgl_lahir'] = request.POST['tgl_lahir']

        # convert ke integer equal operator dropdown butuh integer
        if 'pangkat' in request.POST:
            context['selected_pangkat'] = int(request.POST['pangkat'])

        # idem
        if 'jabatan' in request.POST:
            context['selected_jabatan'] = int(request.POST['jabatan'])

        # idem
        if 'korps' in request.POST:
            context['selected_korps'] = int(request.POST['korps'])
        
        if '__all__' in form.errors:
            context['message'] = form.errors['__all__'].as_text()

        return context

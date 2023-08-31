from django.urls import path

from pendidikan.views import pendidikan_views

app_name = "pendidikan"

urlpatterns = [
    ############################################################################
    # VIEW
    ############################################################################
    path('', pendidikan_views.HomeView.as_view(), name="home"),
    path('personil/', pendidikan_views.PersonilListView.as_view(),
         name='personil-list'),
    path('personil/create/', pendidikan_views.PersonilCreateView.as_view(),
         name='personil-create'),

    ############################################################################
    # API
    ############################################################################
]

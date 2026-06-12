from django.urls import path

from . import views

app_name = 'opere'

urlpatterns = [
    path('sculture/', views.opere_base_view, name='sculture'),
    path('gioielli/', views.gioielli_base_view, name='gioielli'),
    path('disegni/', views.disegni_base_view, name='disegni'),
    path('mostre/', views.mostre_list_view, name='mostre'),
    path('mostra/<slug:slug>/', views.mostra_detail_view, name='mostra_detail'),
    path('opera/<slug:slug>/', views.opera_detail_view, name='opera_detail'),
]

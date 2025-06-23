from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('general-statistics', views.index, name='general_statistics'),
    path('demand', views.index, name='demand'),
    path('geography', views.index, name='geography'),
    path('skills', views.index, name='skills'),
    path("latest_vacancies", views.latest_vacancies, name="latest_vacancies"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
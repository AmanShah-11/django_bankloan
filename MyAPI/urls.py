from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    # # path('admin', admin.site.urls),
    # path('form/', views.cxcontact, name='cxform'),
    # path('api/', include(routers.urls)),
    # path('status/', views.approvereject),
    # path('form2/', views.cxcontact, name='form'),
    path('', views.cxcontact, name='form')
]
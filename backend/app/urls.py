from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('students', views.StudentView)
# router.register('results', views.ResultView)

urlpatterns = [
    # path('', include(router.urls))
    path('students/', views.StudentView, name = 'StudentView'),
    path('login/', ObtainAuthToken.as_view()),
    path('generate/', views.Generate, name = 'Generate'),
]
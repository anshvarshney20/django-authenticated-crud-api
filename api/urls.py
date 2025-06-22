from django.urls import path
from api import views


urlpatterns = [
    path('get', views.home, name='home'),
    path('signup', views.register_user, name='signup'),
    path('signin', views.login_user, name='signin'),
    path('get/<uuid:id>/', views.home_by_Id, name='home_by_id'),
    path('update/<uuid:id>/', views.home_by_Id, name='home_by_id'),
]

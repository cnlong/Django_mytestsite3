from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('index2', views.index2),
    path('temp_vars', views.temp_var),
    path('temp_targs', views.temp_targs),
    path('temp_filter', views.temp_filter),
    path('temp_inherit', views.temp_inherit),
    path('html_escape', views.html_escape),
    path('login/', views.login),
    path('login_check', views.login_check),
    path('change_pwd', views.change_pwd),
    path('change_pwd_action', views.change_pwd_action),
    path('verify_code', views.verify_code),
    path('url_reverse', views.url_reverse),
    path('show_args/<int:a>/<int:b>', views.show_args, name='showargs'),
    path('test_reverse', views.test_reverse),
]

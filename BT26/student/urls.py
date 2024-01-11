from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('index', views.index, name='index'),
    path('test-media', views.testMedia, name='testMedia'),
    path('insert', views.insert, name='insert'),
    path('add', views.add, name='add'),
    path('delete/<str:pk>', views.remove, name='delete'),
    path('update/<str:pk>', views.update, name='update'),
    path('edit/<str:pk>', views.edit, name='edit'),
    path('send', views.send, name='send'),
    path('send-email', views.sendEmail, name='sendEmail'),
    path('send-email2', views.sendEmail2, name='sendEmail2'),
    path('check-login', views.check_login, name='check_login'),
    path('login', views.login, name='login'),
    path('thongbao', views.thongbao, name='thongbao'),
    path('accounts/profile/', views.login_success_google, name='login_success_google'),
    path('', views.main,name='main'),
    path('main/', views.mainHome, name='mainHome'),
    path('changepassword/', views.change_pass, name='changepass'), 
    path('register/', views.register, name='register'), 
    path('test-form/', views.testForm, name='testForm'), 
    path('check-test-form/', views.check_test_form, name='check_test_form'),
    path('register-with-google/', views.register_with_google, name='register_with_google'), 
    path('check-change-password/', views.check_change_password, name='check_change_password'),
    path('check-reset/<uidb64>/', views.CheckPassReset, name='check_password_reset_confirm'),
    path('form_reset_email', views.form_email_reset, name = 'form-reset-email'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView, name='password_reset_confirm'),
    path('password_reset/', views.CustomPasswordReset, name='CustomPasswordReset'),
    path('test-send-email/', views.testSendMail2, name = 'testSendMail2'),
    path('logout/', views.logout, name='logout'), 
]

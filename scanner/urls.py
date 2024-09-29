from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path("scan/", views.scan, name="scan"),
    path("target/", views.target, name="target"),
    path("report/", views.report, name="report"),
    path("notify/", views.notify, name="notify"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("vulnerability/", views.vulnerability, name="vulnerability")
]

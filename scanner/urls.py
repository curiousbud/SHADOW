from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chart", views.chart, name="chart"),
    path("empty", views.empty, name="empty"),
    path("ui_elements", views.ui_elements, name="ui_elements"),
    path("form", views.form, name="form"),
    path("tab_panel", views.tab_panel, name="tab_panel"),
    path("table", views.table, name="table"),
    path("base", views.base, name="base"),
    path("scan", views.scan, name="scan"),
    path("target", views.target, name="target"),
    path("report", views.report, name="report"),
    path("notify", views.notify, name="notify"),
    path("vulnerability", views.vulnerability, name="vulnerability")
]

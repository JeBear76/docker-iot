from django.urls import re_path
from django.urls import path, include
from django.views.generic import TemplateView
from iotApp import views
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'customers', views.CustViewSet)

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    # re_path(r'^$', views.HomePageView.as_view()),
    # url(r'^links/$', views.LinksPageView.as_view()), # simple view
    # url(r'^getcust/$',views.Customers.getCust), # simple view
    # url(r'^apitest/$',views.CalcTest), # for REST API test
]
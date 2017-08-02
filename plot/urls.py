from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^job/.*$', views.plot_job_comp_metrics),
    #url(r'^comp/.*$', views.plot_comp_metrics),
    url(r'^png/.*$', views.png_job_comp_metrics),
]

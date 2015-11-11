__author__ = 'Austin'

from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    #url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    #ex: /HiveManagement/
    url(r'^$', views.index, name='index'),
    #ex: /filter/2015-12-01/2016-01-28
    url(r'^filter/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',views.index, name='filter'),
    url(r'^field/(?P<field_id>[0-9]+)/$', views.field, name='field'),
    url(r'^pallet/(?P<pallet_id>[0-9]+)/$', views.pallet, name='pallet'),
    url(r'^analysis/', views.analysis, name='analysis'),
    url(r'^back_date/(?P<field_id>[0-9]+)/(?P<region_name>[\w\-]+)', views.add_previous_field, name='back_date')
    ]
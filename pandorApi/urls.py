from django.urls import path
#
from .views import api_overview, occasion_list, occasion_detail, occasion_create, occasion_update, occasion_delete
#

from django.conf.urls import url
from django.http import HttpResponseRedirect

from .views import ImportantOccasionCreate, ImportantOccasionUpdate, ImportantOccasionDelete

app_name = 'api'
urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('new/'), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', ImportantOccasionUpdate.as_view(), name='update'),
    url(r'^new/$', ImportantOccasionCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ImportantOccasionDelete.as_view(), name='delete'),

    # This is probably more applicable in the root urls
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

urlpatterns += [

    path('', api_overview, name="api_overview"),
    path('occasion-list/', occasion_list, name="occasion_list"),
    path('occasion_detail/<str:pk>/', occasion_detail, name="occasion_detail"),
    path('occasion-create/', occasion_create, name="occasion_create"),
    path('occasion-update/<str:pk>/', occasion_update, name="occasion_update"),
    path('occasion-delete/<str:pk>/', occasion_delete, name="occasion_delete"),

]
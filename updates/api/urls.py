from django.conf.urls import url


from .views import (
    UpdateModelAPIDetailView,
    UpdateModelAPIListView

)


urlpatterns = [
    url(r'^$', UpdateModelAPIListView.as_view()), #api/updates/
    url(r'^(?P<id>\d+)/$', UpdateModelAPIDetailView.as_view())
]
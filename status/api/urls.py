from django.conf.urls import url, include
from django.contrib import admin
from .views import StatusAPIView, StatusAPIDetailView

urlpatterns = [
    url(r'^$', StatusAPIView.as_view(), name='list'),
    url(r'^(?P<id>\d+)/$', StatusAPIDetailView.as_view(), name='detail')
]

# /api/status/ -> List
# /api/status/create -> Create
# /api/status/12/ -> Detail
# /api/status/12/update/ -> Update
# /api/status/12/delete/ -> Delete

# End With

# /api/status/ -> list -> CRUD
# /api/status/ -> Detail -> CRUDS

# Final

# /api/status/ -> CRUD & LS
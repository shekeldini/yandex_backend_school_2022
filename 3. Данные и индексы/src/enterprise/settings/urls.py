from django.urls import path
from enterprise.users.views import UsersV1ListViewSet, UsersV2ListViewSet, UsersV3ListViewSet

urlpatterns = [
    path('v1/users/', UsersV1ListViewSet.as_view({'get': 'list'})),
    path('v2/users/', UsersV2ListViewSet.as_view({'get': 'list'})),
    path('v3/users/', UsersV3ListViewSet.as_view({'get': 'list'})),
]

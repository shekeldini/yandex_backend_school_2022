from django.db.models.functions import Concat
from django.db.models import F, Value, CharField
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import CursorPagination

from enterprise.users.models import User, Job, Company
from enterprise.users.serializers import CompanySerializer, JobSerializer, UserSerializer


class UsersV1ListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = CursorPagination
    queryset = User.objects.all()

    filter_backends = (filters.SearchFilter,)

    search_fields = (
        "=id",
        "^first_name",
        "^last_name",
    )


class UsersV2ListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = CursorPagination  # perfomance issue SHCP-5191
    queryset = User.objects.all().order_by("last_name")

    filter_backends = (filters.SearchFilter,)

    search_fields = (
        "=id",
        "first_name",
        "last_name",
        "^phone_number",
        "email",
    )


class UsersV3ListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = CursorPagination  # perfomance issue SHCP-5191
    queryset = User.objects.annotate(
        fio=Concat(
            F('last_name'),
            Value(' '),
            F('first_name'),
            Value(' '),
            F('second_name'),
            output_field=CharField(),
        ),
    ).all().order_by("fio")

    filter_backends = (filters.SearchFilter,)

    search_fields = (
        "=id",
        "^first_name",
        "last_name",
        "fio",
        "phone_number",
        "email",
        "company__title",
        "job__title",
    )


class CompaniesListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = CompanySerializer
    pagination_class = CursorPagination  # perfomance issue SHCP-5191
    queryset = Company.objects.all()

    filter_backends = (filters.SearchFilter,)

    search_fields = (
        "=id",
        "^title",
        "address",
    )


class JobsListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = JobSerializer
    pagination_class = CursorPagination  # perfomance issue SHCP-5191
    queryset = Job.objects.all()

    filter_backends = (filters.SearchFilter,)

    search_fields = (
        "=id",
        "^title",
    )

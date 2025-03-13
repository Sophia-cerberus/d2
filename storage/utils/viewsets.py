from rest_framework import mixins
from rest_framework.viewsets import ViewSetMixin
from utils.generics import GenericAPIView
from utils.pagination import Pagination
from rest_framework.request import Request
from types import FunctionType, MethodType
from utils.exceptions import APIException

from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError, Http404):
        raise APIException(message='该对象不存在或者无访问权限')
    

class GenericViewSet(ViewSetMixin, GenericAPIView):
    extra_filter_backends = []
    pagination_class = Pagination

    def handle_logging(self, request: Request, *args, **kwargs):
        view_loggers = self.get_view_loggers(request, *args, **kwargs)
        for view_logger in view_loggers:
            handle_action = getattr(view_logger, f'handle_{self.action}', None)
            if handle_action and isinstance(handle_action, (FunctionType, MethodType)):
                handle_action(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        serializer = serializer_class(*args, **kwargs)
        serializer.request = self.request
        return serializer

    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def initial(self, request, *args, **kwargs):
        """
        重写initial方法
        (1)新增action的权限校验
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        super().initial(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass
import logging
from types import FunctionType, MethodType

from rest_framework.request import Request
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class CustomAPIView(APIView):
    """
    继承、增强DRF的APIView
    """
    view_logger_classes = ()

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get_view_loggers(self, request: Request, *args, **kwargs):
        logger_classes = self.view_logger_classes or []
        if not logger_classes:
            return []
        view_loggers = [logger_class(view=self, request=request, *args, **kwargs) for logger_class in logger_classes]
        return view_loggers

    def handle_logging(self, request: Request, *args, **kwargs):
        view_loggers = self.get_view_loggers(request, *args, **kwargs)
        method = request.method.lower()
        for view_logger in view_loggers:
            view_logger.handle(request, *args, **kwargs)
            logger_fun = getattr(view_logger, f'handle_{method}', f'handle_other')
            if logger_fun and isinstance(logger_fun, (FunctionType, MethodType)):
                logger_fun(request, *args, **kwargs)

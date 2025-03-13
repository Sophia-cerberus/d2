from django.http.response import JsonResponse
from rest_framework.response import Response


class SuccessResponse(Response):

    def __init__(self, data=None, msg='success', code=200, status=None, template_name=None, headers=None, 
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "message": msg,
            "status": 'success'
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):

    def __init__(self, data=None, msg='error', code=400, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "message": msg,
            "status": 'error'
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class AuthResponse(Response):

    def __init__(self, data=None, msg='error', code=401, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "message": msg,
            "status": 'error'
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class NotFoundResponse(Response):

    def __init__(self, data=None, msg='error', code=404, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "message": msg,
            "status": 'error'
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)
        
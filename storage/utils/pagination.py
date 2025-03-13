
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination, _positive_int

from utils.response import SuccessResponse


class Pagination(PageNumberPagination):
    """
    标准分页器
    """
    page_size_query_param = 'pageSize'
    other_page_size_query_param = []
    # other_page_size_query_param = ['pageSize', ]

    page_query_param = "pageNum"
    other_page_query_param = []
    # other_page_query_param = ['currentPage', 'pageNum']
    max_page_size = 1000
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        page_num = request.query_params.get(self.page_query_param)
        # 判断，如果 pageNum 为all 则取消分页返回所有
        if page_num == 'all':
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_next_link(self):
        return super().get_next_link()

    def get_previous_link(self):
        return super().get_previous_link()

    def get_page_size(self, request):
        """
        获取页大小
        :param request:
        :return:
        """
        if self.other_page_size_query_param:
            for param_name in self.other_page_size_query_param:
                if param_name in request.query_params:
                    return _positive_int(
                        request.query_params[param_name],
                        strict=True,
                        cutoff=self.max_page_size
                    )
        return super().get_page_size(request)

    def get_page_num(self, request):
        """
        获取页码
        :param request:
        :return:
        """
        if self.other_page_query_param:
            for param_name in self.other_page_query_param:
                if param_name in request.query_params:
                    return _positive_int(request.query_params[param_name], strict=True)
        page_num = request.query_params.get(self.page_query_param, 1)
        return _positive_int(page_num, strict=True)

    def get_paginated_response(self, data, search_fields=''):
        return SuccessResponse(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

import urllib

from django.core.paginator import EmptyPage, Paginator


class Pagination:
    """
    Class ini menggunakan django pagination dengan mekanisme render di server.
    """

    # override url di setiap Views yang menggunakan class helper ini
    url = None

    def get_first_page_url(self, request, current_page):
        # transform dari QueryDict menjadi dictionary
        params = request.GET.dict()

        # update page number berikutnya
        params['page'] = 1

        return '{}?{}'.format(self.url,
                              urllib.parse.urlencode(params, True))

    def get_previous_page_url(self, request, current_page):
        # transform dari QueryDict menjadi dictionary
        params = request.GET.dict()

        # update page number berikutnya
        try:
            params['page'] = current_page.previous_page_number()
        except EmptyPage:
            return '#'

        return '{}?{}'.format(self.url,
                              urllib.parse.urlencode(params, True))

    def get_next_page_url(self, request, current_page):
        # transform dari QueryDict menjadi dictionary
        params = request.GET.dict()

        # update page number berikutnya
        try:
            params['page'] = current_page.next_page_number()
        except EmptyPage:
            return '#'

        return '{}?{}'.format(self.url,
                              urllib.parse.urlencode(params, True))

    def get_last_page_url(self, request, current_page):
        # transform dari QueryDict menjadi dictionary
        params = request.GET.dict()

        # update page number berikutnya
        params['page'] = current_page.paginator.num_pages

        return '{}?{}'.format(self.url,
                              urllib.parse.urlencode(params, True))


class FilterPagination:
    """
    Class ini menggunakan django pagination dengan mekanisme render di server.
    """

    # override url di setiap Views yang menggunakan class helper ini
    url = None

    def get_first_page_url(self, request, current_page):
        # update page number berikutnya
        params = request.GET.copy()
        params['page'] = 1

        return '{}?{}'.format(self.url, params.urlencode())

    def get_previous_page_url(self, request, current_page):
        # update page number berikutnya
        try:
            params = request.GET.copy()
            params['page'] = current_page.previous_page_number()
        except EmptyPage:
            return '#'

        return '{}?{}'.format(self.url, params.urlencode())

    def get_next_page_url(self, request, current_page):
        # update page number berikutnya
        try:
            params = request.GET.copy()
            params['page'] = current_page.next_page_number()
        except EmptyPage:
            return '#'

        return '{}?{}'.format(self.url, params.urlencode())

    def get_last_page_url(self, request, current_page):
        # update page number berikutnya
        params = request.GET.copy()
        params['page'] = current_page.paginator.num_pages

        return '{}?{}'.format(self.url, params.urlencode())

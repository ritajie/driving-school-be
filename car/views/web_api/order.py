from django.views.generic import View


class OrderListView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class OrderOneView(View):
    def patch(self, request, order_id: int):
        pass

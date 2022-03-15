from django.views.generic import View


class OrderUsageListView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class OrderUsageOneView(View):
    def patch(self, request, order_usage_id: int):
        pass

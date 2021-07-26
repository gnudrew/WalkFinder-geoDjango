from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse

# Create your views here.
class JSONResponseMixin:
    """
    A mixin that can used to render a JSON response.
    """
    def render_to_json_response(self, context, **kwargs):
        return JsonResponse(self.get_data(context),**kwargs)

    def get_data(self, context):
        # Here we should do context handling to ensure arbitrary objects in `context` are JSON serializable
        return context

class SinglePageView(TemplateView):
    template_name='single_page.html'

class RouteGenView(JSONResponseMixin, FormView):
    def post():
        """Receive location and routegen parameters, calculate a route, passed back as JSON"""
        pass
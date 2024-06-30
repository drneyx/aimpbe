from django.shortcuts import render
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your context data here
        context['title'] = 'Dashboard'
        context['data'] = {
            # Add any data you want to pass to the template
            'example_data': 'This is an example data.'
        }
        return context
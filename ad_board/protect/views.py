from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexViews(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

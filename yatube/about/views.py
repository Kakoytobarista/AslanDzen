from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.views.generic.base import TemplateView


@method_decorator(cache_page(10 * 5), name='dispatch')
class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'
    title = 'About Author'


@method_decorator(cache_page(10 * 5), name='dispatch')
class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
    title = 'Tech'

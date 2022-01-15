from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'
    title = 'About Author'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
    title = 'Tech'

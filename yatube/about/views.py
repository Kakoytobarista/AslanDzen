from django.views.generic.base import TemplateView
from django.http import HttpRequest, HttpResponse
from typing import Any


class AboutAuthorView(TemplateView):
    """
    View for the 'About Author' page.

    Attributes:
        template_name (str): The template file to render.
        title (str): The title of the page.
    """

    template_name: str = 'about/author.html'
    title: str = 'About Author'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Cached dispatch method for the view."""
        return super().dispatch(request, *args, **kwargs)


class AboutTechView(TemplateView):
    """
    View for the 'About Tech' page.

    Attributes:
        template_name (str): The template file to render.
        title (str): The title of the page.
    """

    template_name: str = 'about/tech.html'
    title: str = 'Tech'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Cached dispatch method for the view."""
        return super().dispatch(request, *args, **kwargs)

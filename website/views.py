from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse

from website.forms import PlayerForm, Player
from website.models import PartyImage
from website.tasks import image_processor

PAGE_SIZE = 6


class Index(TemplateView):
    template_name = "index.html"


class Gallery(TemplateView):
    template_name = "gallery.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        """Post endpoint for uploading images"""

        for image in request.FILES.getlist("images"):
            db_image = PartyImage.objects.create(image=image)
            image_processor.delay(db_image.id)

        return HttpResponse()

    @classmethod
    def infinite_scroll(cls, request, *args, **kwargs):
        """Separate endpoint for the infinite scroll feature"""
        if request.method != "GET":
            return HttpResponseNotAllowed(["GET"])

        if not request.headers.get("x-inline", None):
            return redirect(reverse("gallery"))

        page: int = kwargs.get("page", 0)

        start = page * PAGE_SIZE
        end = start + PAGE_SIZE

        items = list(PartyImage.objects.order_by("-created_on")[start:end])

        context = {"items": items}
        response = render(request, "parts/partyimage.html", context)
        response["x-has-more"] = len(items) == PAGE_SIZE
        return response

class NewPlayer(CreateView):
    template_name = "new_player.html"
    form_class = PlayerForm
    success_url = "/player/{id}"

class PlayerView(TemplateView):
    template_name = "player.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = Player.objects.get(id=self.kwargs['id'])
        return context

class NewGame(TemplateView):
    template_name = "new_game.html"


class Scores(TemplateView):
    template_name = "scores.html"

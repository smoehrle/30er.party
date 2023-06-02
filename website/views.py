from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Sum, Count

from website.forms import PlayerForm, Player, PlayGameForm
from website.models import PartyImage, PlayResult, Player
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

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        if 'x-player-name' not in self.request.COOKIES:
            # Set cookie with player name but only for the first player a user is creating
            response.set_cookie('x-player-name', context['player'].name)
        return response

class NewGame(CreateView):
    template_name = "new_play.html"
    form_class = PlayGameForm
    success_url = "/"


class Scores(TemplateView):
    template_name = "scores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the number of wins and loses and points per player
        results = PlayResult.objects.values("player", "is_winner").annotate(total_points=Sum("points"), num=Count("points"))

        # Mapping: player.id -> [playername, wins, games, points, is_current_user]
        current_user = self.request.COOKIES.get('x-player-name', None)
        players = {player.id: [player.name,0,0,0,False] for player in Player.objects.all()}
        for result in results:
            player_id = result["player"]
            if result["is_winner"]:
                players[player_id][1] += result["num"]
            # Total games
            players[player_id][2] += result["num"]
            # Total points
            players[player_id][3] += result["total_points"]

            # Mark as current user
            if players[player_id][0] == current_user:
                players[player_id][4] = True

        context["players"] = sorted(players.values(), key=lambda x: x[3], reverse=True)
        return context

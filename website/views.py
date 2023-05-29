from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse

from website.models import PartyImage

class Index(TemplateView):
    template_name = "index.html"

class Gallery(TemplateView):
    template_name = "gallery.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        """Post endpoint for uploading images"""

        for image in request.FILES.getlist("images"):
            db_image = PartyImage.objects.create(image=image)
            # TODO: Thumbnail
            # image_processor.delay(db_image.id)

        return HttpResponse()

class NewPlayer(TemplateView):
    template_name = "new_player.html"

class NewGame(TemplateView):
    template_name = "new_game.html"

class Scores(TemplateView):
    template_name = "scores.html"
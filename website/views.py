from django.views.generic import TemplateView

class Index(TemplateView):
    template_name = "index.html"

class Gallery(TemplateView):
    template_name = "gallery.html"

class NewPlayer(TemplateView):
    template_name = "new_player.html"

class NewGame(TemplateView):
    template_name = "new_game.html"

class Scores(TemplateView):
    template_name = "scores.html"
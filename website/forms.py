from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from website.models import Player, PlayGame


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'


class PlayGameForm(ModelForm):
    participants = ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True)
    class Meta:
        model = PlayGame
        fields = '__all__'

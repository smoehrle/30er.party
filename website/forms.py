from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from website.models import Player, PlayGame
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout


class CustomPlayerSelect(Field):
    """"""

    template = "parts/custom_player_select.html"


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
        fields = ['game', 'participants']

    @property
    def helper(self):  # pylint: disable=missing-function-docstring
        helper = FormHelper()
        helper.form_tag = False
        helper.layout = Layout(
            Field("game"),
            CustomPlayerSelect("participants"),
        )

        return helper

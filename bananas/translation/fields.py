from django.forms import ChoiceField

from bananas.translation.utils import get_languages


class LanguageField(ChoiceField):

    def __init__(self, required=True, widget=None,
                 label=None, initial=None, help_text='', *args, **kwargs):

        languages = get_languages()

        choices = (
            lambda: [(lang['language'], lang['name']) for lang in languages])

        super(LanguageField, self).__init__(
            choices=choices, required=required, widget=widget, label=label,
            initial=initial, help_text=help_text, *args, **kwargs
        )

from django import forms
from applications.brandcolors.models import Fabric
from django.forms import ModelForm

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _, ugettext
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.layout import Layout, Fieldset, Submit, Button

from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper

class HexcodeForm(forms.Form):
    hexcode = forms.CharField(widget = forms.HiddenInput(), label='hexcode', max_length=100)

class FabricForm(ModelForm):
    class Meta:
        model = Fabric
        fields = ['picture']

    def __init__(self, *args, **kwargs):
        super(FabricForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Fabric form"),
                layout.Field("picture", css_class="input-block-level", rows="3"),
            ),
            # forms.ChoiceField('country', choices=self.country, required=True),
            bootstrap.FormActions(
                layout.Submit("submit", _("Save"), css_class="btn-primary"),
                layout.Button(
				'cancel', 'Cancel',
				css_class="btn-xs", style='display:block',
				onclick="location.href='%s'" % reverse('brandcolors:homepage')),
            )
        )

from django import forms
from applications.startupconfort.models import CartItem, ShippingAddress
from django.forms import ModelForm

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _, ugettext
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.layout import Layout, Fieldset, Submit, Button

from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper

class BrainTreeFrom(forms.Form):
    [...]
    def __init__(self, *args, **kwargs):
        super(BrainTreeFrom, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'like_website',
                'favorite_number',
                'favorite_color',
                'favorite_food',
                'notes'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class CartItemQuantityForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
    """
    showoff = forms.CharField(
        label="showoff",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'whadiyabi',
            'class': 'form-control',
        }))
    photo = forms.ImageField(
        label="Photo",
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }))
    """
    def __init__(self, *args, **kwargs):
        super(CartItemQuantityForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Update the Quantity of Item"),
                layout.Field("quantity", css_class="input-block-level", rows="3"),
            ),
            bootstrap.FormActions(
                layout.Submit("submit", _("Update"), css_class="btn-primary"),
                layout.Button(
				'cancel', 'Cancel',
				css_class="btn-xs", style='display:block',
				onclick="location.href='%s'" % reverse('startupconfort:my_shopping_cart')),
            )
        )



class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['telephone', 'country',
				'shipping_address', 'customer_name',
				'telephone', 'billing_email', 'city', 'postal_code', 'state']

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Shipping Address form"),
                layout.Field("customer_name", css_class="input-block-level", rows="3"),
                layout.Field("shipping_address", css_class="input-block-level", rows="8"),
                layout.Field("city", css_class="input-block-level", rows="8"),
                layout.Field("postal_code", css_class="input-block-level", rows="8"),
                layout.Field("state", css_class="input-block-level", rows="8"),
                layout.Field("country", css_class="input-block-level", rows="3"),
				layout.Field("telephone", css_class="input-block-level", rows="3"),
                layout.Field("billing_email", css_class="input-block-level", rows="3"),
            ),
            # forms.ChoiceField('country', choices=self.country, required=True),
            bootstrap.FormActions(
                layout.Submit("submit", _("Save"), css_class="btn-primary"),
                layout.Button(
				'cancel', 'Cancel',
				css_class="btn-xs", style='display:block',
				onclick="location.href='%s'" % reverse('startupconfort:my_shopping_cart')),
            )
        )

from rest_framework import serializers
from rest_framework.reverse import  reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group, Permission,ContentType
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from rest_framework.serializers import (CharField, DateField, ModelSerializer,
                                        PrimaryKeyRelatedField)

#from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from applications.startupconfort.models import Startup
from applications.startupconfort.models import StartupProduct
from applications.startupconfort.models import StartupColor
from applications.startupconfort.models import StartupProductImage
from applications.startupconfort.models import StartupShopppingCart
from applications.startupconfort.models import Cart, CartItem

# HyperlinkedModelSerializer
class StartupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Startup
        exclude = ()
        fields = ('created', 'modified','title',
                            'slug', 'brand_url', 'source_url')

class StartupColorSerializer(serializers.ModelSerializer):

    #startup = StartupSerializer()
    class Meta:
        model = StartupColor
        fields = ('created', 'startup', 'color')

class StartupProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartupProduct
        fields = ('id', 'created', 'modified','startup',
                   'title','shortdesc',
                            'slug','price', 'quantity')

class StartupProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartupProductImage
        fields = ('created', 'modified','product', 'picture', 'color')

class StartupShopppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartupShopppingCart
        fields = ('created', 'modified',
                            'owner', 'product','color', 'quantity',
                            'startup', 'total_amount',
                            'shipping_address', 'customer_name',
                            'cart_slug')


class ErrorToString(object):

    @property
    def errors_to_text(self):
        assert isinstance(self, serializers.Serializer)
        errors_list = []
        for field, field_errors in self.errors.items():
            if not field_errors:
                continue
            errors_list.append('{}: {}'.format(field, field_errors[0]))
        text = ' '.join(errors_list)
        return text

#
# class PhoneSerializer(serializers.Serializer, ErrorToString):
#     phone = PhoneNumberField()







class AddItemToCartSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)


class RemoveItemFromCartSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    type = serializers.IntegerField()


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.Serializer):
    # customer = CustomerSerializer()
    items = CartItemSerializer(many=True)

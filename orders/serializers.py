from rest_framework.serializers import ModelSerializer
from social.models import Order, OrderItems


class OrderSerializer(ModelSerializer):
    class Meta:
        model=Order
        fields=['order_id', 'buyer', 'address', "price"]
    
    # def create(self, validated_data):
        
from rest_framework import serializers

from users.models import Payments, User, Subscription



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
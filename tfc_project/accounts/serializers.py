from rest_framework import serializers
from accounts.models import CustomUser, Card, Payment
from datetime import date
from dateutil import relativedelta


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": f"Password must be at least 8 characters."
        }
    )

    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": f"Password must be at least 8 characters."
        }
    )

    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'password', 'password2', 'email', 'phone_num', 'avatar',
                  'first_name', 'last_name', 'is_subscribed', 'pmt_option']

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_num=validated_data["phone_num"],
            avatar=validated_data["avatar"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_num', 'billing_addr', 'expires_at', 'cvv',
                  'holder']

    def validate(self, data):
        if data["expires_at"] < date.today():
            raise serializers.ValidationError("This card has expired. "
                                              "Please use another one.")
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


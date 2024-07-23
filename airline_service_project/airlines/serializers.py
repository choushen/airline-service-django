from rest_framework import serializers
from .models import *

# Serializer for the Flight model
class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ("__all__")


# Serializer for the passenger model
class PassengerSerailzier(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = ("__all__")


# Serializer for the Booking model
class BookingSerializer(serializers.ModelSerializer):

    passengers = PassengerSerailzier(many=True)

    class Meta:
        model = Booking
        fields = ("flight_id", "passengers")


# Serializer for the PaymentProvider model
class PaymentProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentProvider
        fields = ("pay_provider_id", "pay_provider_name")


# Serializer for the Invoice model
class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ("__all__")

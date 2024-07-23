# Importing from Django framework
from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Importing from Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import string, random, datetime

# Importing models and class serializers from the sis app folderpy
from .models import *
from .serializers import *


# Lists all flights
class FindFlight(APIView):

    def get(self, request):

        requestInfo = request.data

        flights = Flight.objects.filter(dep_airport=requestInfo['dep_airport'], dest_airport=requestInfo['dest_airport']
                                        , dep_datetime__startswith=requestInfo['dep_datetime'])

        serializer = FlightSerializer(flights, many=True)

        if serializer.data != []:
            # Specifying that there are many users to return so it doesn't return one JSON object
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            return Response("There are no flights for the given request criteria...", status=status.HTTP_503_SERVICE_UNAVAILABLE)

class BookFlight(APIView):

    def post(self, request):

        print("Request Received")
        serializer = BookingSerializer(data=request.data)
        flight_id = request.data['flight_id']

        if serializer.is_valid():

            # Updating the flight id in the data property
            serializer.data['flight_id'] = flight_id

            # Using the flight ID to obtain the correct flight
            flight = Flight.objects.get(flight_id=flight_id)
            # print(flight)

            # hold_time = models.DateTimeField()

            # Defining other fields
            # Default hold time of 30 minutes
            todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')
            bookingHoldTime = todaysDate + " 00:30:00"
            bookingStatus = "ON_HOLD"
            bookingNumber = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            passengerArray = serializer.data['passengers']


            passengerObjectArray = []
            numberOfPassengers = 0

            for person in passengerArray:
                numberOfPassengers += 1

                passenger = Passenger.objects.create(first_name=person.pop('first_name'), surname=person.pop('surname'),
                                                     email=person.pop('email'), phone_number=person.pop('phone_number'))
                passengerObjectArray.append(passenger)

            # Calculating the total cost
            flight_price = Flight.objects.get(flight_id=request.data['flight_id']).price
            tot_price = flight_price * numberOfPassengers
            print("This is total price: ", tot_price)

            # Creating the booking object
            bookingObject = Booking.objects.create(booking_num=bookingNumber,flight_id=flight,
                                                   booked_seats=numberOfPassengers, status=bookingStatus,
                                                   hold_time=bookingHoldTime)


            # print(passengerArray)

            # Passing the passenger array to the booking object
            bookingObject.passengers.set(passengerObjectArray)

            # Saving the booking object
            bookingObject.save()

            # serializer.save()
            return Response({'booking_num':bookingNumber, 'status':bookingStatus, 'tot_price':tot_price}, status=status.HTTP_201_CREATED)
        else:
            print("error 400")
            print("errors")
            print("error messages")
            serializer.error_messages
            return Response("Booking could not be completed as here are no available seats", status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PaymentMethods(APIView):

    def get(self, request):
        providers = PaymentProvider.objects.all()
        # Specifying that there are many providers to return so it doesn't return one JSON object
        serializer = PaymentProviderSerializer(providers, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("There are no payment providers for the given request criteria...", status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PayForBooking(APIView):

    def post(self, request):

        payProviderId = request.data['pay_provider_id']
        bookingNum = request.data['booking_num']

        paymentProvider = PaymentProvider.objects.get(pay_provider_id=payProviderId)
        bookingObject = Booking.objects.get(booking_num=bookingNum)

        invoice_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        airline_reference_number = random.randint(10000, 90000)
        provider_reference_number = random.randint(10000, 90000)
        # booking_num = bookingNum
        amount = bookingObject.flight_id.price * bookingObject.booked_seats
        # print(amount)
        payment_status = True
        electronic_stamp = "aaaaa00000"

        # Building the invoice object
        request.data['invoice_id'] = invoice_id
        request.data['airline_reference_number'] = airline_reference_number
        request.data['provider_reference_number'] = provider_reference_number
        # serializer.data['booking_num']
        request.data['amount'] = float(amount)
        request.data['payment_status'] = payment_status
        request.data['electronic_stamp'] = electronic_stamp


        serializer = InvoiceSerializer(data=request.data)

        pay_provider_id = request.data['pay_provider_id']
        del request.data['pay_provider_id']
        # print(serializer, " tis sis erere")

        if serializer.is_valid():

            # Creating the booking object
            invoiceObject = Invoice.objects.create(invoice_id=invoice_id,
                                                   airline_reference_number=airline_reference_number,
                                                   provider_reference_number=provider_reference_number,
                                                   booking_num=bookingNum,
                                                   amount=amount, payment_status=payment_status,
                                                   electronic_stamp=electronic_stamp)
            # Saving the booking object
            invoiceObject.save()

            # print(request.data)
            serializer = InvoiceSerializer(data=request.data)

            return Response({'pay_provider_id': pay_provider_id, 'invoice_id': invoice_id,
                             'booking_num': bookingNum, 'url': paymentProvider.url},
                            status=status.HTTP_201_CREATED)
        else:
            serializer.error_messages
            serializer.errors
            return Response("Unable to process payment at this time...",
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


class FinalizeBooking(APIView):

    def post(self, request):

        print(request.data)
        pay_provider_id = request.data['pay_provider_id']
        del request.data['pay_provider_id']

        booking = Booking.objects.filter(booking_num=request.data['booking_num']).first()
        invoice = Invoice.objects.filter(booking_num=request.data['booking_num']).first()

        invoice.electronic_stamp = request.data['electronic_stamp']
        booking.status = "CONFIRMED"

        booking.save()
        invoice.save()

        # # Building the invoice object
        request.data['invoice_id'] = invoice.invoice_id
        request.data['airline_reference_number'] = invoice.airline_reference_number
        request.data['provider_reference_number'] = invoice.provider_reference_number
        request.data['amount'] = invoice.amount
        request.data['payment_status'] = invoice.payment_status
        request.data['electronic_stamp'] = invoice.electronic_stamp

        serializer = InvoiceSerializer(data=request.data)
        # print(request.data)
        if serializer.is_valid():

            return Response({'booking_num': booking.booking_num, 'booking_status': booking.status},
                            status=status.HTTP_201_CREATED)
        else:
            serializer.error_messages
            serializer.errors
            return Response("Unable to finalize payment at this time...",
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)


class BookingStatus(APIView):

    def get(self, request):
        # Specifying that there are many providers to return so it doesn't return one JSON object
        booking_num = request.data['booking_num']

        booking = Booking.objects.get(booking_num=booking_num)

        if booking:

            booking_status = booking.status

            flight_num = booking.flight_id.flight_num
            dep_airport = booking.flight_id.dep_airport
            dest_airport = booking.flight_id.dest_airport
            dep_datetime = booking.flight_id.dep_datetime
            arr_datetime = booking.flight_id.arr_datetime
            duration = booking.flight_id.duration

            return Response({"booking_num": booking_num, "booking_status": booking_status,
                             "flight_num": flight_num, "dep_airport": dep_airport, "dest_airport": dest_airport,
                             "dep_datetime": dep_datetime, "arr_datetime": arr_datetime, "duration": duration,
                             }, status=status.HTTP_200_OK)
        else:
            return Response("Unable to display booking status at this time...", status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CancelBooking(APIView):

    def post(self, request):

        booking = Booking.objects.get(booking_num=request.data['booking_num'])

        if booking:

            booking.status = "CANCELLED"
            booking.save()

            return Response({"booking_num": booking.booking_num, "booking_status": booking.status}, status=status.HTTP_200_OK)
        else:
            return Response("Unable to display booking status at this time...", status=status.HTTP_503_SERVICE_UNAVAILABLE)




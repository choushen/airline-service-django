from django.db import models


# Unique ID add already added behind the scenes
class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=100)
    tail_number = models.CharField(max_length=30, unique=True)
    number_of_seats = models.IntegerField()

    def __str__(self):
        return self.aircraft_type + ' - ' + self.tail_number + ' - ' + str(self.number_of_seats)


class Airport(models.Model):
    airport_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    time_zone = models.CharField(max_length=50)

    def __str__(self):
        return self.airport_name + ' - ' + self.country + ' - ' + self.time_zone

class Flight(models.Model):
    flight_id = models.CharField(max_length=50, unique=True)
    flight_num = models.CharField(max_length=50)
    dep_airport = models.CharField(max_length=100)
    dest_airport = models.CharField(max_length=100)
    dep_datetime = models.DateTimeField()
    arr_datetime = models.DateTimeField()
    duration = models.TimeField()
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_flex = models.BooleanField(default=False)

    def __str__(self):
        return self.flight_id + ' - ' + self.flight_num + ' - ' + self.dep_airport + ' - ' + self.dest_airport \
        + str(self.dep_datetime) + ' - ' + str(self.dep_datetime) + ' - ' + str(self.arr_datetime) \
        + str(self.duration) + ' - ' + str(self.price) + ' - ' + str(self.is_flex)


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name + ' - ' + self.surname + ' - ' + self.email + ' - ' + self.phone_number


class Booking(models.Model):
    booking_num = models.CharField(max_length=10, unique=True)
    flight_id = models.ForeignKey('Flight', on_delete=models.CASCADE)
    booked_seats = models.IntegerField()
    passengers = models.ManyToManyField(Passenger)
    status = models.CharField(max_length=15)
    hold_time = models.DateTimeField()

    def __str__(self):
        return self.booking_num


class PaymentProvider(models.Model):
    pay_provider_id = models.CharField(max_length=10)
    pay_provider_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    account_number = models.IntegerField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.pay_provider_id + ' - ' + self.pay_provider_name + ' - ' + self.url + ' - ' + str(self.account_number) + ' - ' \
        + self.username + ' - ' + self.password


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=10)
    airline_reference_number = models.IntegerField()
    provider_reference_number = models.IntegerField()
    booking_num = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    electronic_stamp = models.CharField(max_length=15)

    def __str__(self):
        return str(self.airline_reference_number) + ' - ' + str(self.provider_reference_number) + ' - ' + \
        str(self.booking_num) + ' - ' + str(self.amount)+ ' - ' + str(self.payment_status) + ' - ' + \
        self.electronic_stamp










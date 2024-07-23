#
# A client for accessing an airline booking API
# @ Author: Jacob McKenzie
#

# Imports
import requests
import json

#1) Find Flight: GET method

# Defining the endpoint URL and the payload
findFlightEndpoint = 'http://127.0.0.1:8000/api/findflight/'
findFlightPayload = {"dep_airport":"New York JFK", "dest_airport":"London Heathrow LHR", "dep_datetime":"2018-05-10", "num_passengers":"1", "is_flex":"0"}

# Creating the request
request_1 = requests.get(findFlightEndpoint, json=findFlightPayload)

# Printing the result
print("1) Find Flight")
print("Payload: ")
print(findFlightPayload)
print("API Response: ")
print(request_1.text)
print("Status Code: " + str(request_1.status_code))

# Converting the request to JSON
data  = json.loads(request_1.text)


print("1) List of Available Flights:")
for flight in data:
    print("______________________________________________")
    print("Flight ID: " + flight["flight_id"] )
    print("Flight Number: " + flight["flight_num"] )
    print("Depature Airport: " + flight["dep_airport"] )
    print("Destination Airport: " + flight["dest_airport"] )
    print("Depature DateTime: " + flight["dep_datetime"] )
    print("Arrival DateTime: " + flight["arr_datetime"] )
    print("Flight Duration: " + flight["duration"] )
    print("Seat Price: " + flight["price"] )
    print("______________________________________________")
print("\n\n")

# 2) Book Flight: POST method

bookFlightEndpoint = 'http://127.0.0.1:8000/api/bookflight/'
bookFlightPayload = {"flight_id":"01", "passengers":[{"first_name":"John", "surname":"Doe", "email":"sc15jd@mail.com", "phone_number":"07000000000"},{"first_name":"Jane", "surname":"Smith", "email":"sc15js@mail.com", "phone_number":"07000000000"}]}

# Creating the request
request_2 = requests.post(bookFlightEndpoint, json=bookFlightPayload)

# Printing the result
print("2) Booking Flight")
print("Payload: ")
print(bookFlightPayload)
print("API Response: ")
print(request_2.text)
print("Status Code: " + str(request_2.status_code))
print("\n\n")


# 3) Payment Methods: GET method
paymentMethodsEndpoint = 'http://127.0.0.1:8000/api/paymentmethods/'

# Creating the request
request_3 = requests.get(paymentMethodsEndpoint)

# Printing the result
print("3) Payment Providers")
print("Payload: ")
print(paymentMethodsEndpoint)
print("API Response: ")
print(request_3.text)
print("Status Code: " + str(request_3.status_code))

data  = json.loads(request_3.text)

print("3) Available Payment Providers")
for provider in data:
    print("Payment Provider ID: " + provider["pay_provider_id"])
    print("Payment Provider Name: " + provider["pay_provider_name"])
print("\n\n")


# 4) Pay for Booking: POST method
# Passing the booking number generated in part 2 along with a payment provider id generated in part 3
payForBookingEndpoint = 'http://127.0.0.1:8000/api/payforbooking/'
payForBookingPayload = {"booking_num":"OK6O3V", "pay_provider_id":1}

# Creating the request
request_4 = requests.post(payForBookingEndpoint, json=payForBookingPayload)

# Printing the result
print("4) Pay for Booking")
print("Sent Payload: ")
print(payForBookingPayload)
print("API Response: ")
print(request_4.text)
print("Status Code: " + str(request_4.status_code))
print("\n\n")


# 5) Finalize Booking: POST method
finalizeBookingEndpoint = 'http://127.0.0.1:8000/api/finalizebooking/'
# Passing the booking number from part 2, payment provider id from part 3 and stamp from the payment service
finalizeBookingPayload = {"booking_num":"OK6O3V", "pay_provider_id": "1", "electronic_stamp":"a1b2c3d4e5"}

# Creating the request
request_5 = requests.post(finalizeBookingEndpoint, json=finalizeBookingPayload)

# Printing the result
print("5) Finalize Booking")
print("Sent Payload: ")
print(finalizeBookingPayload)
print("API Response: ")
print(request_5.text)
print("Status Code: " + str(request_5.status_code))
print("\n\n")


# 6) Booking Status: POST method
bookingStatusEndpoint = 'http://127.0.0.1:8000/api/bookingstatus/'
# Passing the booking number from part 2
bookingStatusPayload = {"booking_num":"OK6O3V"}

# Creating the request
request_6 = requests.get(bookingStatusEndpoint, json=bookingStatusPayload)

# Printing the result
print("6) Booking Status")
print("Sent Payload: ")
print(bookingStatusPayload)
print("API Response: ")
print(request_6.text)
print("Status Code: " + str(request_6.status_code))
print("\n\n")


# 7) Cancel Booking section - Method: POST ##############################
cancelBookingEndpoint = 'http://127.0.0.1:8000/api/cancelbooking/'
# Passing the booking number from part 2
cancelBookingPayload = {"booking_num":"OK6O3V"}


request_7 = requests.post(cancelBookingEndpoint, json=cancelBookingPayload)
print("7) Cancel Booking")
print("Sent Payload: ")
print(cancelBookingPayload)
print("API Response: ")
print(request_7.text)
print("Status Code: " + str(request_7.status_code))

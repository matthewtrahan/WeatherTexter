import smtplib
from credentials import *
from unidecode import unidecode
import json
import requests

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login(EMAIL, PASSWORD)

zipCodes = [77450, 77002]

for zipCode in zipCodes:

	message = ""

	# get the API required location key
	locationKeyUrl = "http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey={}&q={}".format(KEY, zipCode)
	locationKeyResponse = requests.get(locationKeyUrl)
	locationKeyJson = locationKeyResponse.json()

	locationKey = locationKeyJson[0]['Key']

	# daily forecast
	dailyForecastUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/{}?apikey={}&details=true".format(locationKey, KEY)
	dailyForecastResponse = requests.get(dailyForecastUrl)
	dailyForecastJson = dailyForecastResponse.json()

	headline = dailyForecastJson['Headline']['Text']
	low = dailyForecastJson['DailyForecasts'][0]['Temperature']['Minimum']['Value']
	high = dailyForecastJson['DailyForecasts'][0]['Temperature']['Maximum']['Value']
	sunriseRaw = dailyForecastJson['DailyForecasts'][0]['Sun']['Rise']
	sunsetRaw = dailyForecastJson['DailyForecasts'][0]['Sun']['Set']

	sunriseRaw2 = sunriseRaw.split('T')
	sunsetRaw2 = sunsetRaw.split('T')

	sunriseRaw3 = sunriseRaw2[1].split('-')
	sunsetRaw3 = sunsetRaw2[1].split('-')

	sunrise = sunriseRaw3[0]
	sunset = sunsetRaw3[0]

	# current conditions
	currentConditionsUrl = "http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}".format(locationKey, KEY)
	currentConditionsResponse = requests.get(currentConditionsUrl)
	currentConditionsJson = currentConditionsResponse.json()

	currentTemp = currentConditionsJson[0]['Temperature']['Imperial']['Value']
	currentCondition = currentConditionsJson[0]['WeatherText']

	# forecast for the next 12 hours
	nextTwelveHoursUrl = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{}?apikey={}".format(locationKey, KEY)
	nextTwelveHoursResponse = requests.get(nextTwelveHoursUrl)
	nextTwelveHoursJson = nextTwelveHoursResponse.json()

	temperatures = []
	conditions = []
	precipitationProbs = []

	for hour in nextTwelveHoursJson:
		temperatures.append(hour['Temperature']['Value'])
		conditions.append(hour['IconPhrase'])
		precipitationProbs.append(hour['PrecipitationProbability'])

	message += headline + '.\n'
	message += 'Today\'s high will be ' + high + '.\n'
	message += 'Today\'s low will be ' + low + '.\n'
	message += 'The sun will rise at ' + sunrise + '.\n'
	message += 'The sun will set at ' + sunset + '.\n'
	message += 'The current temperature is ' + currentTemp + '.\n'
	message += 'The current condition is ' + currentCondition + '.\n'
	


	# Send text message through SMS gateway of destination number
	# server.sendmail( 'Matthew', PHONE, message)

	print(message)
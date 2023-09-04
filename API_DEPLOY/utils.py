"""
************************************************************************
* Author = Gerardo David López Castillo                                *
* Date = '30/08/2023'                                                  *
* Description = Envio de mensajes Twilio con Python                    *
************************************************************************
"""
import pandas as pd
import requests
import time
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,PHONE_NUMBER_DES,API_KEY_WAPI
from datetime import datetime

def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_wapi(api_key,query):

    url_clima = 'https://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):

    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return fecha,hora,condicion,tempe,rain,prob_rain

def create_df(data):

    col = ['Fecha','Hora','Condicion','Temperatura','Lluvia','prob_lluvia']
    df = pd.DataFrame(data,columns=col)
    df = df.sort_values(by = 'Hora',ascending = True)

    df = df.replace('Light rain', 'Lluvia lig').replace('Fog', 'Niebla').replace('Mist', 'Neblina').replace(
        'Partly cloudy', 'Parc/nublado').replace('Sunny', 'Soleado').replace('Patchy light rain with thunder',
                                                                             'Lluvia lig irr/truenos').replace(
        'Moderate or heavy rain shower', 'Lluvia moderada/fuerte').replace('Light rain shower', 'Lluvia lig').replace(
        'Patchy rain possible', 'Pos lluvia irr').replace('Cloudy', 'Nublado')
    #df_rain = df[(df['Lluvia']==1) & (df['Hora']>6) & (df['Hora']< 22)]
    df_rain = df[(df['Hora'] > 3) & (df['Hora'] < 22)]
    df_rain = df_rain[['Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']]
    df_rain.set_index('Hora', inplace = True)

    return df_rain

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df_rain,query):

    time.sleep(10)
    original_message = '\nGDLOPEZCASTILLO! El pronostico de lluvia hoy ' + input_date + ' en ' + query + ' es : \n\n ' + str(df_rain)
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=original_message,
                        from_=PHONE_NUMBER,
                        to=PHONE_NUMBER_DES
                    )

    return message.sid

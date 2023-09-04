"""
************************************************************************
* Author = Gerardo David López Castillo                                *
* Date = '30/08/2023'                                                  *
* Description = Envio de mensajes Twilio con Python                    *
************************************************************************
"""
from twilio_config import *
from tqdm import tqdm
from utils import request_wapi,get_forecast,create_df,send_message,get_date

query = 'Guatemala'
api_key = API_KEY_WAPI

input_date= get_date()
response = request_wapi(api_key,query)

datos = []
for i in tqdm(range(24),colour = 'green'):
    datos.append(get_forecast(response,i))

df_rain = create_df(datos)

# Send Message
message_id = send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df_rain,query)

print('Mensaje Enviado con exito ' + message_id)
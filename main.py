import telebot
import requests


def forecast(city):
    url = 'https://openweathermap.org/data/2.5/weather?q=' + \
          city + '&appid=b6907d289e10d714a6e88b30761fae22'

    response = requests.get(url)
    dictionary = response.json()
    if dictionary['cod'] != 200:
        raise Exception('can\'t find this city...')
    result = 'country: ' + str(dictionary['sys']['country']) + '\n' + \
             'main_info: ' + str(dictionary['weather'][0]['main']) + '\n' + \
             'temperature: ' + str(dictionary['main']['temp']) + '\n' + \
             'feels_like: ' + str(dictionary['main']['feels_like'])
    return result


def _main():
    print()
    city = input('Enter the city name (or \'exit\' to exit):\n')
    try:
        f = forecast(city)
        print(f)
    except Exception as err:
        print(err.args[0])
    finally:
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


TOKEN = '1003641334:AAGTcXkdNFzHq2KQwXSw_4YIGza0ajGt_og'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def give_description(message):
    bot.send_message(message.chat.id, 'enter a city name, ' + \
                     'for example, \'Вологда\' to get a weather forecast')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Howdy, how are you doing?\n' \
            'type \'/help\' to get information')


@bot.message_handler(func=lambda message: True)
def make_weather_forecast(message):
    f = ''
    try:
        f = forecast(message.text)
    except Exception as err:
        f = err.args[0]
    bot.send_message(message.chat.id, f)


bot.polling(none_stop=True)

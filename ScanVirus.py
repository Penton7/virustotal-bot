import requests
import telebot
import config
import sys

bot = telebot.TeleBot(config.token)
file = ''

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
 try:
    chat_id = message.chat.id

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = '/home/penton7/test/' + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Start scans")
    url0 = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params0 = {'apikey': '958b49fa9966ae15cee97686c744b717f3a8a9a8b9f8d93f20f19a312a07991f'}
    files = {'file': (str(src), open(str(src), 'rb'))}
    response = requests.post(url0, files=files, params=params0)
    #print(response.json())
    resource = response.json()["resource"]

    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': '958b49fa9966ae15cee97686c744b717f3a8a9a8b9f8d93f20f19a312a07991f', 'resource': str(resource)}
    #    print(start.resource)
    response = requests.get(url, params=params)
    scans = response.json()["scans"]
    sys.stdout = open("/home/penton7/test/text.txt", "w")

    for key, det in scans.items():
        print("[Antivirus] " + key + " | ", end="")
        print("Detected:", det['detected'])
    sys.stdout.close()
    bot.reply_to(message, open("/home/penton7/test/text.txt", "r"))

 except Exception as e:
    bot.reply_to(message, e)

bot.polling(none_stop=True, interval=0)

#https://api.telegram.org/bot554264595:AAElo0W0P4QNG3LfGmmnR0TifnavgxDNOeU/getFile?file_id=BQADAgADvQMAAr7LGUi8K-ZIBmvBMQI






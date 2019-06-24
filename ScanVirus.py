import requests
import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
 try:
    chat_id = message.chat.id

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = '/home/penton7/test/' + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Wait pls...")
    #Send file to virustotal
    params0 = {'apikey': config.api}
    files = {'file': (str(src), open(str(src), 'rb'))}
    response = requests.post(config.url_scan, files=files, params=params0)
    resource = response.json()["resource"]

    #Report antivirus
    params = {'apikey': config.api, 'resource': str(resource)}
    response = requests.get(config.url_info, params=params)
    scans = response.json()["scans"]
    fal = 0
    tru = 0
    for key, det in scans.items():
        if det['detected'] == False:
            fal += 1
        else:
            tru += 1

    bot.reply_to(message, 'Detected: ' + str(tru) + "\n" + "Clear: "+ str(fal) + "\n" + "Link: " + "https://www.virustotal.com/gui/file/"+ str(resource) + "/detection"  )
 except Exception as e:
    bot.reply_to(message, e)

bot.polling(none_stop=True, interval=0)







import requests
import telebot
import time

token = '814437389:AAHtwOCGU3Zp6s0aMna9w0rXszTUMXvfyb0' #Telegram token
api = 'x-apikey: 958b49fa9966ae15cee97686c744b717f3a8a9a8b9f8d93f20f19a312a07991f' #VirusTotal api token
url_scan = 'https://www.virustotal.com/api/v3/files' #Url for scans file and return file id
url_info = 'https://www.virustotal.com/api/v3/analyses/' #Url for information file

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
 try:
    #Telegram download file
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = '/home/penton7/projects/test/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Wait pls...")

    #Send file to virustotal
    headers = {'x-apikey':'958b49fa9966ae15cee97686c744b717f3a8a9a8b9f8d93f20f19a312a07991f'}
    files = {'file': (src)+ message.document.file_name}
    print(files)
    response = requests.post("https://www.virustotal.com/api/v3/files", headers=headers, files=files )
    print(response)
    resource = response.json()["data"]["id"]

    #Report antivirus   
    response = requests.get("https://www.virustotal.com/api/v3/analyses/NTZiNDg5OWU4NDQ2MjlkNDJjZmNlN2Y4Nzc4OTM4MmE6MTU2ODAzMDY0OQ==", headers=headers)
    time.sleep(30)
    scans = response.json()["data"]["attributes"]["results"]
    #tru = 0
    #for key, det in scans.items():
     #   if det['detected'] == False:
      #      bot.reply_to(message, det[''] + 'Virus: ')
    #bot.reply_to(message, 'Virus: ' + str(tru) + "\n" + "Clear: "+ str(fal) + "\n" + "Link: " + "https://www.virustotal.com/gui/file/" + str(resource) + "/detection")
    bot.reply_to(message, scans)
 except Exception as e:
    bot.reply_to(message, e)

bot.polling(none_stop=True, interval=0)

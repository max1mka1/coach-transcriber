import sys, os
import threading
from io import StringIO 
import telebot
from collections import deque
import whisper
import torch

# СЮДА НАДО ВПИСАТЬ ВАШ ТОКЕН ОТ ТЕЛЕГРАМ

os.

token = 'ВАШ_ТОКЕН'

q = deque()


# turn on cuda if GPU is available
use_cuda = torch.cuda.is_available()

if use_cuda:
    model = whisper.load_model("small").cuda()
else: 
    model = whisper.load_model("small")

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

print('Загрузка...')

bot = telebot.TeleBot(token)

print('Бот запущен и работает...')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "hello...")

@bot.message_handler(content_types=['voice'])
def message_deque(message):
    q.append(message)

#bot.polling(interval=3, timeout=45)
#bot.infinity_polling()
if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        if q:
            message = q.popleft()
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('audio.ogg', 'wb') as new_file:
                new_file.write(downloaded_file)
            with Capturing() as output:
                result = model.transcribe("audio.ogg")

           
            reply = result["text"][:1024]
            if len(reply) > 4096:
                msgs = [reply[i:i + 4096] for i in range(0, len(reply), 4096)]
                for text in msgs:
                    bot.reply_to(message, text, parse_mode="HTML")    
            else:
                print(reply)
                bot.reply_to(message, reply, parse_mode="HTML")

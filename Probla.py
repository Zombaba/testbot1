import telebot
 
bot = telebot.TeleBot('929156879:AAEYEhJpZDSz8U8Ns_GFXiyCwh47-K2o9ac')
###########################################################################################################################
pol = ['Cześć', 'Placić', 'Czekać', 'Pisać', 'Nieść', 'Do widzenia', 'Dzień dobry', 'Świetnie', 'Jeszcze raz', 'Wiedzieć']#
rus = ['привет', 'платить', 'ждать', 'писать', 'нести', 'до свидания', 'день добрый', 'отлично', 'еще раз', 'знать']      #
###########################################################################################################################
# это генератор, выдает слова из списка по одному 
def get_words():
    for word in pol:
        yield word
# в words будет генератор, в messages ответы пользователя
words = None
messages = []
eror = [] 
 
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет. Предлагаю проверить ваши знания: переведите польские слова на руский язык\n\n Введите /go что бы начать тест (ответы писать маленькими буквами)")
 
# эта функция срабатывает если пользователь написал /go
# создаем генератор и отправляем первое слово списка
@bot.message_handler(commands=['go'])
def start_message(message):
    global words
    words = get_words()
    bot.send_message(message.chat.id, next(words))
 
 
# эта функция срабатывает если пользователь напишет любое слово
@bot.message_handler(func=lambda message: True)
def echo(message):
    global words, messages, eror
    # если пользователь не писал /go, то ничего не делаем
    if not words:
        return
    # если у генератора попробовать получить слово вне списка, то он вернет исключение
    try:
        # записываем ответ пользователя и отправляем ему новое слово
        messages.append(message.text)
        bot.send_message(message.chat.id, next(words))
    except: 
        x = 0            
        bad = 0
        good = 0
        # подсчитываем правильные и неправильные ответы
        for i, ru in enumerate(messages):
            if ru == rus[i]:
                good += 1
            else:
                bad += 1
                eror.append(ru)
        if bad > 0:
            bot.send_message(message.chat.id,  "Ошибка сделана в следующих словах: ")         
            for x in eror: 
                bot.send_message(message.chat.id,  x) 
        elif bad == 0:
            bot.send_message(message.chat.id,"Вы ответили правильно на все слова. Поздравляю!")
        else:
            bot.send_message(message.chat.id, "Вы сделали " + str(bad) +" ошибок\n Вы ответили правильно на " + str(good) +" вопросов.")
        bot.send_message(message.chat.id,   "Введите /go что бы пройти тест ещё раз. ")
        # обнуляем переменные words и messages, теперь если написать /go, то начнется сначала
       # if bad < 3:
       #     bot.send_message(message.chat.id, "Приговор: Ебать ты красава")
       # elif bad < 6:
       #     bot.send_message(message.chat.id, "Приговор: Ты ёба")
       # elif bad < 10:
       #     bot.send_message(message.chat.id, "Приговор: Отошёл от компа, ПИДОР!!!")
        words = None
        messages = []
        eror = []
bot.polling()
from telegram import(ReplyKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import (Updater,CommandHandler,MessageHandler,Filters,ConversationHandler)

import logging
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

NAME,STID,CLASSTIME,PROJECTS,SUMMARY=range(5)

userstid=""
userfullname=""
userclass=""
usersummary=""
username=""

def start(bot,update):

    update.message.reply_text(
        'سلام به ربات دريافت پروژه درس کارگاه کامپيوتر خوش آمديد'
        'لطفا نام و نام خانوادگي خود را وارد کنيد')
    return NAME

def name(bot,update):
    global userfullname
    user = update.message.from_user
    userfullname = update.message.text
    update.message.reply_text('با تشکر'
                              'لطفا شماره دانشجويي خود را با اعداد انگليسي وارد کنيد')
    return STID

def stid(bot,update):
    global userstid
    reply_keyboard = [['shanbe: 9:00-12:00', 'shanbe: 13:30-16-30','yek shanbe: 9:00-12:00', 'yek shanbe: 13:30-16-30']]
    user = update.message.from_user
    userstid= update.message.text
    update.message.reply_text('متشکرم'
                              'حالا نوبت کلاس خود را مشخص کنيد'
                              ,reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    return CLASSTIME

def classtime(bot,update):
    global userclass
    user = update.message.from_user
    userclass = update.message.text
    update.message.reply_text('با تشکر'
                              'فايل پروژه خود را با فرمت پايتون ارسال کنيد')
    return PROJECTS

def project(bot,update):
    global userstid
    user = update.message.from_user
    Id=update.message.document.file_id
    userproject = bot.get_file(Id)
    userproject.download(str(userstid) + ".py")
    update.message.reply_text('توضيح کوتاهي در مورد پروزه خود بدهيد')

    return SUMMARY

def summary(bot,update):
    global userclass
    global userstid
    global userfullname
    global usersummary
    global username
    user = update.message.from_user
    usersummary = update.message.text
    update.message.reply_text('پروژه شما ثبت شد')
    sharh = open(str(userstid) + ".txt", "a" , encoding="utf-8")
    kamel = ("\n" + str(userfullname) + "\n" + str(userstid) + "\n" + str(userclass) + "\n" + str(usersummary) + "\n" + str(user.username) + "\n" + str(datetime.datetime.now())+"\n")
    sharh.write(kamel)
    sharh.close()
    return ConversationHandler.END

def cancel(bot,update):
    user = update.message.from_user
    logger.info("شما اين گفت و گو را لغو کرديد")
    update.message.reply_text('منتظر ارسال پروژه در اولين فرصت هستيم',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def error(bot,update,error):
    logger.warning('update "%s" caused erroe "%s"',update,error)

def main():
    updater = Updater("706236196:AAHJ9fLV3FYk0NGo7hSekoX2IWjPZUh8qhw")

    dp=updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],

        states={

            NAME: [MessageHandler(Filters.text,name)],

            STID: [MessageHandler(Filters.text,stid)],

            CLASSTIME: [MessageHandler(Filters.text,classtime)],

            PROJECTS: [MessageHandler(Filters.document,project)],

            SUMMARY: [MessageHandler(Filters.text,summary)]

            },

            fallbacks=[CommandHandler('cancel',cancel)]

        
        )
    
    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
                             
    

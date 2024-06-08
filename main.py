import pandas as pd
import telebot
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
import os,codecs
import json
import shutil
from server import server

#=========Basic Require
token = ''
id_admin = 00000000
path_file = "data.xlsx"
#==========

df = pd.read_excel(path_file)
def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object

bot = telebot.TeleBot(token, num_threads=20, skip_pending=True)
@bot.message_handler(commands=['start'])
def start(message):
    #=================ADMIN#=================
    if message.chat.id == id_admin:
        key_admin = InlineKeyboardMarkup(row_width=2)
        
        but_admin1 = InlineKeyboardButton(text="اذاعة", callback_data="mesage_admain")
        key_admin.add(but_admin1)
        
        but_admin2 = InlineKeyboardButton(text="حظر", callback_data="blook_admain")
        key_admin.add(but_admin2)
        
        but_admin3 = InlineKeyboardButton(text="فك الحظر", callback_data="unblook_admain")
        key_admin.add(but_admin3)
        
        but_admin4 = InlineKeyboardButton(text="المستخدمين", callback_data="users_admain")
        key_admin.add(but_admin4)
        
        bot.send_message(message.chat.id, f"Bot Info Data\n===============\nUser_act = {len(os.listdir('users_id/'))}\nUser_blok = {len(os.listdir('users_blook/'))}\nUsers_all = {len(os.listdir('users_blook/'))+len(os.listdir('users_id/'))}\n===============\n@knk_1k", reply_markup=key_admin)
        
    
    ##=================BLOOK#=================
    elif f"{message.chat.id}.json" in os.listdir("users_blook/"):
        bot.send_message(message.chat.id, "تم حظرك من قبل مدير البوت للاستفسار @knk_1k")
    
    else:
        ##=================New user#=================
        if f"{message.chat.id}.json" not in os.listdir("users_id/"):
            jf = open(f"users_id/{message.chat.id}.json", "w")
            data_user = {"Id":message.from_user.id,"First_Name":message.from_user.first_name,"Last_Name":message.from_user.last_name,"Username":message.from_user.username,"data_info":[]}
            jf.write(json.dumps(data_user))
            jf.close()
            start(message)
        else:
            key_mainis = InlineKeyboardMarkup(row_width=2)
            but_mainch_name = InlineKeyboardButton(text="بحث عن اسم شخص", callback_data="serch_name")
            key_mainis.add(but_mainch_name)
            but_mainch_email = InlineKeyboardButton(text="بحث عن اميل", callback_data="serch_emali")
            key_mainis.add(but_mainch_email)
            but_mainch_ph = InlineKeyboardButton(text="بحث عن رقم هاتف", callback_data="serch_ph")
            key_mainis.add(but_mainch_ph)
            bot.send_message(message.chat.id, "هذا البوت تم برمجته من قبل المهندس مجتبى المياحي", reply_markup=key_mainis)


@bot.callback_query_handler(func=lambda call: call.data == 'serch_emali')
def handle_button_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='ارسل الاميل المراد البحث عنه')
    bot.register_next_step_handler(call.message,def_serch_emali)
def def_serch_emali(message):
    if "/start" == message.text:
        start(message)
    else:
        mes = bot.reply_to(message, "جار البحث ... يرجى الانتظار")
        emli = str(message.text)
        
        #Save Serch user
        with open(f"users_id/{message.chat.id}.json") as file_data:
            data = json.load(file_data, object_hook=from_json)
        data['data_info'].append(emli)
        file_data.close()
        os.remove(f'users_id/{message.chat.id}.json')
        jf = open(f"users_id/{message.chat.id}.json", "w")
        jf.write(json.dumps(data))
        jf.close()
        
        
        res = df[df['Email ']== emli].to_dict()
        try:
            if res['Email '] == {}:
                bot.delete_message(message.chat.id, mes.message_id)
                bot.send_message(message.chat.id, "لا يوجد هذا الاميل في قواعد البيانات")  
                start(message)
            
            else:
                bot.delete_message(message.chat.id, mes.message_id)
                info_tar = f"Name : {list(res['First Name'].values())[0]} {list(res['Last Name'].values())[0]}\nGender : {list(res['Gender'].values())[0]}\nEmail : {list(res['Email '].values())[0]}\nPhone : {list(res['Phone Number'].values())[0]}\nCity : {list(res['City'].values())[0]}\nAddress : {list(res['Address'].values())[0]}\n======================================\nDEV eng_Mojtaba Tele & Insta in knk_1k"
                bot.send_message(message.chat.id, info_tar)
                start(message)
    
        except Exception as e:
            bot.send_message(message.chat.id,f"حدث خطأ \n{e}") 
            start(message) 
    




@bot.callback_query_handler(func=lambda call: call.data == 'serch_ph')
def handle_button_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='ارسل رقم الهاتف بدون رمز الدولة\nمثلا\n310674195.0')
    bot.register_next_step_handler(call.message,def_serch_ph)
def def_serch_ph(message):
    if "/start" == message.text:
        start(message)
    else:
        
        try:
            mes = bot.reply_to(message, "جار البحث ... يرجى الانتظار")
            ph = int(message.text)
            
            #Save Serch user
            with open(f"users_id/{message.chat.id}.json") as file_data:
                data = json.load(file_data, object_hook=from_json)
            data['data_info'].append(ph)
            file_data.close()
            os.remove(f'users_id/{message.chat.id}.json')
            jf = open(f"users_id/{message.chat.id}.json", "w")
            jf.write(json.dumps(data))
            jf.close()
            
            res = df[df['Phone Number']== ph].to_dict()

            if res['Phone Number'] == {}:
                bot.delete_message(message.chat.id, mes.message_id)
                bot.send_message(message.chat.id, "لا يوجد هذا الرقم في قواعد البيانات")  
                start(message)

            else:
                bot.delete_message(message.chat.id, mes.message_id)
                info_tar = f"Name : {list(res['First Name'].values())[0]} {list(res['Last Name'].values())[0]}\nGender : {list(res['Gender'].values())[0]}\nEmail : {list(res['Email '].values())[0]}\nPhone : {list(res['Phone Number'].values())[0]}\nCity : {list(res['City'].values())[0]}\nAddress : {list(res['Address'].values())[0]}\n======================================\nDEV eng_Mojtaba Tele & Insta in knk_1k"
                bot.send_message(message.chat.id, info_tar)
                start(message)
                
        except Exception as e:
            if "int()" in str(e):
                bot.delete_message(message.chat.id, mes.message_id)
                bot.send_message(message.chat.id, "يرجى كتابة الرقم الصحيح")
                start(message)
            else:
                bot.delete_message(message.chat.id, mes.message_id)
                bot.send_message(message.chat.id, f"حدث خطا \n{e}")
                start(message)


@bot.callback_query_handler(func=lambda call: call.data == 'serch_name')
def handle_button_2(call):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='ارسل الاسم مع اسم العائلة بالانكليزي\nمثلا \nJose Garcia')
    bot.register_next_step_handler(call.message,def_serch_name)
def def_serch_name(message):
    if "/start" == message.text:
        start(message)
    else:
        name = str(message.text)
        mes = bot.reply_to(message, "جار البحث ... يرجى الانتظار")
        
        #Save Serch user
        with open(f"users_id/{message.chat.id}.json") as file_data:
            data = json.load(file_data, object_hook=from_json)
        data['data_info'].append(name)
        file_data.close()
        os.remove(f'users_id/{message.chat.id}.json')
        jf = open(f"users_id/{message.chat.id}.json", "w")
        jf.write(json.dumps(data))
        jf.close()
        

        if len(name.split()) == 2:
            Fname = name.split(" ")[0]
            Lname = name.split(" ")[1]
            res = df[df['First Name']== Fname].to_dict()
            
            if res['First Name'] != {}:
                ress = df[df['Last Name']== Lname].to_dict()
                if ress['Last Name'] != {}:
                    info_tar = f"Name : {list(ress['First Name'].values())[0]} {list(ress['Last Name'].values())[0]}\nGender : {list(ress['Gender'].values())[0]}\nEmail : {list(ress['Email '].values())[0]}\nPhone : {list(ress['Phone Number'].values())[0]}\nCity : {list(ress['City'].values())[0]}\nAddress : {list(ress['Address'].values())[0]}\n======================================\nDEV eng_Mojtaba Tele & Insta in knk_1k"
                    bot.delete_message(message.chat.id, mes.message_id)
                    bot.send_message(message.chat.id, info_tar)
                    start(message)
                    
                else:
                    bot.delete_message(message.chat.id, mes.message_id)
                    bot.send_message(message.chat.id, "لا يوجد هذ الاسم في قواعد البيانات")
                    start(message)
            
            else:
                bot.delete_message(message.chat.id, mes.message_id)
                bot.send_message(message.chat.id, "لا يوجد هذ الاسم في قواعد البيانات")
                start(message)

        else:
            bot.delete_message(message.chat.id, mes.message_id)
            bot.send_message(message.chat.id, "يرجى ارسال الاسم مع الاسم العائلة")
            start(message)



@bot.callback_query_handler(func=lambda call: call.data == 'mesage_admain')
def handle_button_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='ارسل الرسالة المرادارسالها للمستخدمين')
    bot.register_next_step_handler(call.message,def_send_message)
def def_send_message(message):
    if "/start" == message.text:
        start(message)
    else:
        for i in os.listdir("users_id/"):
            user_id = i.split(".json")[0]
            bot.send_message(chat_id=user_id, text=message.text)

        bot.send_message(chat_id=message.chat.id, text="انتهى")
        start(message)



@bot.callback_query_handler(func=lambda call: call.data == 'blook_admain')
def handle_button_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='ارسل الايدي لكي يتم حضره من البوت')
    bot.register_next_step_handler(call.message,def_blook_admain)  

def def_blook_admain(message):
    if "/start" == message.text:
        start(message)
    else:
        idd_ = message.text
        
        if f"{idd_}.json" in os.listdir("users_id/"):
            shutil.move(f"users_id/{idd_}.json",f"users_blook/{idd_}.json")
            bot.send_message(chat_id=idd_, text='تم حظرك')
            bot.send_message(chat_id=message.chat.id, text='تم الحظر')
            start(message)
        else:
            bot.send_message(chat_id=message.chat.id , text='لا يوجد هذا المعرف في قائمةالمستخدمين')
 

@bot.callback_query_handler(func=lambda call: call.data == 'unblook_admain')
def handle_button_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='ارسل الايدي لكي يتم رفع الحظر منه')
    bot.register_next_step_handler(call.message,def_unblook_admain)  

def def_unblook_admain(message):
    if "/start" == message.text:
        start(message)
    else:
        idd_ = message.text
        
        if f"{idd_}.json" in os.listdir("users_blook/"):
            shutil.move(f"users_blook/{idd_}.json",f"users_id/{idd_}.json")
            bot.send_message(chat_id=idd_, text='تم فتح الحظر عنك')
            bot.send_message(chat_id=message.chat.id, text='تم رفع الحظر')
            start(message) 
        else:
            bot.send_message(chat_id=message.chat.id, text='لا يوجد هذا المعرف في قائمة المحظورين')
 

#
#users_admain
@bot.callback_query_handler(func=lambda call: call.data == 'users_admain')
def handle_button_1(call):
    key_us = InlineKeyboardMarkup(row_width=2)
    but_us1 = InlineKeyboardButton(text=f"قائمة المستخدمين |{len(os.listdir('users_id/'))}|", callback_data="admain_list_user")
    key_us.add(but_us1)
    but_us2 = InlineKeyboardButton(text=f"قائمة المحظورين |{len(os.listdir('users_blook/'))}|", callback_data="admain_list_blook")
    key_us.add(but_us2)
    bot.send_message(call.message.chat.id, "قائمة المستخدمين", reply_markup=key_us)

@bot.callback_query_handler(func=lambda call: call.data == 'admain_list_user')
def handle_button_1(call):         
    if len(os.listdir("users_id/")) >=1:  
        for i in os.listdir("users_id/"):
            with open(f"users_id/{i}", "r") as al:
                data = json.load(al)
            bot.send_message(call.message.chat.id, f"NAME = {data['First_Name']} {data['Last_Name']}\nUSER = {data['Username']}\nINFO_SH = {data['data_info']}\n\nID = {data['Id']}")  
    else:
        bot.send_message(call.message.chat.id,"لا يوجد مستخدمين للبوت")

@bot.callback_query_handler(func=lambda call: call.data == 'admain_list_blook')
def handle_button_1(call):
    if len(os.listdir("users_blook/")) >=1:  
        for i in os.listdir("users_blook/"):
            with open(f"users_blook/{i}", "r") as al:
                data = json.load(al)
            bot.send_message(call.message.chat.id, f"NAME = {data['First_Name']} {data['Last_Name']}\nUSER = {data['Username']}\nINFO_SH = {data['data_info']}\n\nID = {data['Id']}")  
    else:
        bot.send_message(call.message.chat.id,"لا يوجد مستخدمين في قائمة الحظر")


if __name__ == "__main__":
    print("STARTING ...")
    server()
    bot.polling()
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
import re
import sqlite3 as sq
import schedule
import time
import asyncio
import requests
import config


class TelegramPost:
    TOKEN = config.TOKEN
    TOKEN_notification = config.TOKEN_notification

    GENERAL_IDs = config.GENERAL_IDs
    PRIVATE_IDs = config.PRIVATE_IDs

    bot = Bot(token=TOKEN)

    def __await__(self):
        return self._async_init().__await__()

    def post_channel_private(self):
        data = sql_read('private')
        if data:
            n, name, description, tg_id, tag, checked, to_1, to_2, link, message_id = data
            
            if link and tg_id:
                msg = f"🔥 <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="{link}">Ссылка</a>'+f'\n\n<a href=\"tg://user?id={tg_id}\">Связаться с заказчиком</a>'
                url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.PRIVATE_ID}&text={msg}&parse_mode=HTML"
                data_oo = requests.get(url)
                to_link_message_id(data_oo.json().get("result").get("message_id"), n)

                # Отправляем уведомление, что выложили объявление
                msg_notification = f"Ваше объявление \"<b>{name}</b>\" проверено и уже доступно соискателям"
                url_notification = f"https://api.telegram.org/bot{self.TOKEN_notification}/sendMessage?chat_id={tg_id}&text={msg_notification}&parse_mode=HTML"
                requests.get(url_notification)
                return
            if link:
                msg = f"🔥 <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="{link}">Связаться с заказчиком</a>'
                url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.PRIVATE_IDs.get(tag)}&text={msg}&parse_mode=HTML"
                data_oo = requests.get(url)
                to_link_message_id(data_oo.json().get("result").get("message_id"), n)
                return
            if tg_id:
                msg = f"🔥 <b>{name}</b>"+'\n\n'+description+f'\n\n<a href=\"tg://user?id='+str(tg_id)+'\">Связаться с заказчиком</a>'
                url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.PRIVATE_IDs.get(tag)}&text={msg}&parse_mode=HTML"
                data_oo = requests.get(url)
                to_link_message_id(data_oo.json().get("result").get("message_id"), n)

                # Отправляем уведомление, что выложили объявление
                msg_notification = f"Ваше объявление \"<b>{name}</b>\" проверено и уже доступно соискателям"
                url_notification = f"https://api.telegram.org/bot{self.TOKEN_notification}/sendMessage?chat_id={tg_id}&text={msg_notification}&parse_mode=HTML"
                requests.get(url_notification)
        return

    def post_channel_general(self):
        data = sql_read('general')
        if data:
            # Отправляем в общий
            n, name, description, tg_id, tag, checked, to_1, to_2, link, message_id = data
            msg = f"🔥 <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="t.me/freelancex_account_bot/?start={n}">Связаться с заказчиком</a>'
            url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.GENERAL_IDs.get(tag)}&text={msg}&parse_mode=HTML"
            message_id_in_usual_data = requests.get(url)
                
            # Отправляем уведомление, что выложили объявление
            gg = message_id_in_usual_data.json().get('result')
            link_to_post = str(gg.get("sender_chat").get("username"))+"/"+str(gg.get('message_id'))
            msg_notification = f"Ваше объявление \"<a href=\"https://t.me/"+str(link_to_post)+f'\"><b>{name}</b></a>\" проверено и уже доступно соискателям'
            url_notification = f"https://api.telegram.org/bot{self.TOKEN_notification}/sendMessage?chat_id={tg_id}&text={msg_notification}&parse_mode=HTML"
            requests.get(url_notification)
            return
        return
    
    def post_channel_all(self):
        data = sql_read('all')
        if data:
            n, name, description, tg_id, tag, checked, to_1, to_2, link, message_id = data
            if link and tg_id:
                # Отправляем в приват
                msg = f"🔥 №<code>{n}</code> - <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="{link}">Ссылка</a>'+f'\n\n<a href=\"tg://user?id={tg_id}\">Связаться с заказчиком</a>'
                url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.PRIVATE_IDs.get(tag)}&text={msg}&parse_mode=HTML"
                data_oo = requests.get(url)
                to_link_message_id(data_oo.json().get("result").get("message_id"), n)
                
                # Отправляем в общий
                msg2 = f"🔥 №<code>{n}</code> - <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="t.me/freelancex_account_bot/?start={n}">Связаться с заказчиком</a>'
                url2 = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.GENERAL_IDs.get(tag)}&text={msg2}&parse_mode=HTML"
                message_id_in_usual_data = requests.get(url2)

                # Отправляем уведомление, что выложили объявление
                gg = message_id_in_usual_data.json().get('result')
                link_to_post = str(gg.get("sender_chat").get("username"))+"/"+str(gg.get('message_id'))
                msg_notification = f"Ваше объявление \"<a href=\"https://t.me/"+str(link_to_post)+f'\"><b>{name}</b></a>\" проверено и уже доступно соискателям'
                url_notification = f"https://api.telegram.org/bot{self.TOKEN_notification}/sendMessage?chat_id={tg_id}&text={msg_notification}&parse_mode=HTML"
                requests.get(url_notification)
                return
            if link:
                # Отправляем в приват
                msg = f"🔥 №<code>{n}</code> - <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="{link}">Связаться с заказчиком</a>'
                url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.PRIVATE_IDs.get(tag)}&text={msg}&parse_mode=HTML"
                data_oo = requests.get(url)
                to_link_message_id(data_oo.json().get("result").get("message_id"), n)
                
                # Отправляем в общий
                msg2 = f"🔥 №<code>{n}</code> - <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="t.me/freelancex_account_bot/?start={n}">Связаться с заказчиком</a>'
                url2 = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.GENERAL_IDs.get(tag)}&text={msg2}&parse_mode=HTML"
                requests.get(url2)
                return
            if tg_id:
                # Отправляем в приват
                msg = f"🔥 №<code>{n}</code> - <b>{name}</b>"+'\n\n'+description+f'\n\n<a href=\"tg://user?id='+str(tg_id)+'\">Связаться с заказчиком</a>'
                url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.PRIVATE_IDs.get(tag)}&text={msg}&parse_mode=HTML"
                data_oo = requests.get(url)
                to_link_message_id(data_oo.json().get("result").get("message_id"), n)
                
                # Отправляем в общий
                msg2 = f"🔥 №<code>{n}</code> - <b>{name}</b>"+'\n\n'+description+f'\n\n<a href="t.me/freelancex_account_bot/?start={n}">Связаться с заказчиком</a>'
                url2 = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.GENERAL_IDs.get(tag)}&text={msg2}&parse_mode=HTML"
                message_id_in_usual_data = requests.get(url2)
                
                # Отправляем уведомление, что выложили объявление
                gg = message_id_in_usual_data.json().get('result')
                link_to_post = str(gg.get("sender_chat").get("username"))+"/"+str(gg.get('message_id'))
                msg_notification = f"Ваше объявление \"<a href=\"https://t.me/"+str(link_to_post)+f'\"><b>{name}</b></a>\" проверено и уже доступно соискателям'
                url_notification = f"https://api.telegram.org/bot{self.TOKEN_notification}/sendMessage?chat_id={tg_id}&text={msg_notification}&parse_mode=HTML"
                requests.get(url_notification)
                return
        return

    def check_delete_post(self):
        data = sql_read_to_delete_pool()
        if data:
            for i in data:
                n, name, description, id, tag, checked, to_1, to_2, link, message_id = i
                if message_id:
                    url = f"https://api.telegram.org/bot{self.TOKEN}/deleteMessage?chat_id={self.PRIVATE_IDs.get(tag)}&message_id={message_id}"
                    requests.get(url)
                    clear_delete_pool(message_id)
        return


def to_link_message_id(message_id, post_id):
    base = sq.connect('./cool.db')
    cur = base.cursor()
    cur.execute("UPDATE main SET message_id = ? WHERE id = ?", (message_id, post_id))
    base.commit()
    base.close()
    return


def clear_delete_pool(message_id):
    base = sq.connect('./cool.db')
    cur = base.cursor()
    cur.execute("DELETE FROM to_delete_pool WHERE message_id = ?", (message_id, ))
    base.commit()
    base.close()
    return


def sql_read_to_delete_pool():
    base = sq.connect('./cool.db')
    cur = base.cursor()
    data = None
    data = cur.execute(f'SELECT * FROM to_delete_pool').fetchall()
    if data:
        return data
    return None


def sql_read(where):
    base = sq.connect('./cool.db')
    cur = base.cursor()
    data = None
    if where == "all":
        data = cur.execute(f'SELECT * FROM main WHERE to_1 = 1 and to_2 = 1 and checked = 1').fetchone()
        if data:
            cur.execute("UPDATE main SET to_2 = 0, to_1 = 0 WHERE id = ?", (data[0],))
    elif where == 'general':
        data = cur.execute(f'SELECT * FROM main WHERE to_1 = 1 and to_2 = 0 and checked = 1').fetchone()
        if data:
            cur.execute("UPDATE main SET to_1 = 0 WHERE id = ?", (data[0],))
    elif where == 'private':
        data = cur.execute(f'SELECT * FROM main WHERE to_1 = 0 and to_2 = 1 and checked = 1').fetchone()
        if data:
            cur.execute("UPDATE main SET to_2 = 0 WHERE id = ?", (data[0],))
    base.commit()
    base.close()
    return data


if __name__ == "__main__":
    # schedule.every(1).minute.do(TelegramPost().post_channel_general)
    # TelegramPost().post_channel_general()
    # schedule.every(1).minute.do(TelegramPost().post_channel_private)
    # TelegramPost().post_channel_private()
    schedule.every(2).hours.do(TelegramPost().post_channel_all)
    TelegramPost().post_channel_all()
    schedule.every(5).minutes.do(TelegramPost().check_delete_post)
    TelegramPost().check_delete_post()
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except:
            time.sleep(10)
            schedule.run_pending()
            time.sleep(5)




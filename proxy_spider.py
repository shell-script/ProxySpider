#!/usr/bin/env python3

from pyrogram import Client
import python3pickledb as pickledb
import re
import logging
import base64
import socket
from telegram.ext import Updater

updater = Updater("123456:abdcefghijklmnopqrszuvwxyz") # Bot_Token | Get it from @BotFather
bot = updater.bot

logging.basicConfig(level=logging.WARN)
api_id = 123456 # API ID | Get it from my.telegram.org
api_hash = "abdcefghijklmnopqrszuvwxyz" # API Hash | Get it from my.telegram.org
where_to_send = '-100123456789' # Channel ID / Group ID

ss = re.compile(r'(ssr?://[a-zA-Z0-9._-]*)')
vmess = re.compile(r'(vmess://[a-zA-Z0-9._-]*)')
mtp = re.compile(r'(server=[a-zA-Z0-9._-]*&port=[a-zA-Z0-9._-]*&secret=[a-zA-Z0-9._-]*)')
socks = re.compile(r'(socks\?server=[a-zA-Z0-9._-]*&port=[a-zA-Z0-9._-]*)')
socks_auth = re.compile(r'(socks\?server=[a-zA-Z0-9._-]*&port=[a-zA-Z0-9._-]*&user=[a-zA-Z0-9._-]*&pass=[a-zA-Z0-9._-]*)')
app = Client("userbot", api_id, api_hash)

def GetMiddleStr(content,startStr,endStr):
  startIndex = content.index(startStr)
  if startIndex>=0:
    startIndex += len(startStr)
  endIndex = content.index(endStr)
  return content[startIndex:endIndex]


def check_ip(ip,port,timeout=5):
    db = pickledb.load('datas.db', True)
    c = db.get(str(ip))
    if c == "True":
        return False
    db.set(str(ip),"True")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip,int(float(port))))
        s.close()
        return True
    except:
        s.close()
        return False

def checkit(ssrlink):
    link = ssrlink.replace("ssr://", "").replace("ss://", "").encode()
    missing_padding = 4 - len(link) % 4
    if missing_padding:
        link += b'='* missing_padding
    server = str(base64.urlsafe_b64decode(link)).replace("b'","").split(":")
    if check_ip(server[0], server[1]):
        return True

def checkit_socks(sockslink):
    if check_ip(GetMiddleStr(sockslink, "server=", "&port"), sockslink.split("&port=")[1]):
        return True

def checkit_socks_auth(socksauthlink):
    if check_ip(GetMiddleStr(socksauthlink, "server=", "&port"), GetMiddleStr(socksauthlink, "port=", "&user")):
        return True

def checkit_vmess(vmesslink):
    import json
    link = vmesslink.replace("vmess://", "").encode()
    missing_padding = 4 - len(link) % 4
    if missing_padding:
        link += b'='* missing_padding
    x = json.loads(base64.urlsafe_b64decode(link).decode())
    if check_ip(x["add"], x["port"]):
        return True

@app.on_message()
def proxy_handler(client, message):
    if message.text == None:
        return
    for i in ss.findall(message.text):
        print("Find link: %s" % i)
        if checkit(i):
            if not (message.chat.username is None):
                bot.send_message(where_to_send, '<code>%s</code>\n\nForward from: @%s | Message ID: %s' % (i, str(message.chat.username), str(message.message_id)), parse_mode="html")
            else:
                bot.send_message(where_to_send, '<code>%s</code>\n\nForward from: %s | Message ID: %s' % (i, str(message.chat.id), str(message.message_id)), parse_mode="html")
    for i in socks_auth.findall(message.text):
        print("Find link: %s" % i)
        if checkit_socks_auth(i):
            if not (message.chat.username is None):
                bot.send_message(where_to_send, 'https://t.me/%s\n\nForward from: @%s | Message ID: %s' % (i, str(message.chat.username), str(message.message_id)), parse_mode="html")
            else:
                bot.send_message(where_to_send, 'https://t.me/%s\n\nForward from: %s | Message ID: %s' % (i, str(message.chat.id), str(message.message_id)), parse_mode="html")
    for i in socks.findall(message.text):
        print("Find link: %s" % i)
        if checkit_socks(i):
            if not (message.chat.username is None):
                bot.send_message(where_to_send, 'https://t.me/%s\n\nForward from: @%s | Message ID: %s' % (i, str(message.chat.username), str(message.message_id)), parse_mode="html")
            else:
                bot.send_message(where_to_send, 'https://t.me/%s\n\nForward from: %s | Message ID: %s' % (i, str(message.chat.id), str(message.message_id)), parse_mode="html")
    for i in vmess.findall(message.text):
        print("Find link: %s" % i)
        if checkit_vmess(i):
            if not (message.chat.username is None):
                bot.send_message(where_to_send, '<code>%s</code>\n\nForward from: @%s | Message ID: %s' % (i, str(message.chat.username), str(message.message_id)), parse_mode="html")
            else:
                bot.send_message(where_to_send, '<code>%s</code>\n\nForward from: %s | Message ID: %s' % (i, str(message.chat.id), str(message.message_id)), parse_mode="html")
    for i in mtp.findall(message.text):
        print("Find link: %s" % i)
        c = i + "&se"
        if check_ip(GetMiddleStr(c,"server=","&port="),int(float(GetMiddleStr(c,"&port=","&se")))):
            if not (message.chat.username is None):
                bot.send_message(where_to_send, 'https://t.me/proxy?%s\n\nForward from: @%s | Message ID: %s' % (i, str(message.chat.username), str(message.message_id)), parse_mode="html")
            else:
                bot.send_message(where_to_send, 'https://t.me/proxy?%s\n\nForward from: %s | Message ID: %s' % (i, str(message.chat.id), str(message.message_id)), parse_mode="html")
app.run()

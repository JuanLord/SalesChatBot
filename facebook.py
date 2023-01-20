from concurrent.futures import thread
from http import client
from fbchat import Client, log
from fbchat.models import *
import apiai, codecs, json
from time import sleep
from getpass import getpass

from numpy import str0

# AI
from chat_botANN import Talking, send_finish_mail
from database_manager import *
from spreadsheets_iphones import is_battery, is_color, is_pesos, is_stock, gb_get

# Send an EMAIL HELP
import smtplib

from getpass import getpass
import regex as re
FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
]
"""
revision = 1
FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
]
username = "luchovarela2000"
client = fbchat.Client(username, getpass())
name = input("Friend? ")
friends = client.searchForUsers(name)
friend = friends[0]
msg = str(input("MESSAGE: "))
sent = client.send(fbchat.models.Message(msg),friend.uid)
if sent:
    print("SENT SUCCESFFUL")
"""

class chatS(Client):
    
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "Access token code"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'en'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None, **kwargs):
        print(thread_id,author_id)

        #user = Client.fetchUserInfo("<5628347480510354>")
        #print("EA SPORTS",user["name"])
        # Check if you talked before
        custom = Client.searchForGroups("Juanmartin · iPhone 11 de 64 gb , sellado")
        print(custom)
        is_know = search_data("client_id",str(thread_id))
        if is_know:
            pass
        else:
            insert_Data(str(thread_id),"","","")

        # GET IPHONE JUST SEE TEXT CHAT MARKETPLACE
        iphones_chat = ["Iphone 8 64gb","Iphone 8 Plus 64 gb","IPhone 8 Plus 64gb","IPhone 8 Plus 256gb","IPhone X 64gb","IPhone X 256gb","IPhone 11 64gb","iPhone 11 de 64 gb , sellado","IPhone 11 128gb","IPhone 11 Pro 64gb","IPhone 11 Pro Max 64gb","11 Pro Max 256gb","IPhone 13 128GB Nuevo Sellado!"]
        for chat in iphones_chat:
            customers = Client.searchForGroups(chat)
            if customers != None:
                for customer in customers:
                    if customer.uid == thread_id:
                        print("Hee Hee")
                        update_Iphone(thread_id,chat)
        """
        print("EEDSS")
        for i in range(10):
            name = "Juanmtin Varela"
            friends = Client.searchForUsers(name)
            friend = friends[0]
            if friend.uid == thread_id:
                print("HEE HEEE")
            else: 
                pass
        """

        # Wait for message

        #log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))
        msgText = message_object.text

        # https://docs.google.com/spreadsheets/d/17TJJgm9T_ESF9D7wbYWvO1lR_AgAjq9wsBwhNSV4zEk/edit?usp=sharing
        # STUFF IN VIDEO
        #self.markAsRead(author_id)
        #self.apiaiCon()
        #self.request.query = msgText
        #response = self.request.getresponse()
        #obj = json.load(response)
        #reply = obj['result']['fulfillment']['speech']
        
        message, topic = Talking(msgText)

        # Send IMG of iphone -> list in intents
        topic_lists = ["iphone8","iphone8 plus","iphonex","iphonexs max","iphone11 de 64gb en caja sellado","iphone11 de 64gb","iphone11 pro","iphone11 pro max","iphone13"]
        color_topics = ["black","gold","green","blue","white"]
        gbtopic = ["64gb","128gb","256gb"]

        if author_id != self.uid:
             # Send picture of specific iPhone
             if topic.lower() in topic_lists:
                if is_stock(topic.lower()):
                    # UPDATE LIKING DATABASE
                    update_Iphone(thread_id,topic.lower())

                    # SEND PHOTO
                    print("Send Photo")
                    path = f"iPhones/{topic.lower()}/iphone.png"
                    self.sendLocalImage(path,message=Message(text="Dejame saber si estas interesado"), thread_id=thread_id, thread_type=thread_type)
                else:
                    # NO STOCK
                    self.send(Message(text="Perdon pero ese telefono no se encuentra en stock, en que otro iphone estarias interesado?"), thread_id=thread_id, thread_type=thread_type)
            # IF ASKS FOR COLORS
             if topic.lower() in color_topics:
                print("color")
                update_color(thread_id,topic)
                row = read_phone(thread_id)
                if row[1] == "":
                    # NO IPHONE
                    self.send(Message(text="Que telefono te gustaria?"), thread_id=thread_id, thread_type=thread_type)
                else:
                    # HAS PHONE
                    print("has phone", row[1])
                    if is_color(topic,row[1]):
                        print("has color")
                        self.send(Message(text="Tengo de ese color!"), thread_id=thread_id, thread_type=thread_type)
                        send_finish_mail(["Hola Lucho,", "Espero que estes bien, acabo de tener un cliente mu potencial que quiere un..",f" el quiere un {row[1]} del color {row[2]}"])
                    else:
                        print("has no color")
                        self.send(Message(text="Perdon, pero no tengo de ese color"), thread_id=thread_id, thread_type=thread_type)

            # IF ASKS FOR BATTERY
             if topic.lower() in "battery":
                row = read_phone(thread_id)
                if row[1] == "":
                    # NO IPHONE
                    self.send(Message(text="Que telefono te gustaria?"), thread_id=thread_id, thread_type=thread_type)
                else:
                    # HAS PHONE
                    self.send(Message(text="El telefono tiene {} de bateria!".format(is_battery())), thread_id=thread_id, thread_type=thread_type)

            # IF ASKS FOR GB
             if topic.lower() in gbtopic:
                print("YEEE")
                row = read_phone(thread_id)
                print("READ")
                if row[1] == "":
                    # NO IPHONE
                    self.send(Message(text="Que telefono te gustaria?"), thread_id=thread_id, thread_type=thread_type)
                else:
                    # HAS PHONE
                    print("YES PHONE")
                    gb = gb_get(row[1],topic.lower())
                    update_gb(thread_id,str(topic))
                    if gb == "no":
                        print("NO GB")
                        self.send(Message(text="Perdon pero no tengo esa memoria"), thread_id=thread_id, thread_type=thread_type)
                    else:
                        print("YES GB")
                        self.send(Message(text="Tengo esa memoria! El {} con {} cuesta {}".format(row[1],topic,gb)), thread_id=thread_id, thread_type=thread_type)
                        send_finish_mail(["Hola Lucho,", "Espero que estes bien, acabo de tener un cliente mu potencial que quiere un..",f" el quiere un {row[1]}, CHAUUU! BYE! BYE! BESITOS!!! <3"])

             if topic.lower() == "tengo":
                row = read_phone(thread_id)
                if row[1] == "":
                    # NO IPHONE
                    self.send(Message(text="Que telefono te gustaria?"), thread_id=thread_id, thread_type=thread_type)
                elif row[2] == "":
                    # NO GB
                    print("NO GB")
                    self.send(Message(text="Cuanto espacio te gustaria que tuviera? tengo de 64gb, 128gb o 256gb"), thread_id=thread_id, thread_type=thread_type)
                else:
                    # HAS PHONE AND GB
                    print("HAS HAS")
                    offer = is_pesos(row[1],row[4])
                    print("HEE HEEE")
                    if "mil" in msgText:
                        # Takes all numbers said and turns it into number
                        list_uy = []
                        num = 0
                        for i in msgText.split():
                            num += 1
                            if i.isdigit():
                                num = 0
                                list_uy.append(int(i))
                        amount = ' '.join(str(e) for e in list_uy)
                        pesos = (int(amount)) * 1000
                        if int(offer) >= pesos:
                            self.send(Message(text="Lo mejor que puedo es {}".format(offer)), thread_id=thread_id, thread_type=thread_type)
                        else:
                            self.send(Message(text="Dale"), thread_id=thread_id, thread_type=thread_type)
                            send_finish_mail(["Hola Lucho,", "Espero que estes bien, acabo de tener un cliente mu potencial que quiere un..",f" el quiere un {row[1]} del color {row[2]} y me hico una oferta irresistible por {pesos} pesos"])
                    else:
                        # Takes all numbers said and turns it into number
                        list_uy = []
                        num = 0
                        for i in msgText.split():
                            num += 1
                            if i.isdigit():
                                num = 0
                                list_uy.append(int(i))
                        amount = ' '.join(str(e) for e in list_uy)
                        pesos = int(amount)
                        if int(offer) >= pesos:
                            self.send(Message(text="Lo mejor que puedo es {}".format(offer)), thread_id=thread_id, thread_type=thread_type)
                        else:
                            self.send(Message(text="Dale"), thread_id=thread_id, thread_type=thread_type)
                            send_finish_mail(["Hola Lucho,", "Espero que estes bien, acabo de tener un cliente mu potencial que quiere un..",f" el quiere un {row[1]} del color {row[2]} y me hico una oferta irresistible por {pesos} pesos"])
             self.send(Message(text=message), thread_id=thread_id, thread_type=thread_type)
            
        
        self.markAsDelivered(author_id, thread_id)

Client = chatS("machinesfromhell@gmail.com", "Lolovarela")
Client.listen()
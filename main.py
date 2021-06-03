import sys
# -*- coding: utf-8 -*-
import wikipedia
import socket
import threading as thread

class ClientThread(thread.Thread):

    def __init__(self,client_socket):
        thread.Thread.__init__(self)
        self.client_socket = client_socket
    def run(self):
        while True:
            print("Listening...")
            person = client_socket.recv(1024).decode("utf8")
            print(person)
            Daten = self.offline(person)
            if Daten == "":
                Daten = self.wikisuche(person)
            print("OK")
            Daten=Daten+"^"
            client_socket.send(Daten.encode("utf8"))
            print("Sended...")
            client_socket.recv(1024).decode('utf8')

    def wikisuche(self,name):
        name2 = ""
        nachname = ""
        Geboren = ""
        Wohnort = ""
        Arbeit = ""
        bild = ""
        wikipedia.set_lang("de")
        # print("Person eingeben:")
        # x=input()
        x = name

        l = 0
        l2 = 1
        for i in x:
            if (i == " "):
                l = l + 1
        for i in x:
            if l == 101:
                nachname = nachname + i
            if i == " ":
                if l == l2:
                    l = 101
                else:
                    l2 = l2 + 1
            if l != 101:
                name2 = name2 + i

        print(wikipedia.suggest(x))
        try:
            a = wikipedia.summary(x)
        except:
            a = wikipedia.summary(wikipedia.suggest(x))
        print(a)
        o = 0
        oo = 0
        r = 0
        for i in a:
            if i == ")":
                break
            if o == 1:
                if r == 1:
                    if i == "n":
                        o = 2
                        r = 4
                    if i == " ":
                        Geboren = Geboren + "i"
                        r = 0
                if i == "i" and oo == 1:
                    r = 1
                if (oo == 1) and (r == 0):
                    Geboren = Geboren + i
                if oo == 3:
                    oo = 1
                if i == "*":
                    oo = 3
                if i == "," and oo == 1:
                    o = 2
                    r = 4
            if o == 2:
                if r == 4:
                    print("")
                    r = 5
                elif r == 5:
                    r = 6
                else:
                    Wohnort = Wohnort + i
            if (i == "("):
                o = 1

        return (name2 + "|" + nachname + "|" + Geboren + "|" + Wohnort + "|" + Arbeit + "|" + a2+ "|" + bild + "|")

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 1234))
    server_socket.listen()
    print("Server is running and waiting for clients on port: ", 1234)

    while True:
        client_socket, addr = server_socket.accept()
        print("Incomming Connection by", addr[0])
        tempClient = ClientThread(client_socket)
        tempClient.start()

    server_socket.close()
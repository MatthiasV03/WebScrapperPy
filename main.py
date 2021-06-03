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
    def speichern(self,name,geboren,wohnort,arbeit,text,bild):
        nachname2 = ""
        name3=""
        l = 0
        l2 = 1
        for i in name:
            if (i == " "):
                l = l + 1
        for i in name:
            if l == 101:
                nachname2 = nachname2 + i
            if i == " ":
                if l == l2:
                    l = 101
                else:
                    l2 = l2 + 1
            if l != 101:
                name3 = name3 + i
        file = open(name+".txt", "a")
        file.write(name3 +"\n" + nachname2 +"\n" + geboren +"\n" + wohnort +"\n"+ arbeit + "\n")
        for i in text:
            try:
                file.write(i)
            except:
                print("Busted:" + i)
        file.write("\n"+bild)
        file.close()
        print("Gespeichert...")


    def offline(self,name):
        try:
            file = open(name + ".txt", "r")
            r = 0
            while (r < 7):
                print(r)
                if r == 0:
                    name2 = file.readline()[:-1]
                if r == 1:
                    nachname = file.readline()[:-1]
                if r == 2:
                    Geboren = file.readline()[:-1]
                if r == 3:
                    Wohnort = file.readline()[:-1]
                if r == 4:
                    Arbeit = file.readline()[:-1]
                if r < 5:
                    text = file.readline()[:-1]
                if r == 6:
                    bild = file.readline()[:-1]
                r = r + 1

            file.close()
            print("Offline vorhanden!!...")
            print(bild)
            return (name2 + "|" + nachname + "|" + Geboren + "|" + Wohnort + "|" + Arbeit + "|" + text + "|" + bild + "|")
        except:
            print("Online Suche starten...")
            return ""


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
        if Geboren == "":
            Geboren = "zwischen "
            b = a.find("zwischen") + 9
            ii = 0
            iii = 0
            u = False
            gw = 0
            for i in a:
                if gw == 1:
                    if i == ",":
                        break
                    if iii == 1:
                        Wohnort = Wohnort + i
                    iii = 1
                if ii >= b and gw == 0:
                    if u == True:
                        if i == "n":
                            gw = 1
                    if i == "i":
                        u = True
                    Geboren = Geboren + i
                ii = ii + 1
            Geboren = Geboren[:(-3)]
        # -------------------------------------------------
        b = a.find("ist ein ") + 8
        b2 = a.find("war ein ") + 8
        b3 = a.find("ist der ") + 8
        b4 = a.find("war der ") + 8
        ii = 0
        # print(str(b) + "|" + str(b2))
        if b == 7:
            b = 1000
        if b2 == 7:
            b2 = 1000
        if b3 == 7:
            b3 = 1000
        if b4 == 7:
            b4 = 1000
        itmp = "o"
        for i in a:
            if ii >= b or ii >= b2 or ii >= b3 or ii >= b4:
                print(".")
                if i == ".":
                    print(itmp)
                    if (itmp == str(1)) or (itmp == str(2)) or (itmp == str(3)) or (itmp == str(4)) or (
                            itmp == str(5)) or (itmp == str(6)) or (itmp == str(7)) or (itmp == str(8)) or (
                            itmp == str(9)) or (itmp == str(0)):
                        pass
                    else:
                        print("iz")
                        break
                Arbeit = Arbeit + i
            ii = ii + 1
            itmp = i
        try:
            ny = wikipedia.page(wikipedia.suggest(name))
        except:
            ny = wikipedia.page(name)
        for i in ny.images:
            if name2 in i and nachname in i:
                print(bild)
                bild = i
                break
        if bild == "":
            for i in ny.images:
                if name2[:-1] in i:
                    print(bild)
                    bild = i
                    break

        if bild == "":
            bild = ny.images[0]
        print(bild)
        print(".."+name2+"..")
        print(".." + nachname + "..")
        a2=""
        rr=0
        for i in a:
            if i =="[" or rr==1:
                rr=1
                print("Not included:" + i)
                if i=="]":
                    rr=0
            else:
                a2=a2+i
        print("Name: " + name2)
        print("Nachname: " + nachname)
        print("Geboren: " + Geboren)
        print("Geburtsort: " + Wohnort)
        print("Arbeit-Unternehmen: " + Arbeit)
        print("Bild: " + bild)
        self.speichern(name,Geboren,Wohnort,Arbeit,a2,bild)
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
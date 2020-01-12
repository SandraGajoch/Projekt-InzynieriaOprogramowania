import sys, glob, os
from tkinter import *
from tkinter import filedialog
import  re
import matplotlib.pyplot as plt
ListaPlikow=[]#lista sciezek dostepu do plikow
pliki=[] #lista nazw plików
poloczeniah1={} #lista polaczen
poloczeniah2={}

#zamykanie okienka interfejsu
def zamknij(zdarzenie):
    okno.quit()
    okno.destroy()

#dodawnie plików
def dodaj(zdarzenie):
    r= filedialog.askopenfilenames(initialdir="/", title="wybierz plik")# , filetypes=(("text files", ".*"), ("all files", ".")))
    licznik=0
    while licznik<len(r):
        ListaPlikow.append(r[licznik])
        str1=ListaPlikow[licznik]
        x=str1.split('/')
        y=x[-1]
        z=y.split('.')
        pliki.append(z[0])
        licznik+=1

def szukaniepolaczenia_pliki(szukane, nazwy, sciezki):
    kontener={} #przechowywanie polaczen
    y=0
    for x in sciezki:
        plik1 = open(sciezki[y])
        plik = plik1.read()
        zbior=[]
        for linia in plik.split('/n'):   # dzieli tekst na linijki
            for wyraz in nazwy:
                znalezienie=linia.find(wyraz) #szuka wyrazów (wart. -1 gdy nie znajdzie)
                if znalezienie>-1:
                    zbior.append(linia[znalezienie:znalezienie+len(wyraz)]) #to trzeba
#                    print(linia[znalezienie:znalezienie+10])
                else:
                    continue
            kontener[nazwy[y]] = zbior #dodaje do słownika znalezione polaczenia
        y+=1
    return kontener

def nazwyfunkcji(sciezki):
    for x in sciezki:
        plik1 = open(x)
        plik = plik1.read()
        szukaj = r"def[\s]+([a-zA-Z_0-9]+)\(.*\)[ ]*\:" #szuka zadanego wzorca, inspiracja https://docs.python.org/3.1/library/re.html
        funkcje = re.findall(szukaj, plik, re.MULTILINE)
        #print(funkcje)
    return funkcje

def szukaniepolaczenia_funkcje(szukane, sciezki):
    kontener={} #przechowywanie polaczen
    y=0
    for x in sciezki:
        plik1 = open(sciezki[y])
        plik = plik1.read()
        z=-1
        for definicja in plik.split('def'+' '):   # dzieli tekst na linijki
            if z==-1:
                z+=1
            else:
                #print(definicja[0:10])
                zbior = []
                for linia in definicja.split('/n'):
                    for wyraz in szukane:
                        znalezienie = linia.find(wyraz)  # szuka wyrazów (wart. -1 gdy nie znajdzie)
                        if znalezienie > -1:
                            zbior.append(definicja[znalezienie:znalezienie + len(wyraz)])  # to trzeba
                        #                    print(linia[znalezienie:znalezienie+10])
                        else:
                            continue
                if len(zbior)>=1:
                    kontener[zbior[0]] = zbior[1:]  # dodaje do słownika znalezione polaczenia
                else:
                    continue
                y+=1
    return kontener

def historyjka1(zdarzenie):
    slowa=['include', 'required', 'import', 'open'] #slowa do szukania
    poloczeniah1 = szukaniepolaczenia_pliki(slowa, pliki, ListaPlikow) #szuka polaczen
    print(poloczeniah1.items()) #wypisuje cały słownik zależności między plikami
    #print(pliki)

def historyjka2(zdarzenie):
    funkcje_nazwy=nazwyfunkcji(ListaPlikow)  # szuka polaczen
    poloczeniah2 = szukaniepolaczenia_funkcje(funkcje_nazwy, ListaPlikow)  # szuka polaczen
    print(poloczeniah2.items())  # wypisuje cały słownik zależności między plikami

def historyjka3(zdarzenie):
    okno.quit()
    okno.destroy()

#rysowanie okienka interfejsu/
okno = Tk()
etykieta = Label(okno, text="Inzynieria oprogramowania", font=("Arial", 24, "italic"))
etykieta.pack(expand=YES, fill=BOTH)
etykieta = Label(okno, text="Historyjka 1: Jako programista, chcę zobaczyć graf pokazujący połączenia pomiędzy plikami z kodem źródłowym w moim projekcie", font=("Arial"))
etykieta.pack(expand=YES, fill=BOTH)
etykieta = Label(okno, text="Historyjka 2: Jako programista chcę zobaczyć graf relacji między funkcjami/metodami w podanym kodzie źródłowym, w celu analizy zależności w kodzie źródłowym.", font=("Arial"))
etykieta.pack(expand=YES, fill=BOTH)
etykieta = Label(okno, text="Historyjka 3: Jako architekt oprogramowania chcę zobaczyć graf relacji między modułami logicznymi* w podanym kodzie źródłowym, w celu analizy zależności w programie.", font=("Arial"))
etykieta.pack(expand=YES, fill=BOTH)
przycisk1 = Button(okno, text="Dodaj pliki",font=("Arial", 16, "bold"))
przycisk1.bind("<Button-1>", dodaj)
przycisk1.pack(fill=X)
przycisk2 = Button(okno, text="Historyjka 1",font=("Arial", 16, "bold"))
przycisk2.bind("<Button-1>", historyjka1)
przycisk2.pack(fill=X)
przycisk3 = Button(okno, text="Historyjka 2",font=("Arial", 16, "bold"))
przycisk3.bind("<Button-1>", historyjka2)
przycisk3.pack(fill=X)
przycisk4 = Button(okno, text="Historyjka 3",font=("Arial", 16, "bold"))
przycisk4.bind("<Button-1>", historyjka3)
przycisk4.pack(fill=X)
przycisk5 = Button(okno, text="Zamknij",font=("Arial", 16, "bold"))
przycisk5.bind("<Button-1>", zamknij)
przycisk5.pack(fill=X)
okno.mainloop()

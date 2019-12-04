import sys, glob, os
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
ListaPlikow=[]#lista sciezek dostepu do plikow
pliki=[] #lista nazw plików
poloczenia={} #lista polaczen

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

def szukaniepolaczenia(szukane, nazwy, sciezki):
    kontener={} #przechowywanie polaczen
    y=0
    for x in sciezki:
        plik1 = open(ListaPlikow[y])
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
            kontener[nazwy[y]] = zbior
        y+=1
    return kontener


def historyjka1(zdarzenie):
    slowa=['include', 'required', 'import', 'open'] #slowa do szukania
    poloczenia = szukaniepolaczenia(slowa, pliki, ListaPlikow)
    print(poloczenia.items())
    print(pliki)
    i=generate_edges(poloczenia)
    print(i)

def historyjka2(zdarzenie):
    okno.quit()
    okno.destroy()

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

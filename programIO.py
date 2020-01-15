import sys, glob, os
from tkinter import *
from tkinter import filedialog
import re
import matplotlib.pyplot as plt
from IPython.display import Image, display
import pydot
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

ListaPlikow=[]#lista sciezek dostepu do plikow
pliki=[] #lista nazw plików
poloczeniah1={} #lista polaczen plikow
poloczeniah2={} #lista poloczen funkcji

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
            wystepowanie = {}
            for c in zbior:
                wystepowanie[c] = wystepowanie.get(c, 0) + 1
            # print(wystepowanie)
            kontener[nazwy[y]] = wystepowanie #dodaje do słownika znalezione polaczenia
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
                    wystepowanie = {}
                    a=zbior[0]
                    zbior1=zbior[1:]
                    for c in zbior1:
                        wystepowanie[c] = wystepowanie.get(c, 0) + 1
                    # print(wystepowanie)
                    kontener[a] = wystepowanie  # dodaje do słownika znalezione polaczenia
                else:
                    continue
                y+=1
    return kontener

# przyjmuje jeden argument 'relationshipMap' ktyry wygląda tak:
# dict_items(
#	[
#		('task', {}),
# 		('result', {}), 
#		('ReadFileXlsx', 	{'task': 1, 'result': 1}), 
#		('programIO', {})
#	]
#)
def createDirectedGraphs(relationshipMap):  
    G = nx.DiGraph() # włączenie diagramu skierowanego
    G.add_nodes_from(relationshipMap.items()) # dodaje wszystki punkty (nazwy plików) (nazwy plików) ['task', 'result', 'ReadFileXlsx', 'programIO'] | G.add_node -osobne dodawanie 
    pairNode = [] # pary punktów potrzebne do pomalowania itp ('task', 'result'), ('result', 'ReadFileXlsx')
                  # to znaczy, ze miedzy tymi punktami bedzie kreska i strzałka 

    # petle robia relacje miedzy nodami G.add_edges_from([(k, key)]  
    # ustawiaja wagi weight=value  
    # oraz dodaje pary do pairNode.append((k, key))
    for k, v in relationshipMap.items(): 
        for key, value in v.items():
            G.add_edges_from([(k, key)], weight=value)
            pairNode.append((k, key))

    pairWeight =dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)]) # ustaw wagi 

    pos = nx.spring_layout(G) # ustaw layout

    # wlasciwosci nodow ustaw kolor node_color = 'red' 
    # ustaw rozmiar node_size = 500
    nx.draw_networkx_nodes(G, pos, node_color = 'red', node_size = 500) 
    nx.draw_networkx_labels(G, pos) # ustaw napisy na nodach 

    # wlasciwosci strzalek. co polaczyc edgelist=pairNode 
    # kolor strzalek edge_color='black' 
    # uruchomienie strzalek arrows=True
    nx.draw_networkx_edges(G, pos, edgelist=pairNode, edge_color='black', arrows=True) 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pairWeight) # wlacza numery z wagami na strzalkach

    plt.show() # pokazuje okno

def historyjka1(zdarzenie):
    slowa=['include', 'required', 'import', 'open'] #slowa do szukania
    poloczeniah1 = szukaniepolaczenia_pliki(slowa, pliki, ListaPlikow) #szuka polaczen
    print(poloczeniah1.items()) #wypisuje cały słownik zależności między plikami
    print(pliki)
    createDirectedGraphs(poloczeniah1)
    

def historyjka2(zdarzenie):
    funkcje_nazwy=nazwyfunkcji(ListaPlikow)  # szuka polaczen
    poloczeniah2 = szukaniepolaczenia_funkcje(funkcje_nazwy, ListaPlikow)  # szuka polaczen
    print(poloczeniah2.items())  # wypisuje cały słownik zależności między plikami
    createDirectedGraphs(poloczeniah2)

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
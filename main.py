import re
from wyciąganie_tekstu import *
import time
from regexy import *
from forex_python.converter import CurrencyRates
# from csv_reader import *

def z_euro_na_złotego(wartosc_euro):
    return wartosc_euro*4.2
def wyszukiwanie_wszystkich_wystąpień(tekst,fraza):
    fraza=fraza.replace("?:","")
    fraza=fraza.replace("(","(?:").replace("?:?<!","?<!").replace("\(?:","\(")
    return re.findall(fraza,tekst,re.DOTALL|re.IGNORECASE)

def widły(tekst,fraza_początkowa=r"21372137///xD",fraza_końcowa=r"21372137///xD"):
    fraza_początkowa=fraza_początkowa.replace("(","(?:").replace("?:?<!","?<!").replace("\(?:","\(")
    fraza_końcowa=fraza_końcowa.replace("(","(?:").replace("?:?<!","?<!").replace("\(?:","\(")
    lista_fragmentów=[]
    for fragment in re.split(fraza_początkowa,tekst,re.DOTALL|re.IGNORECASE)[1:]:
        # if re.search(fraza_końcowa,fragment,re.DOTALL|re.IGNORECASE):
        #     for fragment_kupującego in re.split(fraza_końcowa,fragment,re.DOTALL|re.IGNORECASE)[:-1]:
        #         lista_fragmentów.append(fragment_kupującego)
        # else: lista_fragmentów.append(fragment)
        lista_fragmentów.append(re.split(fraza_końcowa,fragment,re.DOTALL|re.IGNORECASE)[0])
    return lista_fragmentów

def wyciąganie_ceny_całkowitej(text_file):
    start_time=time.time()
    text=read_from_text(text_file)
    podzielony=re.split("PAGE",text)
    lines=[]
    lines.append(["Suma cen"])
    for i,strona in enumerate(podzielony[1:]):
        print(f"--WIERSZ-- {i+2}")
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['sale']))
        print(len(widły(strona,pattern['sale'])))
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['buy']))
        print(f'całe:{wyszukiwanie_wszystkich_wystąpień(strona,pattern['łączna_cena'])}')
        print(f'łączna_i_słowna:{wyszukiwanie_wszystkich_wystąpień(strona,pattern["cena_łączna_i_słowna"])}')
        fragmenty = widły(strona,pattern['sale'],pattern['buy'])
        suma_cen=0
        for fragment in fragmenty:
            if re.search(r'brutto',fragment,re.DOTALL|re.IGNORECASE) and re.search(r'netto',fragment,re.DOTALL|re.IGNORECASE):
                fragment=re.split(r'netto',fragment,re.DOTALL|re.IGNORECASE)[0]
            print(f'kupione:{wyszukiwanie_wszystkich_wystąpień(fragment,pattern['łączna_cena'])}')
            print("=++=++=++=++=++=++=++=")
            print(fragment)
            print("=++=++=++=++=++=++=++=")
            # -- Mityczny etap 0 --
            if len(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['cena_łączna_i_słowna']))>0:
                perfekcja=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['cena_łączna_i_słowna'])[0]
                cena_słowna=wyszukiwanie_wszystkich_wystąpień(perfekcja,pattern['cena_słowna'])[0]
                print(cena_słowna)
                obecna=suma_cen
                if z_postaci_słownej_do_numerycznej(cena_słowna)!=-1 and len(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['cena_po_ileś']))==0:
                    suma_cen+=z_postaci_słownej_do_numerycznej(cena_słowna)
                else:
                    suma_cen=obecna
                    lista_cen=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['Cena'])
                    print(lista_cen)
                    for cena in lista_cen:
                        if cena[:2]!='po':
                            cena=wyszukiwanie_wszystkich_wystąpień(cena,r'\d+([\., ]\d+)?([\.,]\d+)?')[0]
                            cena=re.sub(r'[\.,]\d{2}\b','',cena)
                            cena=re.sub(r'[,\. \n]','',cena)
                            suma_cen+=int(cena)
                    print("ETAP 3")
                print("ETAP 0")
            # -- Najlepszy przypadek, kiedy znajdziemy łączną cenę sprzedaży --
            elif len(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['łączna_cena']))>0:
                łączne=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['łączna_cena'])[0]
                łączne=re.sub(r'[\.,]\d{2}\b','',łączne)
                łączne=re.sub(r'[,\. \n]','',łączne)
                suma_cen+=int(wyszukiwanie_wszystkich_wystąpień(łączne,r'\d+')[-1])
                print("ETAP 1")
            # -- Słowne ceny sprzedaży we fragmentach, bo są on mniej podatne na zakłócenia --
            elif len(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['cena_słowna']))>0:
                słowne=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['cena_słowna'])
                print(słowne)
                obecna=suma_cen
                for cena_słowna in słowne:
                    if z_postaci_słownej_do_numerycznej(cena_słowna)!=-1 and len(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['cena_po_ileś']))==0:
                        suma_cen+=z_postaci_słownej_do_numerycznej(cena_słowna)
                    else:
                        suma_cen=obecna
                        lista_cen=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['Cena'])
                        print(lista_cen)
                        for cena in lista_cen:
                            if cena[:2]!='po':
                                cena=wyszukiwanie_wszystkich_wystąpień(cena,r'\d+([\., ]\d+)?([\.,]\d+)?')[0]
                                cena=re.sub(r'[\.,]\d{2}\b','',cena)
                                cena=re.sub(r'[,\. \n]','',cena)
                                suma_cen+=int(cena)
                        print("ETAP 3")
                print("ETAP 2")
            # -- Zwykłe ceny sprzedaży --
            elif len(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['Cena']))>0:
                lista_cen=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['Cena'])
                print(lista_cen)
                for cena in lista_cen:
                    czy_euro=False
                    if cena[:2]!='po':
                        if re.search('euro',cena,re.DOTALL|re.IGNORECASE):
                            czy_euro=True
                        cena=wyszukiwanie_wszystkich_wystąpień(cena,r'\d+([\., ]\d+)?([\.,]\d+)?')[0]
                        cena=re.sub(r'[\.,]\d{2}\b','',cena)
                        cena=re.sub(r'[,\. \n]','',cena)
                        if czy_euro:
                            print("EURO wykryte")
                            cena=z_euro_na_złotego(int(cena))
                        suma_cen+=int(cena)
                print("ETAP 3")
        # -- Jak nic nie znajdzie we fragmentach to bierze największą znalezioną łączną cenę z całej strony --
        if suma_cen==0 and len(wyszukiwanie_wszystkich_wystąpień(strona,pattern['łączna_cena']))>0:
            łączne=wyszukiwanie_wszystkich_wystąpień(strona,pattern['łączna_cena'])
            for i,łączny in enumerate(łączne):
                łączny=re.sub(r'[\.,]\d{2}\b','',łączny)
                łączny=re.sub(r'[,\. \n]','',łączny)
                łączne[i]=int(wyszukiwanie_wszystkich_wystąpień(łączny,r'\d+')[-1])
            suma_cen+=max(łączne)
            print("ETAP 4")
        # -- Alternatywna wersja etapu 4 jeśli znajddzie ceny, ale potem znajdzie większą cenę łączną
        elif len(wyszukiwanie_wszystkich_wystąpień(strona,pattern['łączna_cena']))>0:
            łączne=wyszukiwanie_wszystkich_wystąpień(strona,pattern['łączna_cena'])
            for i,łączny in enumerate(łączne):
                łączny=re.sub(r'[\.,]\d{2}\b','',łączny)
                łączny=re.sub(r'[,\. \n]','',łączny)
                łączne[i]=int(wyszukiwanie_wszystkich_wystąpień(łączny,r'\d+')[-1])
            if max(łączne)>suma_cen:
                suma_cen=max(łączne)
                print("ETAP 4")
        # -- W ostateczności bierze jedyną cenę jaką znajdzie --
        elif suma_cen==0 and len(wyszukiwanie_wszystkich_wystąpień(strona,pattern['Cena']))>0:
            cena=wyszukiwanie_wszystkich_wystąpień(strona,pattern['Cena'])[0]
            if cena[:2]!='po':
                cena=wyszukiwanie_wszystkich_wystąpień(cena,r'\d+([\., ]\d+)?([\.,]\d+)?')[0]
                cena=re.sub(r'[\.,]\d{2}\b','',cena)
                cena=re.sub(r'[,\. \n]','',cena)
                suma_cen+=int(cena)
            print("ETAP 5")
        lines.append([suma_cen])
        print(f"Suma cen: {suma_cen}")        
            
    end_time=time.time()
    execution_time=end_time-start_time
    print(f"Czas wykonania: {execution_time}")
    return lines

def z_postaci_słownej_do_numerycznej(text):
    slownik_liczb = {
    # Jedności
    "jeden": 1, "jednego": 1, "jednemu": 1, "jednym": 1,
    "dwa": 2, "dwóch": 2, "dwom": 2, "dwoma": 2,
    "trzy": 3, "trzech": 3, "trzem": 3, "trzema": 3,
    "cztery": 4, "czterech": 4, "czterem": 4, "czterema": 4,
    "pięć": 5, "pięciu": 5,
    "sześć": 6, "sześciu": 6,
    "siedem": 7, "siedmiu": 7,
    "osiem": 8, "ośmiu": 8,
    "dziewięć": 9, "dziewięciu": 9,
    
    # Dziesiątki
    "dziesięć": 10, "dziesięciu": 10,
    "jedenaście": 11, "jedenastu": 11,
    "dwanaście": 12, "dwunastu": 12,
    "trzynaście": 13, "trzynastu": 13,
    "czternaście": 14, "czternastu": 14,
    "piętnaście": 15, "piętnastu": 15,
    "szesnaście": 16, "szesnastu": 16,
    "siedemnaście": 17, "siedemnastu": 17,
    "osiemnaście": 18, "osiemnastu": 18,
    "dziewiętnaście": 19, "dziewiętnastu": 19,
    "dwadzieścia": 20, "dwudziestu": 20,
    "trzydzieści": 30, "trzydziestu": 30,
    "czterdzieści": 40, "czterdziestu": 40,
    "pięćdziesiąt": 50, "pięćdziesięciu": 50,
    "sześćdziesiąt": 60, "sześćdziesięciu": 60,
    "siedemdziesiąt": 70, "siedemdziesięciu": 70,
    "osiemdziesiąt": 80, "osiemdziesięciu": 80,
    "dziewięćdziesiąt": 90, "dziewięćdziesięciu": 90,
    
    # Setki
    "sto": 100, "stu": 100,
    "dwieście": 200, "dwustu": 200,
    "trzysta": 300, "trzystu": 300,
    "czterysta": 400, "czterystu": 400,
    "pięćset": 500, "pięciuset": 500,
    "sześćset": 600, "sześciuset": 600,
    "siedemset": 700, "siedmiuset": 700,
    "osiemset": 800, "ośmiuset": 800,
    "dziewięćset": 900, "dziewięciuset": 900,
    "":0," ":0,"\n":0
    }
    odmiana_tysięcy=["tysiąc","tysięcy","tysiące"]
    odmiana_milionów=["milion","miliony","milionów"]
    czy_euro=False
    text=re.sub(r'\(','',text)
    text=re.sub(r'\)','',text)
    text=re.sub(r'złot(e|ych)','',text)
    if re.search(r'euro',text):
        text=re.sub(r'euro','',text)
        czy_euro=True
    text=re.sub(r' i.*?grosz[ey]','',text,re.DOTALL|re.IGNORECASE)
    text=re.sub(r'\n',' ',text)
    text=re.sub("zł","",text)
    suma=0
    podział1=re.split(r'milionów|miliony|miliona|milion',text,re.DOTALL|re.IGNORECASE)
    if len(podział1)>1:
        for slowo in podział1[0].split(" "):
            if slowo in slownik_liczb:
                suma+=slownik_liczb[slowo]*1000000
            else:
                print(slowo)
                return -1
        text=podział1[1]
    podział2=re.split(r'tysiąca|tysiące|tysięcy|tysiąc',text,re.DOTALL|re.IGNORECASE)
    if len(podział2)>1:
        for slowo in podział2[0].split(" "):
            if slowo in slownik_liczb:
                suma+=slownik_liczb[slowo]*1000
            else:
                print(slowo)
                return -1
        text=podział2[1]
    for slowo in text.split(" "):
        if slowo in slownik_liczb:
            suma+=slownik_liczb[slowo]
        else:
            print(slowo)
            return -1
    if czy_euro:
        print("EURO wykryte")
        return z_euro_na_złotego(int(suma))
    return suma

def wyciąganie_powierzchni_całkowitej(text_file):
    start_time=time.time()
    text=read_from_text(text_file)
    podzielony=re.split("PAGE",text)
    lines=[]
    lines.append(["Suma powierzchni"])
    for i,strona in enumerate(podzielony[1:]):
        udziały=False
        print(f"--WIERSZ-- {i+2}")
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['sale']))
        print(len(widły(strona,pattern['sale'])))
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['buy']))
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['słownik_numer_powierzchnia']))
        numer_do_powierzchni={}
        pary=wyszukiwanie_wszystkich_wystąpień(strona,pattern['słownik_numer_powierzchnia'])
        for i,para in enumerate(pary):
            para=re.sub(",",".",para)
            numer=wyszukiwanie_wszystkich_wystąpień(para,r'\d+(/\d+)?')[0]
            powierzchnia=int(float(wyszukiwanie_wszystkich_wystąpień(para,r'\d+[\.,]\d+')[-1])*10000)
            numer_do_powierzchni[numer]=powierzchnia
        print(numer_do_powierzchni)
        wyszukane=wyszukiwanie_wszystkich_wystąpień(strona,pattern['powierzchnia'])
        for i,wyszukany in enumerate(wyszukane):
            wyszukany=re.sub(",",".",wyszukany)
            wyszukane[i]=float(wyszukiwanie_wszystkich_wystąpień(wyszukany,r'\d+[\.,]\d+')[0])*10000
        if len(set(wyszukane))==1:
            lines.append([wyszukane[0]])
        elif len(numer_do_powierzchni)==1:
            lines.append([list(numer_do_powierzchni.values())[0]])
        else:
            fragmenty = widły(strona,pattern['sale'],pattern['buy'])
            for i,fragment in enumerate(fragmenty):
                if re.search(pattern['udział_w_drodze'],fragment,re.DOTALL|re.IGNORECASE):
                    udziały=True
                fragmenty[i]=re.split(pattern['udział_w_drodze'],fragment,re.DOTALL|re.IGNORECASE)[0]
            lista_powierzchni=[]
            for fragment in fragmenty:
                lista_powierzchni+=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['powierzchnia'])
            print(lista_powierzchni)
            for i,powierzchnia in enumerate(lista_powierzchni):
                powierzchnia=re.sub('\n'," ",powierzchnia)
                powierzchnia=re.sub(r"[Hh]a","",powierzchnia)
                powierzchnia=re.sub(",",".",powierzchnia)
                powierzchnia=re.sub(r'obszaru|powierzchni|pow\.',"",powierzchnia,re.DOTALL|re.IGNORECASE)
                powierzchnia=re.sub(" ","",powierzchnia)
                lista_powierzchni[i]=float(powierzchnia)*10000
            print(lista_powierzchni)
            suma_powierzchni=[sum([x for x in lista_powierzchni])]
            if(len(lista_powierzchni)>2):
                if(abs(suma_powierzchni[0]-lista_powierzchni[-1]*2)<1):
                    print("AA")
                    suma_powierzchni[0]/=2
            print(suma_powierzchni)
            if suma_powierzchni==[0] and udziały:
                suma_powierzchni=["UDZIAŁ"]
            lines.append(suma_powierzchni)
    end_time=time.time()
    execution_time=end_time-start_time
    print(f"Czas wykonania: {execution_time}")
    return lines

def wyciąganie_daty(text_file):
    text=read_from_text(text_file)
    podzielony=re.split("PAGE",text)
    lines=[]
    lines.append(["Data"])
    for i,strona in enumerate(podzielony[1:]):
        print(f"--WIERSZ-- {i+2}")
        if wyszukiwanie_wszystkich_wystąpień(strona,pattern['data']):
            print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['data'])[0])
            lines.append([wyszukiwanie_wszystkich_wystąpień(strona,pattern['data'])[0]])
        else:
            lines.append([""])
            print(strona)
    return lines

def wyciąganie_numeru_repetytorium(text_file):
    text=read_from_text(text_file)
    podzielony=re.split("PAGE",text)
    lines=[]
    lines.append(["Numer repetytorium"])
    for i,strona in enumerate(podzielony[1:]):
        print(f"--WIERSZ-- {i+2}")
        wyszukane=wyszukiwanie_wszystkich_wystąpień(strona,pattern['numer_repetytorium'])
        if(len(wyszukane)>0):
            print(wyszukane[0])
            lines.append([wyszukane[0]])
        else:
            lines.append([""])
    return lines

def wyciąganie_numerów_działek(text_file):
    text=read_from_text(text_file)
    podzielony=re.split("PAGE",text)
    lines=[]
    lines.append(["Numer działki"])
    for i,strona in enumerate(podzielony[1:]):
        print(f"--WIERSZ-- {i+2}")
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['sale']))
        print(len(widły(strona,pattern['sale'])))
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['buy']))
        fragmenty = widły(strona,pattern['sale'],pattern['buy'])
        lista_numerów=[]
        numer_do_powierzchni={}
        pary=wyszukiwanie_wszystkich_wystąpień(strona,pattern['słownik_numer_powierzchnia'])
        for i,para in enumerate(pary):
            para=re.sub(",",".",para)
            numer=wyszukiwanie_wszystkich_wystąpień(para,r'\d+(/\d+)?')[0]
            powierzchnia=int(float(wyszukiwanie_wszystkich_wystąpień(para,r'\d+[\.,]\d+')[-1])*10000)
            numer_do_powierzchni[numer]=powierzchnia
        print(numer_do_powierzchni)
        if len(numer_do_powierzchni)==1:
            lines.append([list(numer_do_powierzchni.keys())[0]])
        else:
            for fragment in fragmenty:
                fragment=re.split(r'zapłacił|zapłata|zapłatę|zapłaty',fragment,re.DOTALL|re.IGNORECASE)[0]
                # if re.search(r'działek([.,:])?',fragment,re.DOTALL|re.IGNORECASE):
                #     od_działek=re.split(r'działek',fragment,re.DOTALL|re.IGNORECASE)[1]
                #     if od_działek and re.search(r'pow|obsz',od_działek,re.DOTALL|re.IGNORECASE):
                #         do_pow=re.split(r'pow|obsz',od_działek,re.DOTALL|re.IGNORECASE)[0]
                #         print("DD")
                #         lista_numerów+=wyszukiwanie_wszystkich_wystąpień(do_pow,r'\d+(/\d+)?')
                print("=++=++=++=++=++=++=++=")
                print(fragment)
                print("=++=++=++=++=++=++=++=")
                print(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['numer_działki']))
                print(wyszukiwanie_wszystkich_wystąpień(fragment,pattern['numery_wielokrotne_iteracja']))
                lista_numerów+=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['numer_działki'])
                lista_numerów+=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['numery_wielokrotne_iteracja'])
            for i,numer in enumerate(lista_numerów):
                # numer=re.sub("\n","",numer)
                # numer=re.sub(" ","",numer)
                lista_numerów[i]=wyszukiwanie_wszystkich_wystąpień(numer,r'\d+(/\d+)?')[-1]
            lista_złączona=",".join(set(lista_numerów))
            # lista_złączona=re.sub("obsz","",lista_złączona)
            # lista_złączona=re.sub("opow","",lista_złączona)
            # lista_złączona=re.sub(r'\(.*?\)','',lista_złączona)
            print(lista_złączona)
            lines.append([lista_złączona])
    return lines

def wyciąganie_obrębu(text_file):
    text=read_from_text(text_file)
    podzielony=re.split("PAGE",text)
    lines=[]
    istniejące=set()
    lines.append(["Obręb"])
    for i,strona in enumerate(podzielony[1:]):
        print(f"--WIERSZ-- {i+2}")
        print(wyszukiwanie_wszystkich_wystąpień(strona,pattern['miejscowosc']))
        # fragmenty = widły(strona,pattern['sale'],pattern['buy'])
        # lista_obrębów=[]
        # lista_obrębów+=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['miejscowosc'])[0]
        # for fragment in fragmenty:
        #     lista_obrębów+=wyszukiwanie_wszystkich_wystąpień(fragment,pattern['obręb'])
            
        # print(lista_obrębów)
        if wyszukiwanie_wszystkich_wystąpień(strona,pattern['pomiejscowosc']):
            wybrany=wyszukiwanie_wszystkich_wystąpień(strona,pattern['pomiejscowosc'])[0]
        else:
            lista_miejscowosci=wyszukiwanie_wszystkich_wystąpień(strona,pattern['miejscowosc'])
            for miejscowosc in lista_miejscowosci:
                miejscowosc=re.sub(r'obręb(ie)?([ \n]ewidencyjn(ym|y))?','',miejscowosc)
                miejscowosc=re.sub(r'położon(y|ej|a|ą|ych|e)([ \n]jest)?[ \n]w(e)?([ \n]miej[sś][cć]ow[ou]ści)?([ \n]wsi)?','',miejscowosc)
                if not re.search(r'wojewódz|teren|miejsco|obręb|kontur|obszar|opisan|gmini|Akt not|\d+',miejscowosc,re.DOTALL|re.IGNORECASE):
                    wybrany=miejscowosc
                    break
        wybrany=re.sub(r'obręb(ie)?([ \n]ewidencyjn(ym|y))?','',wybrany)
        wybrany=re.sub(r'położon(y|ej|a|ą|ych|e)([ \n]jest)?[ \n]w(e)?([ \n]miej[sś][cć]ow[ou]ści)?([ \n]wsi)?','',wybrany)
        wybrany=re.sub(r' oznaczon[yea]\b| gmina\b| nie\b| zlokalizowan[ea]\b','',wybrany)    
        # if len(lista_obrębów)>0:
        #     wybrany=lista_obrębów[0]
        
        print([wybrany])
        lines.append([wybrany])
    #     if wybrany!="":
    #         istniejące.add(wybrany)
    # print(istniejące)
    # for i,strona in enumerate(podzielony[1:]):
    #     # print(f"--WIERSZ-- {i+2}")
    #     if lines[i]==[""]:
    #         lista_obrębów=wyszukiwanie_wszystkich_wystąpień(strona,pattern['obręb'])
    #         for obręb in lista_obrębów:
    #             for istniejący in istniejące:
    #                 if istniejący in obręb and istniejący!="miejscowości":
    #                     # print("ZNALEZIONO")
    #                     lines[i]=[istniejący]
    return lines

lines = [a + b + c + d + e + f for a, b, c,d,e,f in zip(wyciąganie_daty(text_file),wyciąganie_numeru_repetytorium(text_file),wyciąganie_obrębu(text_file),wyciąganie_ceny_całkowitej(text_file),wyciąganie_powierzchni_całkowitej(text_file),wyciąganie_numerów_działek(text_file))]
input_data_into_excel("output/b.xlsx",lines)
# print(lines)
# text=extract_text_from_folder(folder)
# write_string_to_file(text_file,text)
# wyciąganie_numerów_działek(text_file)
# wyciąganie_ceny_całkowitej(text_file)
# wyciąganie_powierzchni_całkowitej(text_file)
# wyciąganie_obrębu(text_file)
# wyciąganie_daty(text_file)
# wyciąganie_numeru_repetytorium(text_file)
# a="(stu dziewięćdziesięciu czterech tysięcy złotych)"
# print(z_postaci_słownej_do_numerycznej(a))
    
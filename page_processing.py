# elaborazione delle pagine
import requests #vari import
from bs4 import BeautifulSoup as bs
import os
import locale
limite_elementi = 5
media = None

def amazon(scheda):  # parte di amazon
    info_schede = {"nome" : [], "prezzo" : [],"link" : []}
    index = 1
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})  # definiamo l'user agent
                
    url = "https://www.amazon.it/s?k=rtx+" + str(scheda)
    
    webpage = requests.get(url, headers=HEADERS)
    soup = bs(webpage.content, "html.parser")

    #recupero il percorso file
    current_dir = os.path.dirname(__file__)
    nome_scheda = "amazon_rtx" + str(scheda) + ".html" 
    file_path = current_dir + "\\"+ nome_scheda # creo il percorso file della pagina html

    #elimino il file già esistente
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Il file {file_path} è stato eliminato.")
        print("\n")
    else:
        print(f"Il file {file_path} non esiste.")
        print("\n")

    #qui vado a salvare la pagina html
    with open(current_dir + '/' + nome_scheda, 'w', encoding= "utf-8") as f:
        f.write(soup.prettify())
    #qui vado a fare tutte le operazioni sulla pagina 
    with open(nome_scheda, "r", encoding="utf-8") as htmlfile:
        soup = bs(htmlfile, "html.parser")
        #qui vado a prendere il link del prodotto per l'iterazione
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})        

        #Qui inizio a prendere i link della pagina della ricerca
        links_list = []
   
        elementi_aggiunti = 0

        for link in links:
            if elementi_aggiunti >= limite_elementi: #limito il numero di elementi per la ricerca
                break
            links_list.append(link.get('href'))
            elementi_aggiunti += 1

       

        for link in links_list: #qui vado cercare tutti i link correlati
            link_prodotto = "https://www.amazon.it" + link
            new_webpage = requests.get(link_prodotto, headers=HEADERS)
            new_soup = bs(new_webpage.content, "html.parser")

            try:#controlo che ci sia il nome del prodotto
                title = new_soup.find("span", attrs={"id": 'productTitle'})
                #qui vado a convertire il titolo in stringa e tolgo gli spazi
                title_str = title.string.strip()
                info_schede["nome"].append(title_str)
                info_schede["link"].append(link_prodotto)
            except AttributeError:
                title_str = ""

            try:#qui vado a recupero il prezzo del prodotto
                price = new_soup.find('span', attrs={'class': 'a-offscreen'}).string.strip()
                info_schede["prezzo"].append(price)
            except AttributeError:
                price = ""
    return info_schede



def akinformatica(scheda): #parte di akinformatica
    info_schede = {"nome" : [], "prezzo" : [],"link" : []}
    
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})  # definiamo l'user agent
                
    url = "https://shop.akinformatica.it/shop/?product-category=schede-video&disponibilita=in-stock&attributo-modello-gpu=geforce-rtx-" + str(scheda)
    
    webpage = requests.get(url, headers=HEADERS)
    soup = bs(webpage.content, "html.parser")

    current_dir = os.path.dirname(__file__)
    nome_scheda = "akinformatica_rtx" + str(scheda) + ".html" 
    file_path = current_dir + "\\"+ nome_scheda # creo il percorso file della pagina html

    #elimino il file già esistente
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Il file {file_path} è stato eliminato.")
        print("\n")
    else:
        print(f"Il file {file_path} non esiste.")
        print("\n")

    #qui vado a salvare la pagina html
    with open(current_dir + '/' + nome_scheda, 'w', encoding= "utf-8") as f:
        f.write(soup.prettify())

    #qui vado a fare tutte le operazioni sulla pagina 
    with open(nome_scheda, "r", encoding="utf-8") as htmlfile:
        soup = bs(htmlfile, "html.parser")
        #qui vado a prendere il link del prodotto per l'iterazione
        links = soup.find_all("a", attrs={'class':'woocommerce-LoopProduct-link woocommerce-loop-product__link'})        

        #Qui inizio a prendere i link della pagina della ricerca
        links_list = []
        elementi_aggiunti = 0

        for link in links:
            if elementi_aggiunti >= limite_elementi: #limito il numero di elementi per la ricerca
                break
            links_list.append(link.get('href'))
            elementi_aggiunti += 1

       
        for link in links_list: #qui vado cercare tutti i link correlati
           
            new_webpage = requests.get(link, headers=HEADERS)
            new_soup = bs(new_webpage.content, "html.parser")

            try:#controlo che ci sia il nome del prodotto
                title = new_soup.find("h1", attrs={"class": 'product_title entry-title'})
                #qui vado a convertire il titolo in stringa e tolgo gli spazi
                title_str = title.string.strip()
                info_schede["nome"].append(title_str)
                info_schede["link"].append(str(link))
            except AttributeError:
                title_str = ""

            try:#qui vado a prendere il prezzo del prodotto se viene trovato
                price = new_soup.find('bdi')
                price_str = price.get_text().strip() #qui recupero il prezzo con il tag bdi
                info_schede["prezzo"].append(price_str)
            except AttributeError:
                price = ""
    return info_schede



def nexths(scheda): #parte di nexths--------------------------------------------------------
    info_schede = {"nome" : [], "prezzo" : [],"link" : []}
    
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})  # definiamo l'user agent
                
    url = "https://www.nexths.it/Products/getSkuFromLev/page/1/l0/Hardware%20Software/l1/Schede%20Video/filterStore/Sede/filterAttributi/Modelli%20GPU%3DGeForce%20RTX" + str(scheda)
    
    webpage = requests.get(url, headers=HEADERS)
    soup = bs(webpage.content, "html.parser")

    current_dir = os.path.dirname(__file__)
    nome_scheda = "nexths_rtx" + str(scheda) + ".html" 
    file_path = current_dir + "\\"+ nome_scheda # creo il percorso file della pagina html

    #elimino il file già esistente
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Il file {file_path} è stato eliminato.")
        print("\n")
    else:
        print(f"Il file {file_path} non esiste.")
        print("\n")

    #qui vado a salvare la pagina html
    with open(current_dir + '/' + nome_scheda, 'w', encoding= "utf-8") as f:
        f.write(soup.prettify())
    #qui vado a fare tutte le operazioni sulla pagina 
    with open(nome_scheda, "r", encoding="utf-8") as htmlfile:
        soup = bs(htmlfile, "html.parser")
        #qui vado a prendere il link del prodotto per l'iterazione
        links = soup.find_all("a", attrs={'alt':'Scheda Prodotto'})        

        #Qui inizio a prendere i link della pagina della ricerca
        links_list = []
        elementi_aggiunti = 0

        for link in links:
            if elementi_aggiunti >= limite_elementi: #limito il numero di elementi per la ricerca
                break
            links_list.append(link.get('href'))
            elementi_aggiunti += 1

       
        for link in links_list: #qui vado cercare tutti i link correlati
           
            new_webpage = requests.get(link, headers=HEADERS)
            new_soup = bs(new_webpage.content, "html.parser")

            try:#controlo che ci sia il nome del prodotto
                title = new_soup.find("h1", attrs={"class": 'itempage_title'})
                #qui vado a convertire il titolo in stringa e tolgo gli spazi
                title_str = title.string.strip()
                info_schede["nome"].append(title_str)
                info_schede["link"].append(str(link))
            except AttributeError:
                title_str = ""

            try:#qui vado a prendere il prezzo del prodotto se viene trovato ------------------
                price = new_soup.find('span', class_='prezzo_normale')
                price_str = price.get_text().strip() #qui recupero il prezzo con il tag bdi
                info_schede["prezzo"].append(price_str)
            except AttributeError:
                price = ""

            try:#qui vado a prendere il prezzo nel caso sia scontato dato che cambia il tag
                if price == "":
                    price = new_soup.find('span', class_='prezzo_promo')
                    price_str = price.get_text().strip() 
                    info_schede["prezzo"].append(price_str)
            except AttributeError:
                price = ""

    return info_schede



def check_soglia(prodotti_amazon):
    prodotti_checked = {"nome": [], "prezzo": [], "link": []}

    prezzi_split = []
    # qui vado a fare la media dei prodotti amazon
    for nome, prezzo, link in zip(prodotti_amazon["nome"], prodotti_amazon["prezzo"], prodotti_amazon["link"]):
        prezzo_senza_euro = prezzo.split("€")[0]
        prezzo_con_punto = prezzo_senza_euro.replace(".", "").replace(",", ".")
        prezzo_split = float(prezzo_con_punto)

        prezzi_split.append(prezzo_split)
        prodotti_checked["nome"].append(nome)
        prodotti_checked["prezzo"].append(prezzo_split)
        prodotti_checked["link"].append(link)

    media = sum(prezzi_split) / len(prezzi_split)
    soglia = media * 0.6

    i = len(prodotti_checked["prezzo"]) - 1
    while i >= 0:
        if prodotti_checked["prezzo"][i] <= soglia:
            prodotti_checked["nome"].pop(i)
            prodotti_checked["prezzo"].pop(i)
            prodotti_checked["link"].pop(i)
        i -= 1

    return prodotti_checked



def cast_prezzi(prodotti):
    prodotti_cast = {"nome": [], "prezzo": [], "link": []}
    if not prodotti:
        return prodotti_cast
    else:
        # Imposta la localizzazione corrente
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

        for nome, prezzo, link in zip(prodotti["nome"], prodotti["prezzo"], prodotti["link"]):
            prezzo_senza_euro = prezzo.split("€")[1].strip()  # Rimuovi spazi iniziali e finali dopo "€"
            prezzo_con_punto = prezzo_senza_euro.replace(".", "").replace(",", ".")
            prezzo_split = None
            if prezzo_con_punto:
                try:
                    prezzo_split = locale.atof(prezzo_senza_euro)
                except ValueError:
                    # Gestisci l'eccezione o salta il valore
                    continue
            else:
                # Salta il valore vuoto
                continue

            prodotti_cast["nome"].append(nome)
            prodotti_cast["prezzo"].append(prezzo_split)
            prodotti_cast["link"].append(link)
    return prodotti_cast



def prezzo_basso(prodotti_amazon, prodotti_akinformatica, prodotti_nexths):

    prezzi_amazon = prodotti_amazon["prezzo"] if prodotti_amazon else []
    prezzo_minimo_amazon = min(prezzi_amazon) if prezzi_amazon else None
    indice_prezzo_minimo_amazon = prezzi_amazon.index(prezzo_minimo_amazon) if prezzo_minimo_amazon is not None else None
    prodotto_minimo_amazon = {
        "nome": prodotti_amazon["nome"][indice_prezzo_minimo_amazon],
        "prezzo": prezzo_minimo_amazon,
        "link": prodotti_amazon["link"][indice_prezzo_minimo_amazon]
    } if prodotti_amazon and indice_prezzo_minimo_amazon is not None else None

    prezzi_akinformatica = prodotti_akinformatica["prezzo"] if prodotti_akinformatica else []
    prezzo_minimo_akinformatica = min(prezzi_akinformatica) if prezzi_akinformatica else None
    indice_prezzo_minimo_akinformatica = prezzi_akinformatica.index(prezzo_minimo_akinformatica) if prezzo_minimo_akinformatica is not None else None
    prodotto_minimo_akinformatica = {
        "nome": prodotti_akinformatica["nome"][indice_prezzo_minimo_akinformatica],
        "prezzo": prezzo_minimo_akinformatica,
        "link": prodotti_akinformatica["link"][indice_prezzo_minimo_akinformatica]
    } if prodotti_akinformatica and indice_prezzo_minimo_akinformatica is not None else None

    prezzi_nexths = prodotti_nexths["prezzo"] if prodotti_nexths else []
    prezzo_minimo_nexths = min(prezzi_nexths) if prezzi_nexths else None
    indice_prezzo_minimo_nexths = prezzi_nexths.index(prezzo_minimo_nexths) if prezzo_minimo_nexths is not None else None
    prodotto_minimo_nexths = {
        "nome": prodotti_nexths["nome"][indice_prezzo_minimo_nexths],
        "prezzo": prezzo_minimo_nexths,
        "link": prodotti_nexths["link"][indice_prezzo_minimo_nexths]
    } if prodotti_nexths and indice_prezzo_minimo_nexths is not None else None

    prezzi_minimi = [prezzo_minimo_amazon, prezzo_minimo_akinformatica, prezzo_minimo_nexths]
    prezzi_minimi_validi = [prezzo for prezzo in prezzi_minimi if prezzo is not None]

    if prezzi_minimi_validi:
        prezzo_minimo_assoluto = min(prezzi_minimi_validi)
        indice_minimo = prezzi_minimi.index(prezzo_minimo_assoluto)

        if indice_minimo == 0:
            prodotto_minimo = prodotto_minimo_amazon
        elif indice_minimo == 1:
            prodotto_minimo = prodotto_minimo_akinformatica
        else:
            prodotto_minimo = prodotto_minimo_nexths

        return prodotto_minimo

    return None



def prezzo_alto(prodotti_amazon, prodotti_akinformatica, prodotti_nexths):
    prezzi_amazon = prodotti_amazon["prezzo"] if prodotti_amazon else []
    prezzo_massimo_amazon = max(prezzi_amazon) if prezzi_amazon else None
    indice_prezzo_massimo_amazon = prezzi_amazon.index(prezzo_massimo_amazon) if prezzo_massimo_amazon is not None else None
    prodotto_massimo_amazon = {
        "nome": prodotti_amazon["nome"][indice_prezzo_massimo_amazon],
        "prezzo": prezzo_massimo_amazon,
        "link": prodotti_amazon["link"][indice_prezzo_massimo_amazon]
    } if indice_prezzo_massimo_amazon is not None else None

    prezzi_akinformatica = prodotti_akinformatica["prezzo"] if prodotti_akinformatica else []
    prezzo_massimo_akinformatica = max(prezzi_akinformatica) if prezzi_akinformatica else None
    indice_prezzo_massimo_akinformatica = prezzi_akinformatica.index(prezzo_massimo_akinformatica) if prezzo_massimo_akinformatica is not None else None
    prodotto_massimo_akinformatica = {
        "nome": prodotti_akinformatica["nome"][indice_prezzo_massimo_akinformatica],
        "prezzo": prezzo_massimo_akinformatica,
        "link": prodotti_akinformatica["link"][indice_prezzo_massimo_akinformatica]
    } if indice_prezzo_massimo_akinformatica is not None else None

    prezzi_nexths = prodotti_nexths["prezzo"] if prodotti_nexths else []
    prezzo_massimo_nexths = max(prezzi_nexths) if prezzi_nexths else None
    indice_prezzo_massimo_nexths = prezzi_nexths.index(prezzo_massimo_nexths) if prezzo_massimo_nexths is not None else None
    prodotto_massimo_nexths = {
        "nome": prodotti_nexths["nome"][indice_prezzo_massimo_nexths],
        "prezzo": prezzo_massimo_nexths,
        "link": prodotti_nexths["link"][indice_prezzo_massimo_nexths]
    } if indice_prezzo_massimo_nexths is not None else None

    prezzi_massimi = [prezzo_massimo_amazon, prezzo_massimo_akinformatica, prezzo_massimo_nexths]
    prezzi_massimi_validi = [prezzo for prezzo in prezzi_massimi if prezzo is not None]

    if prezzi_massimi_validi:
        indice_massimo = prezzi_massimi.index(max(prezzi_massimi_validi))

        if indice_massimo == 0:
            prodotto_massimo = prodotto_massimo_amazon
        elif indice_massimo == 1:
            prodotto_massimo = prodotto_massimo_akinformatica
        else:
            prodotto_massimo = prodotto_massimo_nexths

        return prodotto_massimo

    return None



def calcola_media_prezzi(prodotti_amazon, prodotti_akinformatica, prodotti_nexths):
    prezzi_amazon = prodotti_amazon["prezzo"] if prodotti_amazon else []
    prezzi_akinformatica = prodotti_akinformatica["prezzo"] if prodotti_akinformatica else []
    prezzi_nexths = prodotti_nexths["prezzo"] if prodotti_nexths else []

    prezzi_tot = prezzi_amazon + prezzi_akinformatica + prezzi_nexths
    media_prezzi = sum(prezzi_tot) / len(prezzi_tot)
    media_prezzi = round(media_prezzi, 2)

    return media_prezzi






    
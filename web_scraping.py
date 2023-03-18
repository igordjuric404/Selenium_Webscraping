from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from os.path import isfile

class Proizvod:
    __naziv_modela : str
    __cena : float

    def __init__(self, naziv_modela="Nema podataka o nazivu", cena="Nema podataka o ceni") -> None:
        self.__naziv_modela = naziv_modela
        self.__cena = cena

    def __str__(self) -> str:
        rez = ""
        rez += f"Naziv modela: {self.__naziv_modela}\nCena: {self.__cena}\n"
        return rez

    def get_model(self):
        return self.__naziv_modela

    def get_cena(self):
        return self.__cena

    def set_model(self, model):
        if len(model) < 3:
            return "Naziv modela mora imati barem 3 karaktera"
        self.__naziv_modela = model

    def set_cena(self, cena):
        if cena <= 0:
            return 'Cena ne moze biti negativna'
        self.__cena = cena

    @abstractmethod
    def proizvod_csv(self):
        rez = ""
        naziv = self.__naziv_modela.replace(',', '')
        cena = self.__cena
        rez += f"{naziv},{cena}\n"
        return rez 

    @staticmethod
    def sortiranje_naziv(lista_proizvoda):
        lista_proizvoda = sorted(lista_proizvoda, key=lambda x:x.__naziv_modela)
        return lista_proizvoda
    
    @staticmethod 
    def sortiranje_cena_rastuce(lista_proizvoda):
        lista_proizvoda.sort(key=lambda x: x.__cena, reverse=False)
        return lista_proizvoda
    
    @staticmethod 
    def sortiranje_cena_opadajuce(lista_proizvoda):
        lista_proizvoda.sort(key=lambda x: x.__cena, reverse=True)
        return lista_proizvoda

class SmartTV(Proizvod):
    __procesor : str
    __rezolucija : str
    __broj_hdmi : int

    def __init__(self, naziv_modela, cena, procesor="Nema podataka o procesoru", 
        rezolucija="Nema podataka o rezoluciji", broj_hdmi="Nema podataka o broju HDMI"):
        super().__init__(naziv_modela, cena)
        self.__procesor = procesor
        self.__rezolucija = rezolucija
        self.__broj_hdmi = broj_hdmi
    
    def __str__(self) -> str:
        rez = super().__str__()
        rez += f"Procesor: {self.__procesor}\nRezolucija: {self.__rezolucija}\nBroj HDMI: {self.__broj_hdmi}"
        return rez

    def get_procesor(self):
        return self.__procesor

    def get_rezolucija(self):
        return self.__rezolucija

    def get_hdmi(self):
        return self.__broj_hdmi

    def set_procesor(self, procesor):
        if len(procesor) < 3:
            return 'Naziv procesora mora imati barem 3 karaktera'
        self.__procesor = procesor

    def set_rezolucija(self, rezolucija):
        if len(rezolucija) < 3:
            return 'Rezolucija mora imati barem 3 karaktera'
        self.__rezolucija = rezolucija

    def set_hdmi(self, hdmi):
        if hdmi < 0:
            return 'Broj HDMI portova ne moze biti negativan'
        self.__broj_hdmi = hdmi
    
    @classmethod
    def konstruktor_csv(self, csv_string):
        csv_string.replace('\n', '')
        deo = csv_string.split(',')
        t1 = SmartTV(deo[0], deo[1], deo[2], deo[3], deo[4])
        return t1
        
    def proizvod_csv(self):
        rez =  super().proizvod_csv()
        rez = rez.replace('\n', ',')
        rez += f"{self.__procesor.replace(',', '')},{self.__rezolucija.replace(',', '')},{self.__broj_hdmi.replace(',', '')}\n"
        return rez

    @staticmethod
    def ucitaj_sve_objekte_iz_fajla(naziv_fajla):
        if not isfile(naziv_fajla):
            return 'Fajl ne postoji'
        f = open(naziv_fajla, 'r')
        f.readline()
        objekti = []
        while True:
            red = f.readline()
            if red == '':
                break               
            delovi = red.split(',')      
            cena = delovi[1].replace('RSD', '')   
            cena = cena.replace('.', '')             
            delovi[4] = delovi[4].replace("\n", "")      
            televizor  = SmartTV(delovi[0], float(cena), delovi[2], delovi[3], delovi[4])
            objekti.append(televizor)
        return objekti
            
    @staticmethod
    def upisi_objekte_u_fajl(lista_objekata, fajl):
        if not isfile(fajl):
            return 'Los fajl'
        f = open(fajl, 'w')
        for objekat in lista_objekata:
            f.write(objekat.proizvod_csv())
        f.close

    @staticmethod 
    def opseg_cena(lista_objekata, cena_min, cena_max):
        proizvodi_u_opsegu = []
        for objekat in lista_objekata:
            if objekat.get_cena() > cena_min and objekat.get_cena() < cena_max:
                proizvodi_u_opsegu.append(objekat)

        return proizvodi_u_opsegu

class NonSmartTV(Proizvod):
    __dijagonala : str
    __snaga_zvucnika : str
    __usb : int 

    def __init__(self, naziv_modela, cena, dijagonala="Nema podataka o dijagonali ekrana",
         snaga_zvucnika="Nema podataka o snazi zvucnika", usb="Nema podataka o USB"):
        super().__init__(naziv_modela, cena)
        self.__dijagonala = dijagonala
        self.__snaga_zvucnika = snaga_zvucnika
        self.__usb = usb

    def __str__(self) -> str:
        rez = super().__str__()
        rez += f"Dijagonala ekrana: {self.__dijagonala}\nSnaga zvucnika: {self.__snaga_zvucnika}\nUSB: {self.__usb}"
        return rez

    def get_dijagonala(self):
        return self.__dijagonala

    def set_dijagonala(self, dijagonala):
        if len(dijagonala) < 3:
            return 'Duzina ekrana mora imati barem 3 karaktera'
        self.__dijagonala = dijagonala

    def get_snaga_zvucnika(self):
        return self.__snaga_zvucnika

    def set_snaga_zvucnika(self, snaga_zvucnika):
        if len(snaga_zvucnika) < 3:
            return 'Snaga zvucnika mora imati barem 3 karaktera'
        self.__snaga_zvucnika = snaga_zvucnika
    
    def get_usb(self):
        return self.__usb

    def set_usb(self, usb):
        if usb < 0:
            return 'Broj USB portova ne moze biti negativan'
        self.__usb = usb

    @classmethod
    def konstruktor_csv(self,csv_string):        
        red = csv_string.split(',')
        televizor = NonSmartTV(red[0], red[1], red[2], red[3], red[4])
        return televizor
    
    def proizvod_csv(self):
        rez = super().proizvod_csv()
        rez = rez.replace('\n', '')        
        rez += f",{self.__dijagonala.replace(',','')},{self.__snaga_zvucnika.replace(',','')},{self.__usb}\n"
        return rez

    @staticmethod
    def ucitaj_sve_objekte_iz_fajla(naziv_fajla):
        if not isfile(naziv_fajla):
            return 'Fajl ne postoji'
        f = open(naziv_fajla, 'r')
        f.readline()
        objekti = []
        while True:
            red = f.readline()
            if red == '':
                break                        
            delovi = red.split(',')
            delovi[1] = delovi[1].replace('RSD', '')
            delovi[1] = delovi[1].replace('.','')     
            delovi[4] = delovi[4].replace("\n", "")      
            televizor = NonSmartTV(delovi[0], float(delovi[1]), delovi[2], delovi[3],delovi[4])
            objekti.append(televizor)        
        return objekti    

    @staticmethod
    def upisi_objekte_u_fajl(lista_objekata, fajl):
        if not isfile(fajl):
            return 'Los fajl'
        f = open(fajl, 'w')
        for objekat in lista_objekata:
            f.write(objekat.proizvod_csv())
        f.close

    @staticmethod 
    def opseg_cena(lista_objekata, cena_min, cena_max):
        proizvodi_u_opsegu = []
        for objekat in lista_objekata:
            if objekat.get_cena() > cena_min and objekat.get_cena() < cena_max:
                proizvodi_u_opsegu.append(objekat)

        return proizvodi_u_opsegu

class Tehnomanija:
    __driver : webdriver.Chrome

    def __init__(self):
        self.__driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    def dohvati_stranicu(self, putanja_do_stranice):
        self.__driver.get(putanja_do_stranice)
        self.__driver.maximize_window()

    def zatvori_browser(self):
        self.__driver.quit()

    def zatvori_tab(self):
        self.__driver.close()

    def cekaj(self, vreme_u_sekundama):
        self.__driver.implicitly_wait(vreme_u_sekundama)

    def pretraga_elementa_po_parametru(self, id="", klasa="", tagname="", name="", css_selektor="", link_text="", partial_link_text=""):
        if id != "":
            try:
                return self.__driver.find_element(By.ID, id)                
            except:
                return None            

        elif klasa != "":
            try:
                return self.__driver.find_elements(By.CLASS_NAME, klasa)
            except:
                return []

        elif tagname != "":
            try:
                return self.__driver.find_elements(By.TAG_NAME, tagname)                
            except:
                return []

        elif name != "":
            try:
                return self.__driver.find_elements(By.NAME, name)
            except:
                return []

        elif css_selektor != "":
            try:
                return self.__driver.find_elements(By.CSS_SELECTOR, css_selektor)

            except:
                return []

        elif link_text != "":
            try:
                return self.__driver.find_elements(By.LINK_TEXT, link_text)            
            except:
                return []

        elif partial_link_text != "":
            try:
                return self.__driver.find_elements(By.PARTIAL_LINK_TEXT, partial_link_text)
            except:
                return []

        else:
            return "Nije moguce dohvatiti trazeni element"

    def vrati_sve_stranice_sa_artiklom(self, putanja_pocetne_stranice):            
        self.cekaj(10)
        string_broj_stranica = self.pretraga_elementa_po_parametru(klasa='search-result-page-total')[0].text
        lista_string_broj_stranica = string_broj_stranica.split(" ")
        broj_stranica = lista_string_broj_stranica[2]
        broj_stranica = int(broj_stranica)
        lista_url = [putanja_pocetne_stranice]
        for i in range (broj_stranica):
            putanja_do_sledece = putanja_pocetne_stranice + f"?currentPage={i+1}"
            lista_url.append(putanja_do_sledece)
        return lista_url

    def obidji_stranicu(self, fajl, id="", klasa="", tagname="", name="", css_selektor="", link_text="", partial_link_text=""):                           

        self.cekaj(10)

        if id != "": 
            rez = self.pretraga_elementa_po_parametru(id=id)
        elif klasa != "": 
            rez = self.pretraga_elementa_po_parametru(klasa=klasa)
        elif tagname != "": 
            rez = self.pretraga_elementa_po_parametru(tagname=tagname)
        elif name != "": 
            rez = self.pretraga_elementa_po_parametru(name=name)
        elif css_selektor != "": 
            rez = self.pretraga_elementa_po_parametru(css_selektor=css_selektor)
        elif link_text != "": 
            rez = self.pretraga_elementa_po_parametru(link_text=link_text)
        elif partial_link_text != "":   
            rez = self.pretraga_elementa_po_parametru(partial_link_text=partial_link_text)
        pass
            
        broj_artikala = (len(rez))
        svi_proizvodi = []             
        f = open(fajl, 'a')                                                     
        for i in range(broj_artikala):            
            try:                      
                self.cekaj(10)     
                element = rez[i]                                             
                element.click()                        
                self.cekaj(10)                
                televizor = self.dohvati_proizvod()            
                if televizor is None: 
                    pass          
                svi_proizvodi.append(televizor)                
                f.write(televizor.proizvod_csv())   
            except:
                pass
            self.__driver.back()
            sleep(1)
            if id != "": 
                rez = self.pretraga_elementa_po_parametru(id=id)
            elif klasa != "": 
                rez = self.pretraga_elementa_po_parametru(klasa=klasa)
            elif tagname != "": 
                rez = self.pretraga_elementa_po_parametru(tagname=tagname)
            elif name != "": 
                rez = self.pretraga_elementa_po_parametru(name=name)
            elif css_selektor != "": 
                rez = self.pretraga_elementa_po_parametru(css_selektor=css_selektor)
            elif link_text != "": 
                rez = self.pretraga_elementa_po_parametru(link_text=link_text)
            elif partial_link_text != "":   
                rez = self.pretraga_elementa_po_parametru(partial_link_text=partial_link_text)
            pass
           
        f.close()      
        return svi_proizvodi

    def dohvati_proizvod(self):            
        self.__driver.execute_script("window.scrollTo(0, 200)") 
        try:
            self.cekaj(5)
            tab = self.pretraga_elementa_po_parametru(klasa='tab-title')[1]
            tab.click()
        except:
            pass

        self.cekaj(15)             
        tip = self.pretraga_elementa_po_parametru(css_selektor="a.emphasized")[0].text
        naziv_modela = self.pretraga_elementa_po_parametru(tagname='h1')[0].text
        cena = self.pretraga_elementa_po_parametru(klasa='product-price-newprice')[0].text

        nazivi_spec = self.pretraga_elementa_po_parametru(klasa='feature-name')
        vrednosti_spec = self.pretraga_elementa_po_parametru(klasa='feature-value')
        specifikacije_recnik = {}
        

        for i in range (len(nazivi_spec)):
            naziv = nazivi_spec[i].text
            vrednost = vrednosti_spec[i].text
            specifikacije_recnik[naziv] = vrednost
                       
        if tip == "Non-smart TV":                                           
            try:
                dijagonala = specifikacije_recnik["Dijagonala ekrana"]                    
            except:
                dijagonala = "Nema podataka o dijagonali ekrana"
            try:
                zvucnik = specifikacije_recnik["Snaga zvučnika"]            
            except:
                zvucnik = "Nema podataka o snazi zvucnika"
            try:
                usb = specifikacije_recnik["Usb"]                                
            except:
                usb = "Nema podataka o broju USB portova"              

            print("_" * 205)                             
            print("\n Naziv_modela:", naziv_modela, "\n Cena:", cena, "\n Dijagonala:", dijagonala, "\n Zvucnik:", zvucnik, "\n Broj USB portova:", usb)
            televizor = NonSmartTV(naziv_modela, cena, dijagonala, zvucnik, usb)                                           
            return televizor                             

        if tip == "Smart TV":                
            try:                        
                procesor = specifikacije_recnik['Procesor']            
            except:
                procesor = "Nema podataka o procesoru"
            try:
                rezolucija = specifikacije_recnik['Rezolucija ekrana']            
            except:
                rezolucija = "Nema podataka o rezoluciji ekrana"
            try:
                hdmi = specifikacije_recnik['HDMI']            
            except:
                hdmi = "Nema podataka o broju HDMI portova"

            print("_" * 205)                             
            print("\n Naziv_modela:", naziv_modela, "\n Cena:", cena, "\n Procesor:", procesor, "\n Rezolucija:", rezolucija, "\n Broj HDMI portova:", hdmi)
            televizor = SmartTV(naziv_modela, cena, procesor, rezolucija, hdmi)
            return televizor
                   

    def obidji_sve_stranice(self, putanja, fajl, id="", klasa="", tagname="", name="", css_selektor="", link_text="", partial_link_text=""):
            
            self.dohvati_stranicu(putanja)

            self.__driver.maximize_window()

            if id != "": 
                rez = self.pretraga_elementa_po_parametru(id=id)
            elif klasa != "": 
                rez = self.pretraga_elementa_po_parametru(klasa=klasa)
            elif tagname != "": 
                rez = self.pretraga_elementa_po_parametru(tagname=tagname)
            elif name != "": 
                rez = self.pretraga_elementa_po_parametru(name=name)
            elif css_selektor != "": 
                rez = self.pretraga_elementa_po_parametru(css_selektor=css_selektor)
            elif link_text != "": 
                rez = self.pretraga_elementa_po_parametru(link_text=link_text)
            elif partial_link_text != "":   
                rez = self.pretraga_elementa_po_parametru(partial_link_text=partial_link_text)
            pass

            print("\n" * 15)
            print(rez[0].text)
            f = open(fajl, 'w')
            if rez[0].text == 'Smart TV':        
                f.write("Naziv,Cena,Procesor,Rezolucija,Broj HDMI\n")
            elif rez[0].text == 'Non-smart TV':
                f.write("Naziv,Cena,Dijagonala ekrana,Snaga zvucnika,USB\n")
            else:
                return "Greska pri odaberu tipa proizvoda"
            f.close()
            rez[0].click()  
            sleep(1)          
            url = self.__driver.current_url
            lista_stranica = self.vrati_sve_stranice_sa_artiklom(url)            
            broj_stranica = len(lista_stranica)

            bas_svi_proizvodi = []
            for i in range (broj_stranica):                
                self.cekaj(10)
                self.dohvati_stranicu(lista_stranica[i])
                bas_svi_proizvodi = bas_svi_proizvodi + (self.obidji_stranicu(fajl, klasa='product'))    

def main():

    tehnomanija = Tehnomanija()    

########################################################################   P O K R E T A N J E    W E B    S C R A P I N G - A   ########################################################################

    # metoda obidji_sve_stranice prima putanju stranice gde imamo dve opcije ( nth-child[1] -> NonSmartTV, nth-child[2] -> SmartTV ) 
    # prosledjenim css selektorom se odredjuje da li ce se kliknuti prvi ili drugi link, prosledjuje se i fajl u koji se upisuje

    tehnomanija.obidji_sve_stranice("https://www.tehnomanija.rs/televizori-audio-i-video/televizori", "non_smart_tv.csv", css_selektor='.product-subcategory > .product-category--box:nth-child(1)')
    # tehnomanija.obidji_sve_stranice("https://www.tehnomanija.rs/televizori-audio-i-video/televizori", "smart_tv.csv", css_selektor='.product-subcategory > .product-category--box:nth-child(2)')

########################################################################   P O K R E T A N J E    W E B    S C R A P I N G - A   ########################################################################





#######################################################################   S O R T I R A N J E   L I S T E   T E L E V I Z O R A   #######################################################################

    lista_objekata = []
    lista_objekata = SmartTV.ucitaj_sve_objekte_iz_fajla('smart_tv.csv')

#########################################################################################################################################################################################################

    # -------------------------------- LISTA TELEVIZORA U DATOM OPSEGU CENA --------------------------------

    # televizori_u_opsegu = SmartTV.opseg_cena(lista_objekata, 20000, 50000)
    # for tv in televizori_u_opsegu:
    #     print()
    #     print(tv)
    #     print("_" * 205)

#########################################################################################################################################################################################################

    # ------------------------------------ SORTIRANJE PO NAZIVU 0-9-A-Z ------------------------------------

    # lista_sortirana_naziv = SmartTV.sortiranje_naziv(lista_objekata)
    # for tv in lista_sortirana_naziv:
    #     print()
    #     print(tv.get_model())
    #     print("_" * 205)
    # SmartTV.upisi_objekte_u_fajl(lista_sortirana_naziv, "lista_sortirana_naziv.csv")

#########################################################################################################################################################################################################

    # ------------------------------ SORTIRANJE PO CENI OD NAJNIZE DO NAJVISE ------------------------------

    # lista_sortirana_cena_rastuce = SmartTV.sortiranje_cena_rastuce(lista_objekata)
    # for tv in lista_sortirana_cena_rastuce:
    #     print()
    #     print(tv)
    #     print("_" * 205)
    # SmartTV.upisi_objekte_u_fajl(lista_sortirana_cena_rastuce, "lista_sortirana_cena_rastuce.csv")

#########################################################################################################################################################################################################

    # ------------------------------ SORTIRANJE PO CENI OD NAJVISE DO NAJNIZE ------------------------------

    # lista_sortirana_cena_opadajuce = SmartTV.sortiranje_cena_opadajuce(lista_objekata)
    # for tv in lista_sortirana_cena_opadajuce:
    #     print()
    #     print(tv)
    #     print("_" * 205)
    # SmartTV.upisi_objekte_u_fajl(lista_sortirana_cena_opadajuce, "lista_sortirana_cena_opadajuce.csv")

#######################################################################   S O R T I R A N J E   L I S T E   T E L E V I Z O R A   #######################################################################

if __name__ == "__main__":
    main()
import os
import threading
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import sys
import argparse
import pyperclip
from termcolor import colored
import socket
import signal
import whois
parser = argparse.ArgumentParser(description='web bilgileri',usage="tool kullanım rehberi")
parser.add_argument("site")
args = parser.parse_args()
site = args.site

mesaj ='''
[+]---TURK-----HACK-----TEAM----[+]
[+]-----------yuathay-----------[+]
[+]-----------------------------[+]
github.com/write-exploit
'''
class Interface():
    def __init__ (self):
        self.red = '\033[91m'
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.white = '\033[37m'
        self.bold = '\033[1m'
        self.end = '\033[0m'

    def info(self, message):
        print(f"[{self.white}*{self.end}] {message}")

    def error(self, message):
        print(f"[{self.red}x{self.end}] {self.red}{message}{self.end}")
    def success(self, message):
        print(f"[{self.green}✓{self.end}] {self.green}{message}{self.end}")
    def danger(self,message):
        print(f"[{self.red}!!!{self.end}] {message}")
    def mavi(self,message):
        print(f"{self.blue}{message}{self.end}")
global output
output = Interface()
#==============================
def signal_handler(sig,frame):
    sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)
#==============================
if not args.site:
    output.error("lütfen site adını belirtin")
    sys.exit(1) # çıkış yapıyoruz

if not str(site).startswith("https") and not str(site).startswith("http"): # verilen site https yada http ile başlamıyorsa
    print("\nsite https ilemi yoksa http ilemi başlıyor ?")
    print("https [1]")
    print("http  [2]\n")
    while True:
        try:
            başlangıc = int(input())
            if başlangıc == 1:
                site = f"https://{site}"
                break
            if başlangıc == 2:
                site = f"http://{site}"
                break
        except:
            pass
try:   
    requests.get(site,timeout=3)
except:
    output.error(f"bağlantı başarısız site bizi engelliyor olabilir yada bir hata oluştu [tekrar deneyin]")
    sys.exit(1)

def Terminali_Temizle(): 
    if os.name == 'nt':
        os.system("cls")
    else: 
        os.system("clear")

Terminali_Temizle()
output.mavi(mesaj)
# ========================

def çık_geri_kopyala(kopyalanacak_deger):
    ana_mesaj = '''\033[94m
(0) çıkış
(1) geri git
(2) kopyala\033[0m
          '''
    print(ana_mesaj)
    while True:
        try:
            o____o = int(input())
        except:
            output.error("integer ifadeler girin")
            continue
        if o____o != 0 and o____o != 1 and o____o != 2:
            output.error("lütfen geçerli bir değer girin\n")
            continue
        if o____o == 0: # çıkış
            output.success("çıkış başarılı...")
            sys.exit(1)
        if o____o == 1: # geri
            başlangıç_seçenekleri()
            genel_işlem()
        if o____o == 2: # kopyalama
            pyperclip.copy(kopyalanacak_deger)
            output.success("kopyalandı")
#==============================
# burada site ve site/ değerlerini karşılaştıracaz
# bazen gelen linkler veya bağlantılar site site/ olarak gelebiliyor
# ve bizde tekrar eden linkleri bulmak istedigimizde site == site/ gibi bir kod yazıyoruz
# bu kod bize False cıktısını verdiğinden dolayı tekrar eden değerleri bulamıyoruz
# bu fonksiyonda tam bunu çözecek verilen 2 linkten hangisi uzunsa onun en sağındaki değeri yani / işaretini kaldıracak ve böyle karşılaştırma yapıcak
# eğer linkler aynı ise True döndürecek
def url_kontrol(url1,url2):
    if url1 == url2:
        return True
    else:
        if len(url1) > len(url2):
            kopya_url1 = url1[:-1]
            if kopya_url1 == url2:
                return True
        else:
            kopya_url2 = url2[:-1]
            if kopya_url2 == url1:
                return True
#================================
class URLParser:
    def __init__(self):
        self.protokol = None
        self.domain = None
        self.subpage = None

    def urlparse(self,url):
        tam_url = url
        if url.startswith("https://"):
            url = url.replace("https://","")
            self.protokol = "https://"
        if url.startswith("http://"):
            url = url.replace("http://","")
            self.protokol = "http://"

        self.domain = str(url).split("/")[0]
        uzunluk = len(self.protokol+self.domain)
        self.subpage = tam_url[uzunluk:]
global url_parçala
url_parçala = URLParser()
url_parçala.urlparse(site)
# kullanım :
#https://www.youtube.com/feed/subscriptions
#print(url_parçala.protokol) https://
#print(url_parçala.domain)   www.youtube.com
#print(url_parçala.subpage)  /feed/subscriptions
#=================================
ua = UserAgent() 
def session_başlat():
    ua.firefox
    user_agent = ua.random # rastgele bir user agent alıyoruz
    headers = {'User-Agent':user_agent}
    global session
    session = requests.Session()
    session.headers.update(headers)
#=================================
def robots_txt():
    global Robots_TXT
    session_başlat()
    ana_sayfa = session.get(site)
    txt = session.get(site+"/robots.txt")
    if ana_sayfa.status_code == 200:
        if ana_sayfa.text != txt.text and url_kontrol(txt.url,f"{site}/robots.txt") and '404' not in txt.text:
            Robots_TXT = f"{txt.url} dosyasının içeriği :\n {txt.text}"
        else:
            Robots_TXT = "robots.txt bulunamadı"
    else:
        Robots_TXT = "robots.txt bulunamadı"
robots_txt()
#=================================
linkler = []
def istek(link):
    a = session.get(link).content
    çıktı = BeautifulSoup(a,'html.parser').find_all('a')
    for i in çıktı:
        if str(i["href"]).startswith("https") or str(i["href"]).startswith("http"):
            linkler.append(i['href'])
        else:
            if i["href"] == "#":
                pass
            else:
                if not str(i["href"]).startswith("/"):
                    pass
                else:
                    linkler.append(link+i["href"])
session_başlat()
istek(site)

tekrarsız = list(set(linkler))
#=================
# sitenin bizi yönlendirdiği url'ler arasında zararlı url'ler olabilir bu url'leri kullanıcıya gösterelim
yönlendirilen_urller = str()
for i in tekrarsız:
    response = requests.get(i)
    if response.history:
        if url_kontrol(response.url,i) is not True:
            yönlendirilen_urller += f"{i} ---> {response.url}\n"
            index = tekrarsız.index(i) # i değeri hangi index'de ise onu index adlı değişkene atar
            tekrarsız[index] = response.url

#=================
for i in tekrarsız:
    for w in tekrarsız:
        if i == w: # tekrarsız adlı değişkende tekrar eden elemanları kaldırdık fakat burada 2 döngü kullanıdıgımız icin 
            # degerler kendi ile karşılaşıyor ve karşılaşınca url_kontrol fonksiyonu tekrar eden eleman var diyip remove işlemini uyguluyor 
            # bu durumdan kaçmak için eşit değerler ile karşılaştığımızda continue işlemi uyguluyoruz
            continue
        if url_kontrol(i,w): # burada https://youtube.com https://youtube.com/ değerlerini kontrol ediyoruz eğer böyle değerler varsa birini kaldırıyoruz
            tekrarsız.remove(w)

baglanti_sözlük = {}
def tekrarsız_seçenekler():
    for i in range(len(tekrarsız)):
        baglanti_sözlük[i] = tekrarsız[i]
        print(f"({i}) {tekrarsız[i]}")
def ek_seçenekler():
    global tekrarsız_seçenekler_uzunluk
    tekrarsız_seçenekler_uzunluk = baglanti_sözlük.keys().__len__()
    output.mavi(f"({tekrarsız_seçenekler_uzunluk}) terminali temizle") # 13
    output.mavi(f"({tekrarsız_seçenekler_uzunluk+1}) geri git") # 14
    output.mavi(f"({tekrarsız_seçenekler_uzunluk+2}) çıkış yap") # 15

çekilen_bağlantılar = {} # kullanıcının istediği çekilen bağlantıları kayıt edicez ve sonradan birdaha aynı bağlantıyı çekmek istediginde zaman kaybetmeden sözlük içinden kullanıcıya içeriği vericez
kopyala = ""
def sorgu():
    global kopyala
    while True:
        try:
            cekilecek_baglantı = int(input())
        except:
            output.error("lütfen geçerli bir bağlantı numarası seçin")
            continue
        if kopyala:
            kopyala_secenegi = tekrarsız_seçenekler_uzunluk+3
            if cekilecek_baglantı == int(kopyala_secenegi):
                pyperclip.copy(kopyala)
                output.success("kopyalandı")
                continue
        if cekilecek_baglantı == tekrarsız_seçenekler_uzunluk: 
            Terminali_Temizle()
            fonksiyon_icinde_calistir()
            continue
        elif cekilecek_baglantı == tekrarsız_seçenekler_uzunluk+1: # bura geri git seçeneği bura seçildiğinde en aşağıdaki ana sorgu çalışacak
            başlangıç_seçenekleri()
            genel_işlem()
            
        elif cekilecek_baglantı == tekrarsız_seçenekler_uzunluk+2: # çıkış
            output.success("cıkış başarılı...")
            sys.exit(1)
        #=============
        else:
            if cekilecek_baglantı in baglanti_sözlük.keys():
                if cekilecek_baglantı in çekilen_bağlantılar.keys():
                    print(çekilen_bağlantılar[cekilecek_baglantı])
                    kopyala = çekilen_bağlantılar[cekilecek_baglantı]
                else:
                    baglanti_içerigi = session.get(baglanti_sözlük[int(cekilecek_baglantı)]).text
                    baglanti_içerigi = BeautifulSoup(baglanti_içerigi,'html.parser').prettify()
                    print(baglanti_içerigi)
                    çekilen_bağlantılar[cekilecek_baglantı] = baglanti_içerigi
                    kopyala = çekilen_bağlantılar[cekilecek_baglantı]
                tekrarsız_seçenekler()
                ek_seçenekler()
                output.mavi(f"({tekrarsız_seçenekler_uzunluk+3}) sayfa kaynağını kopyala")
                sorgu()
            else:
                output.error("lütfen geçerli bir bağlantı numarası seçin")
def fonksiyon_icinde_calistir():
    tekrarsız_seçenekler()
    ek_seçenekler()
    sorgu()
def bağlantı_fonksiyonunu_kullanici_icin_başlat():
    tekrarsız_seçenekler()
    ek_seçenekler()
    print("\niçeriğini çekmek istediginiz bağlantının numarasını yazın")
    sorgu()
#=================================
def port_scanner(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((ip,port))
        açık_portlar.append(f"açık port : {port}")
    except:
        pass
    
    finally:
        s.close()
def main():
    global açık_portlar
    açık_portlar = []
    while True:
        try:
            target_ip = url_parçala.domain
            target_ip = socket.gethostbyname(target_ip)  # Site adını IP adresine çevirme
            break
        except:
            pass
    for target_port in range(1111):#65535
        başla = threading.Thread(target=port_scanner,args=(target_ip,target_port))
        başla.start()
main()
portlar = []
for i in açık_portlar:
    i = i.split()
    for port in i:
        if str(port).isdecimal():
            portlar.append(port)
#=================================
def is_it_dangerous():
    global tehlikelimi
    tehlikelimi = str()
    with open(r"zaralı-site.txt","r") as dosya:
        içerik = dosya.read().splitlines()
        # https://www.usom.gov.tr/url-list.txt
        # usom'un zararlı olarak adlandırdığı siteler        
        for r in tekrarsız: # site içerisindeki bağlantıları bulmuştuk bu bağlantıların zararlı olup olmadığını kontrol edicez
            for zararlı in içerik:
                if zararlı == r:
                    if r == site:
                        tehlikelimi += f"\n\033[91m!!! {r} zararlı site'\033[0m'"
                    else:
                        tehlikelimi += f"\n\033[91m!!! {r} site içerisinde zararlı bağlantı bulundu'\033[0m'"
                    break
    if not tehlikelimi:
        tehlikelimi += "site güvenli"
is_it_dangerous()
# ========================================
whois_bilgisi = whois.whois(url_parçala.domain)
# ========================================
gizli_dizinler_liste = []
def gizli_dizinler_arama(girilen_deger):
    hedef_site = girilen_deger
    ana_sayfa = session.get(hedef_site)    
    with open(r"dirlist.txt","r") as dirlist:
        dirlist = dirlist.read().splitlines()
    session_başlat()
    def tara(url):
        response = session.get(url)
        if response.ok and response.text != ana_sayfa.text:
            gizli_dizinler_liste.append(response.url)
    thread = []

    for i in dirlist:
        url = hedef_site+i
        thread.append(threading.Thread(target=tara,args=(url,)))
    for t in thread:
        t.start()

gizli_dizinler_arama(url_parçala.protokol+url_parçala.domain+"/") # normal bir site verildiginde burası güzel bir şekilde çalışıyor 
# ama http://192.168.1.45/bWAPP gibi bir site verilince protokol ve domain şu şekilde oluyor
# http://192.168.1.45 ve işlem başarısız oluyor bu yüzden aşağı tarafa tam linki ekleyip birdaha deneme yaptık
if site.endswith("/"):
    gizli_dizinler_arama(site)
else:
    gizli_dizinler_arama(site+"/")

işlem = {
    "0": "", # sys.exit(1) kodunu çalıştıracaz burada yazarsak kod sonlanır ve aşağıdaki kodlar çalışmaz
    "1": "", # ekran temizle
    "2": Robots_TXT,
    "3": "", # for döngüsü ile acık portları listeliycez
    "4": "", # sitenin alt bağlantıları
    "5": tehlikelimi,
    "6": whois_bilgisi,
    "7": "", # gizli dizinler
    "8": yönlendirilen_urller # yönlendirilen url'ler
    }

def başlangıç_seçenekleri():
    print('''
(0) çıkış yap
(1) terminali temizle
(2) robots.txt
(3) açık portlar
(4) alt bağlantılar
(5) site tehlikelimi
(6) whois bilgileri
(7) gizli dizinler
(8) yönlendirilen url'ler
          ''')

başlangıç_seçenekleri()
def genel_işlem():
    while True:
        seçenek = int(input())
        if str(seçenek) not in işlem.keys():
            output.error("lütfen geçerli bir değer girin")
            continue
        else:
            if not işlem[str(seçenek)]:
                if seçenek == 0: # çıkış
                    sys.exit(1) 
                elif seçenek == 1: # terminal temizliği
                    Terminali_Temizle()
                    başlangıç_seçenekleri()
                    genel_işlem()
                elif seçenek == 3: # portları listeliycez
                    [print(i) for i in açık_portlar]
                        
                    çık_geri_kopyala(str(portlar))

                elif seçenek == 4: # alt bağlantıları bulma
                    bağlantı_fonksiyonunu_kullanici_icin_başlat()
                elif seçenek == 7: # gizli dizinler
                    [print(i) for i in gizli_dizinler_liste]
                    çık_geri_kopyala(str(gizli_dizinler_liste))
              
            else:
                istenilen_deger = işlem[str(seçenek)]
                print(istenilen_deger)
                çık_geri_kopyala(str(istenilen_deger))
        başlangıç_seçenekleri()
genel_işlem()

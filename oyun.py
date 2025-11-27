import math
import pygame
import random

# Pygame baslat
pygame.init()

# Renkler (Etkilesimli tahta icin parlak renkler)
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
MAVI = (52, 152, 219)
YESIL = (46, 204, 113)
KIRMIZI = (231, 76, 60)
TURUNCU = (243, 156, 18)
MOR = (155, 89, 182)
ACIK_GRI = (236, 240, 241)
ALTIN = (241, 196, 15)

# Pencere ayarlari
GENISLIK = 1200
YUKSEKLIK = 800
pencere = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Karekok Sadelestirme Oyunu - 8. Sinif")

# Saat
saat = pygame.time.Clock()

# Zorluk seviyeleri ve puanlari
ZORLUKLAR = {
    "KOLAY": {
        "puan": 5,
        "sayilar": [8, 12, 18, 20, 24, 27, 32, 45, 48, 50],
        "renk": YESIL,
        "aciklama": "Kucuk sayilar - 5 puan"
    },
    "ORTA": {
        "puan": 7,
        "sayilar": [54, 63, 72, 75, 80, 98, 108, 112, 125, 128, 147, 150],
        "renk": TURUNCU,
        "aciklama": "Orta sayilar - 7 puan"
    },
    "ZOR": {
        "puan": 10,
        "sayilar": [162, 180, 192, 200, 242, 245, 288, 300, 338, 392, 432, 450, 500],
        "renk": KIRMIZI,
        "aciklama": "Buyuk sayilar - 10 puan"
    }
}

# Karekok sadelestirme fonksiyonu
def karekok_sadelestir(sayi):
    """√sayi = a√b formatinda tum olasi sadelestirmeleri bulur"""
    sonuclar = []
    for a in range(1, int(math.sqrt(sayi)) + 1):
        b = sayi // (a * a)
        if a * a * b == sayi:
            sonuclar.append((a, b))
    return sonuclar

# Rastgele soru olustur
def soru_olustur(zorluk):
    """Secilen zorlukta rastgele bir karekok sorusu olusturur"""
    sayilar = ZORLUKLAR[zorluk]["sayilar"]
    sayi = random.choice(sayilar)
    dogru_cevaplar = karekok_sadelestir(sayi)
    en_sade = dogru_cevaplar[-1]
    return sayi, dogru_cevaplar, en_sade

# Yanlis cevaplar olustur
def yanlis_cevaplar_olustur(sayi, dogru_cevap):
    """Dogru cevaba benzer ama yanlis cevaplar olusturur"""
    a, b = dogru_cevap
    yanlislar = []
    
    secenekler = [
        (a + 1, b),
        (a - 1, b) if a > 1 else (a + 2, b),
        (a, b + 1),
        (a, b - 1) if b > 1 else (a, b + 2),
        (a + 1, b - 1) if b > 1 else (a + 1, b + 1),
    ]
    
    for cevap in secenekler:
        if cevap not in yanlislar and cevap != dogru_cevap and cevap[0] > 0 and cevap[1] > 0:
            yanlislar.append(cevap)
            if len(yanlislar) == 3:
                break
    
    return yanlislar

# Buton ciz
def buton_ciz(metin, x, y, genislik, yukseklik, renk, uzerine_gelince_renk):
    """Buton cizer ve tiklanma kontrolu yapar"""
    fare = pygame.mouse.get_pos()
    tik = pygame.mouse.get_pressed()
    
    if x < fare[0] < x + genislik and y < fare[1] < y + yukseklik:
        pygame.draw.rect(pencere, uzerine_gelince_renk, (x, y, genislik, yukseklik))
        if tik[0] == 1:
            return True
    else:
        pygame.draw.rect(pencere, renk, (x, y, genislik, yukseklik))
    
    font = pygame.font.Font(None, 50)
    metin_yuzey = font.render(metin, True, BEYAZ)
    metin_rect = metin_yuzey.get_rect(center=(x + genislik/2, y + yukseklik/2))
    pencere.blit(metin_yuzey, metin_rect)
    
    return False

# Oyun durumlari
DURUM_ANA_EKRAN = "ana_ekran"
DURUM_ZORLUK_SECIMI = "zorluk_secimi"
DURUM_OYUN = "oyun"
DURUM_SONUC = "sonuc"

# Oyun degiskenleri
durum = DURUM_ANA_EKRAN
secilen_zorluk = None
puan = 0
toplam_soru = 0
mevcut_soru = None
mevcut_secenekler = None
geri_bildirim = None
geri_bildirim_zamanlayici = 0

# Ana oyun dongusu
calisiyor = True
while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False
    
    pencere.fill(BEYAZ)
    
    # ANA EKRAN
    if durum == DURUM_ANA_EKRAN:
        font_buyuk = pygame.font.Font(None, 100)
        baslik = font_buyuk.render("Karekok Oyunu", True, MAVI)
        pencere.blit(baslik, (300, 150))
        
        font_orta = pygame.font.Font(None, 50)
        alt_baslik = font_orta.render("8. Sinif - Karekoklu Ifadeleri Sadelestirme", True, SIYAH)
        pencere.blit(alt_baslik, (180, 250))
        
        font_kucuk = pygame.font.Font(None, 40)
        aciklama1 = font_kucuk.render("√48 gibi karekoklu ifadeleri", True, SIYAH)
        aciklama2 = font_kucuk.render("4√3 seklinde sadelestir!", True, SIYAH)
        pencere.blit(aciklama1, (350, 350))
        pencere.blit(aciklama2, (380, 400))
        
        if buton_ciz("BASLA", 450, 500, 300, 100, YESIL, (39, 174, 96)):
            durum = DURUM_ZORLUK_SECIMI
            pygame.time.wait(200)
    
    # ZORLUK SECIMI EKRANI
    elif durum == DURUM_ZORLUK_SECIMI:
        font_buyuk = pygame.font.Font(None, 80)
        baslik = font_buyuk.render("Zorluk Seviyesi Sec", True, MAVI)
        pencere.blit(baslik, (280, 100))
        
        # Zorluk butonlari
        y_baslangic = 250
        buton_yukseklik = 120
        bosluk = 40
        
        for i, (zorluk_adi, zorluk_bilgi) in enumerate(ZORLUKLAR.items()):
            y = y_baslangic + i * (buton_yukseklik + bosluk)
            renk = zorluk_bilgi["renk"]
            
            # Zorluk butonu
            if buton_ciz(zorluk_adi, 300, y, 600, buton_yukseklik, renk, ALTIN):
                secilen_zorluk = zorluk_adi
                durum = DURUM_OYUN
                puan = 0
                toplam_soru = 0
                mevcut_soru = soru_olustur(secilen_zorluk)
                sayi, dogru_cevaplar, en_sade = mevcut_soru
                yanlislar = yanlis_cevaplar_olustur(sayi, en_sade)
                tum_secenekler = [en_sade] + yanlislar
                random.shuffle(tum_secenekler)
                mevcut_secenekler = tum_secenekler
                geri_bildirim = None
                pygame.time.wait(200)
            
            # Aciklama metni
            font_kucuk = pygame.font.Font(None, 35)
            aciklama = font_kucuk.render(zorluk_bilgi["aciklama"], True, SIYAH)
            aciklama_rect = aciklama.get_rect(center=(600, y + buton_yukseklik/2))
            pencere.blit(aciklama, aciklama_rect)
        
        # Geri butonu
        if buton_ciz("<- GERI", 50, 700, 200, 60, ACIK_GRI, MAVI):
            durum = DURUM_ANA_EKRAN
            pygame.time.wait(200)
    
    # OYUN EKRANI
    elif durum == DURUM_OYUN:
        sayi, dogru_cevaplar, en_sade = mevcut_soru
        zorluk_bilgi = ZORLUKLAR[secilen_zorluk]
        
        # Ust bilgi cubugu
        pygame.draw.rect(pencere, zorluk_bilgi["renk"], (0, 0, GENISLIK, 80))
        
        # Zorluk gostergesi
        font_kucuk = pygame.font.Font(None, 40)
        zorluk_text = font_kucuk.render("Zorluk: " + secilen_zorluk, True, BEYAZ)
        pencere.blit(zorluk_text, (50, 25))
        
        # Puan goster
        puan_text = font_kucuk.render("Puan: " + str(puan) + " | Soru: " + str(toplam_soru) + "/10", True, BEYAZ)
        pencere.blit(puan_text, (850, 25))
        
        # Soru
        font_buyuk = pygame.font.Font(None, 120)
        soru_text = font_buyuk.render("√" + str(sayi) + " = ?", True, SIYAH)
        pencere.blit(soru_text, (450, 120))
        
        # Aciklama
        font_orta = pygame.font.Font(None, 45)
        aciklama = font_orta.render("En sadelestirmis halini sec:", True, SIYAH)
        pencere.blit(aciklama, (350, 270))
        
        # Puan degeri goster
        puan_degeri_text = font_orta.render("(Her dogru: +" + str(zorluk_bilgi['puan']) + " puan)", True, zorluk_bilgi["renk"])
        pencere.blit(puan_degeri_text, (380, 320))
        
        # Secenekler
        secenek_y_baslangic = 380
        secenek_genislik = 250
        secenek_yukseklik = 120
        secenek_bosluk = 50
        
        for i, (a, b) in enumerate(mevcut_secenekler):
            sutun = i % 2
            satir = i // 2
            x = 250 + sutun * (secenek_genislik + secenek_bosluk)
            y = secenek_y_baslangic + satir * (secenek_yukseklik + secenek_bosluk)
            
            if a == 1:
                secenek_text = "√" + str(b)
            else:
                secenek_text = str(a) + "√" + str(b)
            
            renk = MAVI
            if geri_bildirim:
                if (a, b) == en_sade:
                    renk = YESIL
            
            if buton_ciz(secenek_text, x, y, secenek_genislik, secenek_yukseklik, renk, TURUNCU):
                if not geri_bildirim:
                    toplam_soru += 1
                    if (a, b) == en_sade:
                        puan += zorluk_bilgi["puan"]
                        geri_bildirim = "dogru"
                    else:
                        geri_bildirim = "yanlis"
                    geri_bildirim_zamanlayici = pygame.time.get_ticks()
                    pygame.time.wait(200)
        
        # Geri bildirim
        if geri_bildirim:
            font_geri_bildirim = pygame.font.Font(None, 60)
            if geri_bildirim == "dogru":
                mesaj = font_geri_bildirim.render("DOGRU! +" + str(zorluk_bilgi['puan']) + " puan", True, YESIL)
                pencere.blit(mesaj, (380, 670))
            else:
                mesaj = font_geri_bildirim.render("Yanlis!", True, KIRMIZI)
                if en_sade[0] > 1:
                    dogru_mesaj = font_geri_bildirim.render("Dogru: " + str(en_sade[0]) + "√" + str(en_sade[1]), True, YESIL)
                else:
                    dogru_mesaj = font_geri_bildirim.render("Dogru: √" + str(en_sade[1]), True, YESIL)
                pencere.blit(mesaj, (480, 650))
                pencere.blit(dogru_mesaj, (380, 710))
            
            if pygame.time.get_ticks() - geri_bildirim_zamanlayici > 2000:
                if toplam_soru >= 10:
                    durum = DURUM_SONUC
                else:
                    mevcut_soru = soru_olustur(secilen_zorluk)
                    sayi, dogru_cevaplar, en_sade = mevcut_soru
                    yanlislar = yanlis_cevaplar_olustur(sayi, en_sade)
                    tum_secenekler = [en_sade] + yanlislar
                    random.shuffle(tum_secenekler)
                    mevcut_secenekler = tum_secenekler
                    geri_bildirim = None
    
    # SONUC EKRANI
    elif durum == DURUM_SONUC:
        zorluk_bilgi = ZORLUKLAR[secilen_zorluk]
        
        # Baslik
        font_buyuk = pygame.font.Font(None, 100)
        baslik = font_buyuk.render("Oyun Bitti!", True, MAVI)
        pencere.blit(baslik, (350, 100))
        
        # Zorluk seviyesi
        font_orta = pygame.font.Font(None, 60)
        zorluk_text = font_orta.render("Zorluk: " + secilen_zorluk, True, zorluk_bilgi["renk"])
        pencere.blit(zorluk_text, (430, 220))
        
        # Toplam puan
        font_buyuk2 = pygame.font.Font(None, 90)
        puan_text = font_buyuk2.render("Toplam Puan: " + str(puan), True, YESIL)
        pencere.blit(puan_text, (320, 310))
        
        # Dogru sayisi
        dogru_sayisi = puan // zorluk_bilgi["puan"]
        detay_text = font_orta.render(str(dogru_sayisi) + " dogru / 10 soru", True, SIYAH)
        pencere.blit(detay_text, (400, 420))
        
        # Basari yuzdesi
        yuzde = (dogru_sayisi / 10) * 100
        yuzde_text = font_orta.render("Basari: %" + str(int(yuzde)), True, TURUNCU)
        pencere.blit(yuzde_text, (470, 490))
        
        # Butonlar
        if buton_ciz("TEKRAR OYNA", 300, 600, 300, 80, YESIL, (39, 174, 96)):
            durum = DURUM_ZORLUK_SECIMI
            pygame.time.wait(200)
        
        if buton_ciz("ANA MENU", 650, 600, 300, 80, MAVI, MOR):
            durum = DURUM_ANA_EKRAN
            pygame.time.wait(200)
    
    pygame.display.flip()
    saat.tick(60)

pygame.quit()
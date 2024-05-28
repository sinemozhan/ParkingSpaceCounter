import cv2  # OpenCV kütüphanesini içe aktarır
import pickle  # Pickle kütüphanesini içe aktarır

width = 50  # Park alanı dikdörtgeninin genişliği
height = 100  # Park alanı dikdörtgeninin yüksekliği

# Park alanı pozisyonlarını dosyadan yüklemeyi dene
try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []  # Dosya yoksa veya hata olursa boş bir liste oluştur


# Resmi dikdörtgenlerle kaydeden fonksiyon
def save_image_with_rectangles(img, posList):
    img_with_rects = img.copy()  # Orijinal resmin bir kopyasını al
    for pos in posList:  # Pozisyon listesindeki her pozisyon için
        cv2.rectangle(img_with_rects, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)  # Dikdörtgen çiz
    cv2.imwrite("resim/rektorluk_with_rects2.jpeg", img_with_rects)  # Resmi kaydet


# Fare tıklama olaylarını işleyen fonksiyon
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # Sol fare tuşuna basılırsa
        posList.append((x, y))  # Yeni pozisyonu listeye ekle

    if events == cv2.EVENT_RBUTTONDOWN:  # Sağ fare tuşuna basılırsa
        for i, pos in enumerate(posList):  # Pozisyon listesini dolaş
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:  # Tıklanan yer dikdörtgen içindeyse
                posList.pop(i)  # Pozisyonu listeden çıkar
                break

    # Pozisyon listesini dosyaya kaydet
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

    # Dikdörtgenlerle resmi kaydet
    save_image_with_rectangles(original_img, posList)


# Orijinal resmi oku
original_img = cv2.imread("resim/rektorluk2.jpeg")

# Resmi yüklemeyi dene, hata olursa orijinal resmi kullan
try:
    img = cv2.imread("resim/rektorluk_with.jpeg")
    if img is None:
        img = original_img.copy()
except:
    img = original_img.copy()

# "img" adında bir pencere oluştur ve yeniden boyutlandır
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", 800, 500)

# Sonsuz döngüde resmi göster ve fare olaylarını kontrol et
while True:
    img_display = img.copy()  # Gösterilecek resmin bir kopyasını al
    for pos in posList:  # Pozisyon listesindeki her pozisyon için
        cv2.rectangle(img_display, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)  # Dikdörtgen çiz

    cv2.imshow("img", img_display)  # Resmi göster
    cv2.setMouseCallback("img", mouseClick)  # Fare olaylarını takip et
    key = cv2.waitKey(1) & 0xFF  # Klavyeden tuşa basılmasını bekle
    if key == ord('q'):  # 'q' tuşuna basılırsa döngüden çık
        break

cv2.destroyAllWindows()  # Tüm pencereleri kapat
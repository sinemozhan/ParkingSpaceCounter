import cv2
import pickle
import numpy as np

# Park alanlarını kontrol eden fonksiyon
def checkParkSpace(imgDilate):
    spaceCounter = 0  # Boş park alanı sayacını sıfırla

    # Kaydedilmiş park alanı pozisyonlarını döngüyle gez
    for pos in posList:
        x, y = pos  # Pozisyonun x ve y koordinatlarını al

        # Park alanının görüntüdeki ilgili kısmını kırp
        img_crop = imgDilate[y: y + height, x:x + width]
        count = cv2.countNonZero(img_crop)  # Kırpılmış alandaki beyaz piksel sayısını hesapla

        threshold = 590  # Boş park alanı eşiği

        # Eğer beyaz piksel sayısı eşikten az ise park alanı boş
        if count < threshold:
            color = (0, 255, 0)  # Yeşil renk
            spaceCounter += 1  # Boş park alanı sayısını arttır
        else:
            color = (0, 0, 255)  # Kırmızı renk

        # Park alanının etrafını renkli dikdörtgen ile çiz
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)
        # Park alanındaki beyaz piksel sayısını görüntüye yaz
        cv2.putText(img, str(count), (x, y + height - 5), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

    # Görüntünün sol üst köşesine boş park alanı sayısını yaz
    cv2.putText(img, f"Free: {spaceCounter}/{len(posList)}", (15, 24), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)

width = 40  # Park alanı genişliği
height = 90  # Park alanı yüksekliği

# Video dosyasını aç
cap = cv2.VideoCapture("resim/otopark.mp4")

# Park alanı pozisyonlarını dosyadan yükle
with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

while True:
    success, img = cap.read()  # Videodan bir kare oku
    if not success:
        break  # Video biterse döngüden çık

    # Görüntüyü gri tona çevir
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Görüntüyü bulanıklaştır
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # Bulanık görüntüye adaptif eşikleme uygula
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # Eşiklenmiş görüntüyü medyan filtre ile daha da yumuşat
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    # Görüntüyü genişlet
    imgDilate = cv2.dilate(imgMedian, np.ones((3, 3)), iterations=1)

    # Park alanlarını kontrol et ve görüntü üzerinde işaretle
    checkParkSpace(imgDilate)

    # İşlenmiş görüntüyü göster
    cv2.imshow("img", img)
    # 'q' tuşuna basılırsa döngüden çık
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

cap.release()  # Video yakalamayı serbest bırak
cv2.destroyAllWindows()  # Tüm pencereleri kapat
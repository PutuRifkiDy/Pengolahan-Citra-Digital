from tkinter import *  # saya import library ini untuk menggunakan semua fungsi keperluan untuk membuat GUI 
from PIL import Image, ImageTk  # Digunakan untuk mengkonversi warna dari frame yang dihasilkan oleh opencv formatnya BGR ke format RGB format yang digunakan pada Tkinter agar webcam yang ditampilkan warnanya sesuai
import cv2  # saya mengimport library ini untuk mengakses webcam, mengubah gambar menjadi bentuk hsv, deteksi kontur, konversi warna, deteksi warna
import imutils  # saya mengimport library ini untuk gambar dari webcam yang diambil diubah ukurannya menjadi 720px
import numpy as np  # saya gunakan untuk mendefinisikan warna dalam bentuk format HSV dalam rentang batas bawah dan batas atas

root = Tk()  # saya mendefinisikan variabel root untuk membuat kontainer dari isi komponen-komponen yang terdapat pada tkinter
root.title('Deteksi Object Geometri Berdasarkan Bentuk dan Warna Menggunakan Library OpenCv, Tkinter, Pillow, Imutils, dan Numpy')  # memberikan judul pada aplikasi

# Variabel untuk menyimpan referensi ke webcam
kamera = cv2.VideoCapture(0)  # Membuka Kamera webcam lalu saya simpan ke variabel kamera, kenapa parameternya 0 karena angka 0 itu merepresentasikan kamera default kita atau kamera utama

# Definisikan range warna dalam HSV untuk deteksi
# untuk warna merah itu terdapat 2 bagian range pada Hue nya yaitu 0 derajat sampaii 8 derajat lalu 175 derajat sampai 180 derajat
# saya menggunakan numpy ini untuk menetapkan nilai batas atas dan nilai batas bawahnya
merahBawah1 = np.array([0, 100, 20], np.uint8)
merahAtas1 = np.array([8, 255, 255], np.uint8)
merahBawah2 = np.array([175, 100, 20], np.uint8)
merahAtas2 = np.array([180, 255, 255], np.uint8)

hijauBawah = np.array([36, 100, 20], np.uint8)  # range warna hijau itu disekitaran 36 derajat sampai 70, saya menetapkan  batas bawah dan batas atasnya
hijauAtas = np.array([70, 255, 255], np.uint8)
biruBawah = np.array([100, 100, 20], np.uint8)  # range warna dari biru itu dari 100 sampai 125 derjat saya menetapkan batas bawah dan batas atasnya
biruAtas = np.array([125, 255, 255], np.uint8)  # saya menggunakan tipe data uint8 karena nilainya tidak minus dan range nilainya dari 0 derajat sampai 255 derajat

# Fungsi untuk memproses frame webcam
def proses_gambar(frame): # frame adalah setiap gambar dalam sebuah vide
    frame = imutils.resize(frame, width=720) # frame saya ubah ukurannya menjadi 720 pixel agar prosesnya lebih cepet si python
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # mengubah format warna opencv yaitu BGR ke formar HSV menggunakan open cv

    # Deteksi warna sesuai pilihan
    if pilihWarna.get() == 0:  # Semua warna akan diditeksi
        maskerMerah1 = cv2.inRange(frameHSV, merahBawah1, merahAtas1) # saya menyaring pixel dalam gambar dengan range warna yang telah kita buat pada array numpy sebelumnya menggunakan fungsi pada open cv yaitu inRange
        maskerMerah2 = cv2.inRange(frameHSV, merahBawah2, merahAtas2) # jadi warna terdapat pada range tersebut maka akan berwarna putih menggunakan fungsi inrange itu 
        maskerMerah = cv2.add(maskerMerah1, maskerMerah2)
        maskerBiru = cv2.inRange(frameHSV, biruBawah, biruAtas)
        maskerHijau = cv2.inRange(frameHSV, hijauBawah, hijauAtas)
        masker = cv2.add(cv2.add(maskerMerah, maskerBiru), maskerHijau) 
    
    elif pilihWarna.get() == 1:  # Deteksi warna merah
        maskerMerah1 = cv2.inRange(frameHSV, merahBawah1, merahAtas1)
        maskerMerah2 = cv2.inRange(frameHSV, merahBawah2, merahAtas2)
        masker = cv2.add(maskerMerah1, maskerMerah2) # menggabungkan warna menjadi satu masker akhir

    elif pilihWarna.get() == 2:  # Deteksi warna hijau
        masker = cv2.inRange(frameHSV, hijauBawah, hijauAtas)

    elif pilihWarna.get() == 3:  # Deteksi warna biru
        masker = cv2.inRange(frameHSV, biruBawah, biruAtas)

    # Terapkan filter median
    masker = cv2.medianBlur(masker, 7) # menambahkan blur untuk memperhalus warna yang terdapat pada range. kenapa memilih 7 x 7 kernel kenapa tidak 3 x 3 atau 9 x 9 atau 11 x 11 karena jika memilih di bawah 7 x 7 itu hanya menghaluskan noise ringan  tetapi detail pada gambar masih terlihat sedangkan misal saya memilih lebih dari 7 x 7 maka detil gambar akan hilang seperti tekstur dan garis akan hilang

    # Konversi kembali gambar ke format RGB untuk ditampilkan ke Pkinternya atau GUI nya
    frameAkhir = cv2.cvtColor(frameHSV, cv2.COLOR_HSV2RGB)

    # Gambar sesuai dengan pilihan bentuk
    if bentuk.get() == 0:
        gambarSemua(masker, frameAkhir)
    elif bentuk.get() == 3:
        gambarSegitiga(masker, frameAkhir) # sesuai yang di pilih user nantinya
    elif bentuk.get() == 4:
        gambarPersegi(masker, frameAkhir)
    elif bentuk.get() == 5:
        gambarSegilima(masker, frameAkhir)
    elif bentuk.get() == 7:
        gambarLingkaran(masker, frameAkhir)

    im = Image.fromarray(frameAkhir) # mengonversi frameAkhir yang masih dalam bentuk array numpy menjadi object gambar
    img = ImageTk.PhotoImage(image=im) # mengubah format yang pkinternya tau atau dikenali yaitu menjadi Photo Image 
    lblHasilGambar.configure(image=img)
    lblHasilGambar.image = img

# Fungsi untuk menggambar berbagai bentuk (sama seperti sebelumnya)
def gambarSemua(masker, frameAkhir):
    kontur, _ = cv2.findContours(masker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    # Menemukan kontur objek dalam gambar berdasarkan masker (citra biner)
    # cv2.RETR_EXTERNAL: hanya mencari kontur di luar objek
    # cv2.CHAIN_APPROX_SIMPLE: menyederhanakan kontur dengan hanya menyimpan titik penting

    for c in kontur:  # Melakukan iterasi untuk setiap kontur yang ditemukan
        epsilon = 0.10 * cv2.arcLength(c, True)  # Menghitung keliling kontur dan menentukan seberapa banyak titik yang akan disimpan
        # epsilon = 10% dari panjang keliling kontur
        approx = cv2.approxPolyDP(c, epsilon, True)  # Menyederhanakan kontur dengan hanya menyimpan titik-titik penting

        area = cv2.contourArea(c)  # Menghitung luas area yang dibatasi oleh kontur

        if area > 3000:  # Hanya memproses objek yang memiliki area lebih besar dari 3000 piksel
            target = cv2.moments(c)  # Menghitung momen kontur untuk mendapatkan titik tengah (pusat massa)
            if target["m00"] == 0:  # Jika momen kontur memiliki nilai 0 (bukan area valid), kita set menjadi 1
                target["m00"] = 1
            x = int(target["m10"] / target["m00"])  # Menghitung koordinat x titik pusat
            y = int(target["m01"] / target["m00"])  # Menghitung koordinat y titik pusat
            cv2.circle(frameAkhir, (x, y), 5, (0, 0, 0), -1)  # Menggambar titik pusat pada frame akhir sebagai lingkaran kecil, dengan radius 5 warna hitam

            konturBaru = cv2.convexHull(c)  # Membuat kontur c menjadi lebih halus (menghilangkan detail tidak penting)
            cv2.drawContours(frameAkhir, [konturBaru], 0, (0, 0, 0), 3)  # Menggambar kontur baru dengan warna hitam dan ketebalan 3

def gambarSegitiga(masker, frameAkhir):
    kontur, _ = cv2.findContours(masker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Menemukan kontur segitiga
    for c in kontur:  # Iterasi untuk setiap kontur
        epsilon = 0.10 * cv2.arcLength(c, True)  # Menghitung keliling kontur dan menentukan toleransi penyederhanaan
        approx = cv2.approxPolyDP(c, epsilon, True)  # Menyederhanakan kontur
        if len(approx) == 3:  # Jika jumlah sisi kontur adalah 3, itu adalah segitiga
            target = cv2.moments(c)  # Menghitung momen kontur untuk menemukan titik tengah
            if target["m00"] == 0:  # Menangani kemungkinan pembagian dengan nol
                target["m00"] = 1
            x = int(target["m10"] / target["m00"])  # Menghitung posisi x titik pusat
            y = int(target["m01"] / target["m00"])  # Menghitung posisi y titik pusat
            cv2.circle(frameAkhir, (x, y), 5, (0, 0, 0), -1)  # Menggambar titik pusat objek
            konturBaru = cv2.convexHull(c)  # Membuat kontur lebih halus menghiraukan lekuk lekuk yang tidak perlu
            cv2.drawContours(frameAkhir, [konturBaru], 0, (0, 0, 0), 3)  # Menggambar kontur segitiga

def gambarPersegi(masker, frameAkhir):
    kontur, _ = cv2.findContours(masker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Menemukan kontur persegi
    for c in kontur:  # Iterasi untuk setiap kontur
        epsilon = 0.030 * cv2.arcLength(c, True)  # Menghitung keliling kontur dan menentukan toleransi penyederhanaan
        approx = cv2.approxPolyDP(c, epsilon, True)  # Menyederhanakan kontur
        if len(approx) == 4:  # Jika jumlah sisi kontur adalah 4, itu adalah persegi atau persegi panjang
            target = cv2.moments(c)  # Menghitung momen kontur untuk menemukan titik pusat
            if target["m00"] == 0:  # Menangani pembagian dengan nol
                target["m00"] = 1
            x = int(target["m10"] / target["m00"])  # Menghitung posisi x titik pusat
            y = int(target["m01"] / target["m00"])  # Menghitung posisi y titik pusat
            cv2.circle(frameAkhir, (x, y), 5, (0, 0, 0), -1)  # Menggambar titik pusat objek
            konturBaru = cv2.convexHull(c)  # Membuat kontur lebih halus
            cv2.drawContours(frameAkhir, [konturBaru], 0, (0, 0, 0), 3)  # Menggambar kontur persegi

def gambarSegilima(masker, frameAkhir):
    kontur, _ = cv2.findContours(masker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Menemukan kontur segilima
    for c in kontur:  # Iterasi untuk setiap kontur
        epsilon = 0.035 * cv2.arcLength(c, True)  # Menghitung keliling kontur dan menentukan toleransi penyederhanaan
        approx = cv2.approxPolyDP(c, epsilon, True)  # Menyederhanakan kontur
        if len(approx) == 5:  # Jika jumlah sisi kontur adalah 5, itu adalah segilima
            target = cv2.moments(c)  # Menghitung momen kontur untuk menemukan titik pusat
            if target["m00"] == 0:  # Menangani pembagian dengan nol
                target["m00"] = 1
            x = int(target["m10"] / target["m00"])  # Menghitung posisi x titik pusat
            y = int(target["m01"] / target["m00"])  # Menghitung posisi y titik pusat
            cv2.circle(frameAkhir, (x, y), 5, (0, 0, 0), -1)  # Menggambar titik pusat objek
            konturBaru = cv2.convexHull(c)  # Membuat kontur lebih halus
            cv2.drawContours(frameAkhir, [konturBaru], 0, (0, 0, 0), 3)  # Menggambar kontur segilima

def gambarLingkaran(masker, frameAkhir):
    kontur, _ = cv2.findContours(masker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Menemukan kontur lingkaran
    for c in kontur:  # Iterasi untuk setiap kontur
        epsilon = 0.030 * cv2.arcLength(c, True)  # Menghitung keliling kontur dan menentukan toleransi penyederhanaan
        approx = cv2.approxPolyDP(c, epsilon, True)  # Menyederhanakan kontur
        if len(approx) > 7:  # Jika jumlah sisi kontur lebih dari 7, itu kemungkinan besar lingkaran
            target = cv2.moments(c)  # Menghitung momen kontur untuk menemukan titik pusat
            if target["m00"] == 0:  # Menangani pembagian dengan nol
                target["m00"] = 1
            x = int(target["m10"] / target["m00"])  # Menghitung posisi x titik pusat
            y = int(target["m01"] / target["m00"])  # Menghitung posisi y titik pusat
            cv2.circle(frameAkhir, (x, y), 5, (0, 0, 0), -1)  # Menggambar titik pusat objek
            konturBaru = cv2.convexHull(c)  # Membuat kontur lebih halus
            cv2.drawContours(frameAkhir, [konturBaru], 0, (0, 0, 0), 3)  # Menggambar kontur lingkaran


# Membuat variabel untuk menyimpan pilihan warna dengan menggunakan IntVar, 
# yang akan digunakan untuk memilih warna yang diinginkan (misalnya Merah, Hijau, Biru, Semua warna).
pilihWarna = IntVar()

# Membuat label yang menampilkan teks "Pilih Warna" pada GUI dengan font tebal.
lblWarna = Label(root, text='Pilih Warna', font='bold')
lblWarna.grid(column=0, row=1, columnspan=2)  # Menempatkan label di kolom 0, baris 1, dan melebar di 2 kolom.

# Membuat beberapa tombol radio (radiobuttons) untuk memilih warna. 
# Setiap tombol akan mengubah nilai dari variabel pilihWarna sesuai dengan pilihan pengguna.
rbSemuaWarna = Radiobutton(root, text='Semua warna', value=0, variable=pilihWarna, command=lambda: proses_gambar(frameSaatIni))
rbMerah = Radiobutton(root, text='Merah', value=1, variable=pilihWarna, command=lambda: proses_gambar(frameSaatIni))
rbHijau = Radiobutton(root, text='Hijau', value=2, variable=pilihWarna, command=lambda: proses_gambar(frameSaatIni))
rbBiru = Radiobutton(root, text='Biru', value=3, variable=pilihWarna, command=lambda: proses_gambar(frameSaatIni))

# Menempatkan tombol radio untuk warna pada posisi grid yang sesuai.
rbSemuaWarna.grid(column=0, row=2)
rbMerah.grid(column=0, row=3)
rbHijau.grid(column=0, row=4)
rbBiru.grid(column=0, row=5)

# Membuat variabel untuk menyimpan pilihan bentuk (misalnya segitiga, persegi, lingkaran, dll.)
bentuk = IntVar()

# Membuat label yang menampilkan teks "Pilih Bentuk" pada GUI.
lblBentuk = Label(root, text="Pilih Bentuk")
lblBentuk.grid(column=1, row=1)  # Menempatkan label di kolom 1, baris 1.

# Membuat beberapa tombol radio (radiobuttons) untuk memilih bentuk. 
# Setiap tombol akan mengubah nilai dari variabel bentuk sesuai dengan pilihan pengguna.
rbSemuaBentuk = Radiobutton(root, text="Semua", value=0, variable=bentuk, command=lambda: proses_gambar(frameSaatIni))
rbSegitiga = Radiobutton(root, text="Segitiga", value=3, variable=bentuk, command=lambda: proses_gambar(frameSaatIni))
rbPersegi = Radiobutton(root, text="Persegi", value=4, variable=bentuk, command=lambda: proses_gambar(frameSaatIni))
rbSegilima = Radiobutton(root, text="Segilima", value=5, variable=bentuk, command=lambda: proses_gambar(frameSaatIni))
rbLingkaran = Radiobutton(root, text="Lingkaran", value=7, variable=bentuk, command=lambda: proses_gambar(frameSaatIni))

# Menempatkan tombol radio untuk bentuk pada posisi grid yang sesuai.
rbSemuaBentuk.grid(column=1, row=2)
rbSegitiga.grid(column=1, row=3)
rbPersegi.grid(column=1, row=4)
rbSegilima.grid(column=1, row=5)
rbLingkaran.grid(column=1, row=6)

# Membuat label yang akan menampilkan gambar hasil deteksi atau gambar yang telah diproses.
lblHasilGambar = Label(root)
lblHasilGambar.grid(column=2, row=1, rowspan=6)  # Label ini akan menempati beberapa baris pada grid.

# Fungsi untuk memperbarui gambar video dari webcam secara terus-menerus.
def perbarui_video():
    global frameSaatIni  # Menyimpan frame terbaru di variabel global
    ret, frame = kamera.read()  # Membaca frame baru dari webcam
    if ret:
        frameSaatIni = frame  # Menyimpan frame yang dibaca
        proses_gambar(frame)  # Memproses gambar (deteksi bentuk dan warna)
    lblHasilGambar.after(10, perbarui_video)  # Memperbarui gambar setiap 10 milidetik

# Memulai pembaruan video dengan menetapkan frameSaatIni ke None dan memanggil fungsi perbarui_video.
frameSaatIni = None
perbarui_video()  # Memulai pembaruan video.

root.mainloop()  # Menjalankan main loop Tkinter untuk GUI.

# Melepaskan akses webcam dan menutup semua jendela OpenCV setelah selesai.
kamera.release()
cv2.destroyAllWindows()

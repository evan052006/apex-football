# apex-football
## Link deployment PWS
https://christopher-evan41-apexfootball.pbp.cs.ui.ac.id/

## Membuat projek django baru
Pertama gunakan perintah "cd" untuk memasuki directory git repositorynya. Lalu buatlah virtual env dengan perintah.

`python -m venv env`

Ini akan menghindari clashing antar dependencies dan membuat environment lebih rapi secara umum. Lalu, aktifkan venvnya agar berlaku pada sesi terminal sekarang.

`source ./env/bin/activate`

Sekarang kita ketik file baru requirements.txt sesuai pada tutorial 0 untuk menyesuaikan library yang perlu diinstalasi.

```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
python-dotenv
```

Kemudian kita install setiap baris requirements.txt dengan pip dengan perintah

`pip install -r requirements.txt`

Setelah environment python sudah siap, gunakan perintah startproject yang disediakan django-admin untuk membuat aplikasi baru. Kita perlu menambahkan argumen "." pada perintah untuk mengspesifikasi dimana meletakkan projek barunya ("." menyatakan current directory)

`django-admin startproject apex_football .`

Berikutnya tambahkan file .env dengan isi

`PRODUCTION=False`

File .env bertujuan untuk mengatur environment variables saat server dijalankan pada lokal, yakni hanya untuk testing dahulu.

Lalu buatlah file .env.prod dengan isi

```
DB_NAME=<nama database>
DB_HOST=<host database>
DB_PORT=<port database>
DB_USER=<username database>
DB_PASSWORD=<password database>
SCHEMA=tugas_individu
PRODUCTION=True
```

Saya tidak akan lampirkan informasi DB demi keamanan, namun dapat dilihat file ini bertujuan untuk mengatur environment variables saat server dijalankan pada hosting aslinya (dalam tugas ini, pada PWS). Dan juga berisi kredensial database dan skema yang digunakan, karena ini merupakan tugas individu, saya menggunakan skema tersebut.

Namun .env dan .env.prod hanyalah file yang berisi pengaturannya, untuk benar - benar memuat nilai tersebut pada sistem (host yang menjalankan servernya), kita perlu modifikasi settings.py untuk membaca dan mengatur environment variabelnya. Bagian ini diletakkan bagian atas (setelah import path) agar settings.py dapat membaca environment variables yang telah diubah

```
...
import os
from dotenv import load_dotenv
load_dotenv()
...
```

Lalu dalam settings.py carilah variabel array bernama ALLOWED_HOSTS, kita akan tambahkan host lokal dan host yang digunakan PWS nanti. Pastikan bagian link HTTPS tidak dicantumkan.

```
...
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "christopher-evan41-apexfootball.pbp.cs.ui.ac.id"]
...
```

Lalu kita coba buat variabel baru (tepat diatas DEBUG). Yang akan mengambil environment variabel pada system untuk di assign ke variabel PRODUCTION di django.

`PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'`

Function getenv menerima parameter nama envrionment variabel, dan juga default jika environment variabelnya tidak ditemukan. Kemudian dengan konsep yang sama, kita set informasi konfigurasi database yang digunakan.

```
if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'OPTIONS': {
                'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

Jika server dijalankan dalam production, akan memakai database yang disediakan PWS yaitu postgresql. Kita tambahkan spesifikasi ini pada key 'ENGINE' dalam dictionarynya. Lalu informasi lain terkait name, user, host, dan sebagainya akan kita cuplik dari file .env.prod yang kita buat sebelumnya. Pada kunci options, kita tambahkan argumen baru yang akan secara default mengatur search path database pada skema tugas_individu. Jika database dijalankan lokal, kita pakai sqlite3 saja yang kita namakan berdasarkan direktori projek kita. Setelah selesai, jangan lupa lakukan migrasi database agar perubahan pada database akan tertampil pada server.

`python manage.py migrate`

Kita dapat lihat perintah terkait projek kita dapat kita jalankan dalam manage.py. Untuk menjalankan server, kita jalankan perintah

`python manage.py runserver`

Lalu akhirnya kita bisa jalankan projek pada lokal yaitu port 8000 secara default. Kita hanya perlu datang ke link localhost:8000.

## Membuat aplikasi main
Pertama kita jalankan perintah tersebut dalam manage.py

`python manage.py startapp main`

Jangan lupa untuk mendaftarkan aplikasi main ini pada list "INSTALLED_APPS" dalam settings.py

```
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]
...
```
Langkah ini penting agar Django dapat mengenal aplikasi apa saja pada folder projeknya.

## Melakukan routing pada proyek agar dapat menjalankan aplikasi main
Pertama kita perlu routing URL dari level projek hingga ke main. Ini dilakukan dengan modifikasi file urls.py dalam direktori apex_football dalam projek saya. Kita import function include dari django yang berfungsi untuk mengimpor pola URL dari aplikasi main.

```
...
from django.urls import path, include
...
```

Berikutnya kita hanya perlu tambahkan URL path yang mengarah pada main, dalam kasus ini kita buat saja kosong (jadi default / rootnya).

```
urlpatterns = [
    ...
    path('', include('main.urls')),
    ...
]
```

Namun belum selesai, dari main kita harus melakukan routing untuk display view berdasarkan URL yang diminta. Maka kita perlu buat file urls.py pada aplikasi main dan menulis view apa saja dengan URL apa yang ditampil.

```
from django.urls import path
from main.views import show_index

urlpatterns = [
    path('', index, name='index'),
]
```

Kita belum buat view index, maka langkah berikutnya dilanjutkan.

## Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.

Pada views.py dalam direktori main, kita akan tambahkan fungsi view bernama index yang menerima http request dan mengembalikannya sebagai html. Kita akan render requestnya dengan template index.html dimana kita input data nama, kelas, dan nama aplikasi dalam bentuk dictionary.

```
from django.shortcuts import render


def show_index(request):
    return render(
        request,
        "index.html",
        {
            "nama": "Christopher Evan Tanuwidjaja",
            "kelas": "A",
            "app_name": "main"
        }
    )
```

Sekarang kita perlu buat file html dalam folder templates dalam aplikasi main agar views.py dapat menampilkan response htmlnya.

```
<h1>Apex Football</h1>

<h3>Nama Aplikasi: </h3>
<p>{{ app_name }}</p> 
<h3>Nama: </h3>
<p>{{ nama }}</p> 
<h3>Kelas: </h3>
<p>PBP {{ kelas }}</p>
```

Akhirnya tertampil halaman HTML berdasarkan data tersebut. (ini terdapat dalam commit hash 8101f82c6ff42e96974601e927f9c088ae314f41)

## Membuat model pada aplikasi main dengan nama Product

Pertama kita modifikasi isi dari models.py dalam aplikasi main, kita tambahkan kelas baru "Product" yang inherit dari kelas Model yang diberikan django. Rencana toko football saya adalah memberikan pengguna kebebasan untuk memesan produk custom, tentunya diperlukan verifikasi secara manual. Sehingga saya tambahkan field "is_verified" untuk menandakan pesanan yang sudah diverifikasi kelayakannya. Dan juga saya tambahkan id sebagai primary key dalam database agar setiap order mudah diidentifikasinya secara unik.

```
class Product(models.Model):
    CATEGORIES = [
        ('FW', 'Footwear'),
        ('Sh', 'Shirts'),
        ('misc', 'Misc'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=1000)
    thumbnail = models.URLField(blank=True, null=True)
    category = models.URLField(max_length=20, choices=CATEGORIES, default='FW')
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
```

Jangan lupa setelah membuat model, kita jalankan perintah berikut untuk memperbarui migrasi sekarang.

```
python manage.py makemigrations
python manage.py migrate
```

Dalam konteks ini, "makemigrations" adalah bagaikan "git add" yang bertugas menyeleksi file yang ingin di commit, dan "migrate" adalah bagaikan "git commit" yang bertugas melakukan perubahan. Dalam konteks DB, perubahan bermaksud pada penambahan atau pengurangan field dan juga penambahan, pengurangan, ataupun modifikasi model baru.

## Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.

Setelah selesai, kita hanya perlu membuat projek baru pada PWS (Pacil Web Service). Lalu menggunggah projek ke remote pws dengan perintah berikut.

```
git remote add pws https://pbp.cs.ui.ac.id/christopher.evan41/apexfootball
```

Pertama kita perlu menambahkan remote pws yang disediakan ke git repository kita (Berbeda dengan remote "origin" yang disediakan github). Kita namakan remote ini "pws"

`git branch -M master`

Perintah ini membuat branch baru bernama master. Untuk disiapkan dipush.

`git push pws master`

Perintah ini akan push kode kita ke branch master yang baru dibuat ke repository pada PWS untuk dijalankan. Sebaiknya juga kita tambahkan environment variables production yang telah dibuat sebelumnya berdasarkan .env.prod. Hanya perlu kita tempelkan ke raw editor pada tab environment variables.

```
DB_HOST=...
DB_NAME=...
DB_PASSWORD=...
DB_PORT=...
DB_USER=...
DEBUG=False
PRODUCTION=True
SCHEMA=tugas_individu
```

## Bagan Django
![bagan](bagan.jpeg)

Hubungan pertama dimulai saat pengguna request konek pada web app kita. request ini akan melalui internet yakni pertama melewati modem. Setelah request tiba pada server, pertama akan dirouting melewati urls.py yang berada pada project level, lalu di arahkan lagi pada aplikasi. Setelah tiba di urls.py dalam aplikasi, akan diterima oleh berbagai view tergantung urlnya. View dapat berupa fungsi maupun class, namun fungsinya tetep sama yaitu menerima request HTML, lalu mengembalikan response (yang berupa HTML) berdasarkan request tersebut. views.py juga berinteraksi dengan models.py yang merupakan abstraksi atas operasi DB yang lebih rendah (seperti postgresql, sqlite3, dll). Interaksi model dan database saling request dan response, untuk update atau query DB pada server. Setelah views selesai menjalankan programnya, akan menghasilkan hasil response html yang umumnya merupakan template HTML dimana hanya beberapa nilai yang sebenarnya berubah. Akhirnya response HTML ini akan dikembalikan pada user melalui internet, lalu siklusnya berulang lagi.

## Peran settings.py
Secara umum settings.py berfungsi untuk menyimpan konfigurasi projek yang global, berikut beberapa penjelasan variabel pada settings.py.

- BASE_DIR : Path ke direktori akar dari projek
- DEBUG : Jika true, umumnya menampilkan log error yang berguna untuk development. Namun untuk Production sebaiknya dinonaktifkan karena dapat membuat celah keamanan.
- ALLOWED_HOSTS : Daftar alamat host yang melayani projek django tersebut. Saat debug adalah true dan ini kosong, django akan otomatis mengisi alamat lokal host.
- INSTALLED_APPS : Daftar aplikasi yang aktif dalam django project. Juga berisi aplikasi builtin django seperti admin.
- DATABASES : konfigurasi database suatu projek. Menggunakan sqlite3 secara default.
- STATIC_ROOT : Path ke direktori yang berisi file - file yang bersifat global atau ingin digunakan untuk seluruh projek, seperti gambar, CSS stylesheets, dll.
- STATIC_URL : URL yang digunakan untuk mengakses file dalam STATIC_ROOT, berfungsi agar organisasi static file lebih mudah.


## Cara kerja migrasi DB pada django
Migrasi database di Django adalah cara Django untuk mempropagasikan perubahan yang dibuat pada model (di models.py) ke dalam skema database. Perintah "makemigrations" akan membuat folder migrations pada BASE_DIR yang berisi perubahan model yang ingin dilakukan pada DB. Folder migrations ini bagaikan folder .git dalam git, yang berfungsi sebagai version control DB secara tidak langsung. Setelah sudah siap, kita jalankan perintah "migrate" yang akan menerapkan perubahan yang kita buat ke DB. Mekanisme ini membuat DB lebih reliable, karena jika kita membuat perubahan tidak sengaja pada models.py, kita dapat lebih mudah mengembalikan perubahan tersebut. 


## Mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
Menurut saya, salah satu faktor yang kuat adalah penerapannya yang mirip dengan python yakni "batteries included". Hal ini berarti sudah banyak library untuk mengembangkan fungsi yang umum dilakukan, hingga mempercepat web development. Bagi pengguna, library ini memberikan kesempatan untuk mengerti web development secara konsep level tinggi lebih mudah ketimbang mempelajari setiap aspek dari web development terlebih dahulu (seperti DB, front end development, etc)


## Feedback Tutorial 1
Belum ada feedback, sejauh ini masih lancar mengikuti tutorial :)

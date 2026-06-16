# Rekomendasi Pengembangan Hub-Feeder Menuju Pengalaman seperti SEVIMA ProFeeder

Dokumen ini menggabungkan hasil pembacaan aplikasi hub-feeder, perbandingan dengan NeoFeeder, serta pembandingan ulang terhadap acuan utama yaitu SEVIMA ProFeeder. Tujuannya adalah memberi masukan pengembangan yang konkret agar arah produk semakin sesuai dengan harapan pengguna.

## 1. Konteks dan Tujuan

Aplikasi hub-feeder saat ini tampaknya sedang diarahkan menjadi aplikasi perantara antara sistem akademik dan PDDIKTI/NeoFeeder. Dari sisi target produk, acuan yang paling relevan bukan hanya NeoFeeder, tetapi SEVIMA ProFeeder.

Hal ini penting karena beberapa calon/pengguna saat ini sudah terbiasa menggunakan ekosistem SEVIMA, kemungkinan kombinasi antara SIAKAD Cloud dan ProFeeder. Karena itu, ketika mereka meminta aplikasi baru, yang mereka bayangkan kemungkinan besar bukan sekadar aplikasi untuk mengirim data ke Feeder, melainkan pengalaman kerja yang mirip dengan SEVIMA:

- struktur menu yang familiar
- pola tampilan tabel, filter, dan tombol aksi yang mirip
- dashboard yang memberi gambaran kesiapan pelaporan
- validasi data sebelum pengiriman
- komparasi antara data akademik dan data Feeder
- kemampuan melihat error secara rinci
- kemampuan memperbaiki atau menyesuaikan data sebelum dikirim

Dengan demikian, tujuan pengembangan sebaiknya dirumuskan sebagai berikut:

> Hub-feeder dikembangkan secara bertahap menuju pengalaman kerja seperti SEVIMA ProFeeder, dimulai dari fondasi data dan pengiriman, lalu ditingkatkan menjadi alat validasi, komparasi, koreksi, dan monitoring pelaporan PDDIKTI.

## 2. Posisi Aplikasi Saat Ini

Berdasarkan pembacaan aplikasi, hub-feeder sudah memiliki fondasi awal yang cukup baik. Beberapa modul data sudah tersedia, tabel sudah berjalan, filter dan pagination sudah ada, dan sebagian proses pengiriman data ke Feeder sudah tersedia.

Hal-hal yang sudah baik antara lain:

- aplikasi sudah memakai stack modern berbasis Nuxt 3
- performa halaman relatif cepat
- login dan redirect dasar sudah berjalan
- beberapa modul inti sudah tersedia, seperti mahasiswa, mata kuliah, kelas kuliah, kurikulum, dosen pengajar, periode perkuliahan, dan pelaporan
- tabel, filter, dan pagination sudah menjadi pola umum
- sudah ada tombol pengiriman data pada beberapa halaman
- modul tambahan seperti Sister dan master data Feeder sudah mulai tersedia

Namun, jika dibandingkan dengan pengalaman ProFeeder, aplikasi saat ini masih lebih dekat ke tahap awal, yaitu:

> data viewer + manual sender

Sedangkan ProFeeder lebih dekat ke:

> operational reporting workbench

Artinya, ProFeeder bukan hanya tempat melihat dan mengirim data. ProFeeder membantu operator melalui seluruh siklus kerja pelaporan: menyiapkan data, memeriksa kesiapan, menemukan data bermasalah, membandingkan dengan Feeder, memperbaiki data, mengirim, lalu memantau hasilnya.

## 3. Harapan Pengguna yang Perlu Diterjemahkan ke Produk

Dari konteks bahwa pengguna sudah menggunakan SEVIMA dan menginginkan pengalaman serupa, ada tiga kebutuhan utama yang perlu diterjemahkan secara eksplisit.

### 3.1 Pengalaman yang Mirip SEVIMA

Yang dimaksud “seperti SEVIMA” kemungkinan bukan harus menyalin desain secara visual 1:1, tetapi mengikuti pola kerja yang sudah mereka kenal.

Pola yang perlu didekati:

- menu dikelompokkan berdasarkan area pelaporan
- dashboard menjadi pusat informasi status pelaporan
- setiap modul memiliki filter periode, program studi, dan status data
- setiap modul memiliki kartu ringkasan seperti jumlah data, data akan dikirim, data tidak valid, dan data tidak terhubung
- aksi utama diletakkan konsisten, misalnya unduh/sinkron, validasi, komparasi, kirim
- detail record bisa dibuka untuk melihat status dan pesan masalah

### 3.2 Validasi Sebelum Pengiriman

Pengguna menginginkan data bisa divalidasi sebelum dikirim. Ini sangat masuk akal karena operator pelaporan biasanya tidak ingin langsung mengirim data mentah ke Feeder tanpa mengetahui masalahnya.

Validasi yang diharapkan bukan hanya angka berhasil/gagal setelah kirim, melainkan pemeriksaan sebelum kirim, misalnya:

- field wajib belum terisi
- format email tidak sesuai
- format tanggal tidak valid
- NIK/NIM kosong atau tidak sesuai pola
- kode prodi belum termapping
- referensi agama, jalur masuk, periode, kelas, kurikulum, dan status mahasiswa belum cocok
- data duplikat
- data sudah ada di Feeder tetapi berbeda

Satu hal yang penting untuk tim pengembang: sebagian besar aturan validasi di atas tidak perlu dirancang dari nol. Aturan yang ditampilkan ProFeeder pada dasarnya mengikuti aturan Feeder PDDIKTI itu sendiri (field wajib, panjang maksimal, tipe data, dan referensi pada tiap web service Feeder). Jadi acuan paling tepat adalah dokumentasi/dictionary Feeder, bukan asumsi internal. Pendekatan yang ringan: lakukan pemeriksaan murah di sisi lokal (field wajib, format, panjang, referensi sudah termapping), lalu biarkan Feeder yang menjadi penentu akhir lewat respons errornya. Tidak perlu menduplikasi seluruh logika Feeder di lokal.

Hasil validasi idealnya ditampilkan dalam dua level:

1. ringkasan error, misalnya kolom apa yang paling banyak bermasalah
2. detail per record, agar operator tahu mahasiswa/mata kuliah/kelas mana yang harus diperbaiki

### 3.3 Data Bisa Dikurasi dan Disesuaikan untuk Kepentingan Akreditasi

Data yang ditampilkan dapat dikurasi, disesuaikan, dilengkapi, dan dikoreksi melalui staging area sebelum dikirim ke Feeder.

Hal ini penting agar aplikasi tetap berada dalam koridor tata kelola data yang baik. Jadi yang dibangun bukan manipulasi data tanpa jejak, tetapi mekanisme koreksi data yang aman dan bisa diaudit.

Fitur yang relevan:

- staging data sebelum kirim
- field override yang jelas
- alasan perubahan
- status approval jika diperlukan
- audit trail siapa mengubah apa dan kapan
- histori perubahan data
- pembeda antara data asli dari SIAKAD, data hasil koreksi di hub-feeder, dan data yang sudah terkirim ke Feeder
- export rekap untuk kebutuhan akreditasi

Dengan pendekatan ini, kebutuhan akreditasi tetap terlayani, tetapi aplikasi juga aman secara tata kelola.

## 4. Perbandingan dengan ProFeeder

Dari screenshot ProFeeder pada folder `screenshots/Sevima/`, terlihat beberapa pola utama.

### 4.1 Dashboard ProFeeder sebagai Command Center

Pada `Sevima/sevima-dashboard.png`, dashboard ProFeeder menampilkan:

- filter Periode/Semester
- jumlah mahasiswa belum terlapor
- aktivitas kuliah mahasiswa belum terlapor
- data tidak valid
- data tidak terhubung
- grafik perbandingan AKM Sistem Akademik vs AKM Feeder
- aktivitas yang sedang berjalan
- riwayat aktivitas beserta jumlah berhasil/gagal

Sementara pada hub-feeder, dashboard saat ini belum menjadi pusat monitoring pelaporan. Informasi status sync lebih banyak berada di halaman pelaporan dan belum berbasis periode secara kuat.

Rekomendasi:

- ubah dashboard menjadi pusat status pelaporan
- tampilkan filter periode sebagai kontrol utama
- tampilkan ringkasan data per status
- tampilkan grafik perbandingan data lokal vs Feeder
- tampilkan aktivitas berjalan dan riwayat proses nyata

### 4.2 Modul Operasional ProFeeder Punya Siklus Aksi Lengkap

Pada `Sevima/sevima-detail-periode-kuliah.png`, halaman modul ProFeeder memiliki pola:

- filter program studi
- filter status data
- filter periode
- kartu jumlah data Feeder
- kartu data akan dikirim
- kartu data tidak valid
- kartu data tidak terhubung
- tombol Unduh
- tombol Validasi
- tombol Komparasi
- tombol Kirim
- status per baris
- tombol detail per record

Pada hub-feeder, halaman list sudah ada, tetapi siklus aksinya belum lengkap. Tombol kirim ada, tetapi validasi dan komparasi belum menjadi bagian utama.

Rekomendasi:

- buat pola halaman standar untuk semua modul pelaporan
- urutan aksi sebaiknya: Unduh/Sinkron → Validasi → Komparasi → Koreksi → Kirim
- setiap record harus punya status yang jelas
- detail record harus bisa dibuka dan berfungsi

### 4.3 Komparasi Field-by-Field

Pada `Sevima/sevima-detail-komparasi.png`, ProFeeder menampilkan komparasi antara Data Akademik dan Data Feeder, lengkap dengan keterangan error.

Ini adalah salah satu fitur paling penting karena pengguna yang sudah terbiasa dengan ProFeeder akan mengharapkan kemampuan melihat perbedaan data sebelum mengambil keputusan.

Rekomendasi:

- tambahkan fitur komparasi antara data SIAKAD/hub dan data Feeder
- tampilkan perbedaan per field
- beri keterangan apakah data sama, berbeda, kosong, tidak valid, atau belum terhubung
- sediakan aksi untuk memperbarui staging data atau menandai data siap kirim

### 4.4 Rekap Error Validasi

Pada `Sevima/sevima-cek-rekap-error-validasi.png`, ProFeeder menampilkan ringkasan error validasi dengan kolom:

- Kolom
- Error Validasi
- Jumlah Error

Contohnya:

- Biaya Masuk wajib diisi
- Agama wajib diisi
- NIK/KTP wajib diisi
- Nama Ibu wajib diisi
- Email tidak sesuai format
- Email melebihi panjang maksimal

Hub-feeder saat ini belum memiliki rekap error seperti ini.

Rekomendasi:

- setelah proses validasi, tampilkan ringkasan error per kolom
- ringkasan harus bisa diklik untuk melihat daftar record terkait
- operator harus bisa melakukan perbaikan langsung atau menandai untuk diperbaiki di sumber data

### 4.5 Statistik Kesiapan Pelaporan

File seperti `sevima-stat-persiapan-lapor.png`, `sevima-statistik-data.png`, dan `sevima-stat-mhs-prodi.png` menunjukkan bahwa ProFeeder tidak hanya menampilkan data mentah, tetapi juga statistik kesiapan pelaporan.

Pada hub-feeder, halaman `/statistik` masih kosong.

Rekomendasi:

- jadikan `/statistik` sebagai halaman readiness pelaporan
- tampilkan kesiapan per periode, prodi, dan jenis data
- tampilkan tren data valid, tidak valid, tidak terhubung, terkirim, dan gagal kirim (memakai status baku pada 4.6)
- tampilkan statistik data agregat seperti jumlah mahasiswa per prodi, angkatan, dan status, sebagai pelengkap statistik kesiapan

### 4.6 Indikator Status Sinkronisasi yang Baku

Banyak istilah status muncul di berbagai layar ProFeeder, tetapi yang penting bukan istilahnya, melainkan adanya satu set status yang konsisten dan dipahami operator. Saat ini di hub-feeder istilah seperti "tidak terhubung" dan "tidak valid" belum didefinisikan secara eksplisit, sehingga berisiko ditafsirkan berbeda antar developer.

Rekomendasi: tetapkan satu daftar status sinkronisasi baku yang dipakai konsisten di kartu ringkasan, kolom status per baris, dan filter status data. Misalnya:

- Belum dikirim — data lokal yang belum pernah dikirim ke Feeder
- Tidak valid — gagal validasi lokal/Feeder, belum layak dikirim
- Tidak terhubung — data lokal yang belum punya pasangan di Feeder (belum ada ID Feeder)
- Berbeda — data ada di kedua sisi tetapi isinya tidak sama, butuh komparasi/koreksi
- Siap kirim — sudah valid dan siap diproses
- Terkirim — berhasil masuk ke Feeder
- Gagal kirim — ditolak Feeder, lengkap dengan alasannya

Yang penting bagi end-user: status ini harus tampil langsung di setiap baris data, misalnya berupa badge berwarna, sehingga operator bisa mengetahui kondisi tiap record secara sekilas tanpa harus membuka detail satu per satu. Status per baris ini juga menjadi dasar filter "status data", agar operator bisa langsung menyaring, misalnya hanya menampilkan yang "tidak valid" atau "belum dikirim".

Definisi ini perlu disepakati di awal karena hampir semua fitur lain (dashboard, validasi, komparasi, monitoring) bergantung pada arti status yang sama.

### 4.7 Rekap Ketidakcocokan dan Perubahan Data Mahasiswa

ProFeeder juga menyediakan rekap untuk kasus data yang tidak cocok antara sistem akademik dan Feeder, antara lain Daftar NIM Berbeda dan Daftar Perubahan Data Mahasiswa (PDM), serta pemeriksaan kelayakan sebelum proses tertentu (misalnya cek eligible/PIN). Hub-feeder belum memiliki rekap semacam ini, padahal kasus seperti NIM berbeda dan koreksi biodata sangat umum di lapangan.

Rekomendasi:

- sediakan daftar NIM/identitas yang berbeda antara data akademik dan data Feeder
- sediakan daftar perubahan data mahasiswa beserta status tindak lanjutnya
- jika ada proses yang memerlukan prasyarat, tampilkan pemeriksaan kelayakan sebelum aksi dijalankan

Rekap ini melengkapi alur komparasi pada 4.3, karena tidak semua ketidakcocokan bisa diselesaikan sekadar dengan mengirim ulang data.

## 5. Pemetaan Fitur Saat Ini terhadap Target ProFeeder

| Area | Kondisi Hub-Feeder Saat Ini | Target Bertahap seperti ProFeeder | Prioritas |
|---|---|---|---|
| Dashboard | Ada, tetapi belum menjadi pusat status pelaporan | Dashboard berbasis periode dengan status validasi, koneksi, dan pelaporan | Tinggi |
| List data | Sudah tersedia di beberapa modul | Dipertahankan, tetapi ditambah status dan aksi operasional | Tinggi |
| Pengiriman data | Ada pada sebagian modul | Tetap ada, tetapi didahului validasi dan komparasi | Tinggi |
| Validasi | Belum terlihat | Validasi pre-send per modul dan per record | Sangat tinggi |
| Rekap error | Belum tersedia | Rekap error per kolom dan daftar record bermasalah | Sangat tinggi |
| Komparasi | Belum tersedia | Komparasi data akademik vs data Feeder | Sangat tinggi |
| Detail record | Tombol detail mahasiswa terdeteksi tidak berfungsi | Detail record aktif dengan data, status, dan pesan error | Tinggi |
| Statistik | Halaman tersedia tetapi kosong | Statistik kesiapan pelaporan | Tinggi |
| Audit trail | Masih sangat terbatas/dummy | Riwayat aktivitas nyata per user, waktu, entitas, dan record | Tinggi |
| Koreksi/staging data | Belum jelas | Area koreksi sebelum kirim dengan histori perubahan | Sangat tinggi |
| Mapping referensi | Belum terlihat sebagai fitur utama | Mapping kode lokal ke referensi Feeder | Tinggi |
| Update/delete ke Feeder | Belum terlihat | Mendukung insert, update, delete/restore sesuai kebutuhan | Menengah-tinggi |
| Sandbox/live | Belum ada | Mode uji coba sebelum production | Menengah |
| Keamanan | Ada temuan client secret dan directory listing | Perlu hardening sebelum production serius | Tinggi |

## 6. Rekomendasi Roadmap Bertahap

Karena tujuan akhirnya cukup besar, pendekatan paling realistis adalah bertahap. Jangan langsung mengejar seluruh ProFeeder sekaligus. Lebih baik membangun fondasi workflow yang benar dulu.

### Tahap 1 — Menyamakan Pola Pengalaman Dasar

Tujuan tahap ini adalah membuat aplikasi terasa familiar bagi pengguna yang terbiasa dengan SEVIMA.

Rekomendasi pekerjaan:

1. Rapikan struktur menu mengikuti area pelaporan:
   - Dashboard
   - Operasional/Pelaporan
   - Statistik
   - Master/Referensi
   - Pengaturan

   Sebelum menata ulang, petakan dulu menu hub-feeder yang ada sekarang dan susunan modul ProFeeder, agar penataan benar-benar memperkecil jarak dengan kebiasaan pengguna, bukan sekadar mengganti label.

   Sebagai pertimbangan, berikut usulan struktur menu samping yang lebih rinci pada kelompok Operasional/Pelaporan, dikelompokkan per domain pelaporan:

   - **Mahasiswa**
     - Biodata
     - Riwayat Pendidikan
     - Nilai Transfer
     - Aktivitas Mahasiswa
       - Anggota Aktivitas
       - Pembimbing Aktivitas
       - Penguji Aktivitas
     - Konversi Kampus Merdeka
     - Prestasi Mahasiswa
   - **Matkul dan Kurikulum**
     - Mata Kuliah
       - Rencana Pembelajaran
       - Rencana Evaluasi
     - Kurikulum
       - Matkul Kurikulum
     - Substansi Kuliah
   - **Perkuliahan**
     - Kelas Kuliah
       - Pengajar
       - Peserta & Nilai
       - Komponen Evaluasi
     - Aktivitas Kuliah Mhs (AKM)
   - **Pelengkap**
     - Skala Nilai
     - Pengaturan Periode Kuliah

   Catatan: menu **Jalur Pendaftaran** (jalur masuk) adalah data referensi dari DIKTI, sehingga tempatnya di kelompok Master/Referensi, bukan di menu operasional di atas. Hal yang sama berlaku untuk referensi DIKTI lain (agama, wilayah, tahun ajaran, prodi, dan sejenisnya) yang dipakai untuk mapping pada Tahap 1 nomor 6.

   Catatan: **Aktivitas Kuliah Mahasiswa (AKM)** muncul sebagai entitas operasional di sini sekaligus sebagai metrik utama di dashboard dan statistik. Keduanya konsisten, tetapi pastikan tim memakai satu sumber data dan satu definisi AKM, agar tidak ada dua tempat berbeda yang menghitung hal yang sama dengan hasil yang bisa berbeda.
2. Buat layout standar halaman modul:
   - filter periode
   - filter prodi
   - filter status data
   - kartu ringkasan
   - tabel data
   - aksi utama
3. Pindahkan ringkasan status pelaporan ke dashboard utama.
4. Aktifkan halaman `/statistik` minimal untuk readiness sederhana.
5. Perbaiki tombol detail record yang tidak berfungsi.
6. Siapkan tabel referensi dan mapping kode lokal ke kode Feeder (prodi, agama, jalur masuk, status mahasiswa, periode, kurikulum). Ini didahulukan karena validasi (Tahap 2) dan komparasi (Tahap 4) sama-sama membutuhkannya.

Output tahap ini:

- aplikasi mulai terasa seperti alat kerja pelaporan, bukan hanya kumpulan tabel

### Tahap 2 — Validasi dan Rekap Error

Tujuan tahap ini adalah memenuhi kebutuhan utama pengguna: data dapat diperiksa sebelum dikirim.

Rekomendasi pekerjaan:

1. Buat service validasi per modul dengan dua lapis: pemeriksaan murah di lokal lalu konfirmasi akhir oleh Feeder.
2. Definisikan rule validasi dengan mengacu pada dictionary Feeder PDDIKTI, bukan asumsi internal:
   - required field
   - format
   - panjang karakter
   - referensi Feeder
   - relasi antar data
   - duplikasi
3. Tampilkan hasil validasi dalam kartu ringkasan:
   - total data
   - valid
   - tidak valid
   - belum lengkap referensi
4. Tampilkan rekap error validasi:
   - kolom
   - jenis error
   - jumlah error
5. Buat daftar record bermasalah yang bisa difilter berdasarkan jenis error.

Output tahap ini:

- operator bisa tahu masalah data sebelum pengiriman
- kebutuhan validasi sebelum kirim mulai terpenuhi

### Tahap 3 — Staging dan Koreksi Data untuk Kebutuhan Akreditasi

Tujuan tahap ini adalah memungkinkan data dikurasi sebelum dikirim, dengan tetap menjaga audit trail.

Rekomendasi pekerjaan:

1. Buat staging area untuk data pelaporan.
2. Simpan tiga versi data:
   - data asal SIAKAD
   - data koreksi/staging
   - data terakhir yang terkirim/terbaca dari Feeder
3. Izinkan koreksi field tertentu sebelum kirim.
4. Wajibkan alasan koreksi untuk field sensitif.
5. Simpan audit trail:
   - siapa mengubah
   - kapan mengubah
   - field apa yang diubah
   - nilai sebelum dan sesudah
   - alasan perubahan
6. Sediakan export untuk kebutuhan akreditasi.

Output tahap ini:

- kebutuhan “data bisa dimanipulasi” diterjemahkan menjadi koreksi data yang aman, transparan, dan bisa dipertanggungjawabkan

### Tahap 4 — Komparasi Data Akademik vs Feeder

Tujuan tahap ini adalah mendekati fitur pembeda utama ProFeeder.

Rekomendasi pekerjaan:

1. Ambil data pembanding dari Feeder.
2. Cocokkan berdasarkan key yang tepat, misalnya NIM, id_reg_pd, kode mata kuliah, id_kelas, id_sms, dan sebagainya.
3. Tampilkan komparasi field-by-field:
   - data akademik
   - data staging
   - data Feeder
   - status/keterangan
4. Tandai kondisi:
   - sama
   - berbeda
   - kosong
   - tidak valid
   - tidak terhubung
   - perlu update
5. Tambahkan aksi:
   - gunakan data akademik
   - gunakan data staging
   - sinkronkan dari Feeder
   - tandai siap kirim

Output tahap ini:

- operator bisa memahami gap antara data internal dan data Feeder sebelum melakukan pengiriman/update

### Tahap 5 — Monitoring Pengiriman dan Error Detail

Tujuan tahap ini adalah membuat proses pengiriman lebih terkendali.

Rekomendasi pekerjaan:

1. Buat job queue untuk proses kirim.
2. Tampilkan aktivitas sedang berjalan.
3. Tampilkan riwayat aktivitas:
   - entitas
   - periode
   - total data
   - berhasil
   - gagal
   - waktu proses
   - user yang menjalankan
4. Simpan error dari Feeder per record.
5. Buat halaman retry untuk data gagal.

Output tahap ini:

- operator tidak hanya tahu ada yang gagal, tetapi tahu data mana yang gagal dan kenapa

### Tahap 6 — Penyempurnaan Modul dan Operasi Feeder

Tujuan tahap ini adalah memperluas cakupan modul dan operasi agar lebih siap production.

Rekomendasi pekerjaan:

1. Tambah modul yang belum ada tetapi penting:
   - dosen lengkap
   - nilai kuliah
   - aktivitas kuliah
   - mahasiswa lulus/DO
   - bobot nilai
   - semester
   - daftar NIM berbeda dan perubahan data mahasiswa (PDM)
   - sandbox/live mode
2. Tambah operasi selain insert:
   - update
   - delete
   - restore bila relevan
3. Lengkapi mapping referensi yang belum tercakup di Tahap 1. Mapping inti sudah disiapkan lebih awal karena dibutuhkan validasi dan komparasi, jadi tahap ini tinggal menambah referensi yang belum tertangani.
4. Tambah scheduler jika dibutuhkan.

Output tahap ini:

- aplikasi bergerak dari push client menuju sync-hub yang lebih utuh

## 7. Catatan Keamanan dan Kesiapan Production

Ada beberapa catatan teknis yang sebaiknya tetap ditindaklanjuti sebelum aplikasi dipakai untuk data production secara serius. Khusus dua temuan pertama (client secret dan directory listing), keduanya sebaiknya diperbaiki lebih dulu, karena sudah terlihat dari luar tanpa autentikasi.

### 7.1 Client Secret Jangan Muncul di Frontend

Pada audit sebelumnya ditemukan konfigurasi client secret OAuth2 tercetak di HTML publik, termasuk Client ID Google Sign-In pada konfigurasi yang sama. Nilai-nilai ini sebaiknya dipindahkan ke backend.

Rekomendasi:

- gunakan backend-for-frontend atau API proxy
- simpan client secret hanya di server
- frontend cukup menerima token/session yang aman

### 7.2 Directory Listing Perlu Dimatikan

Path `/users/` sempat menampilkan directory listing Apache.

Rekomendasi:

- matikan directory listing dengan `Options -Indexes`
- pastikan route SPA tidak membuka struktur folder server

### 7.3 Audit Trail Perlu Menjadi Fitur Produk

Karena aplikasi akan dipakai untuk pelaporan dan kemungkinan koreksi data, audit trail bukan hanya fitur tambahan, tetapi bagian penting dari trust.

Minimal audit trail mencatat:

- login user
- proses validasi
- proses komparasi
- koreksi data
- pengiriman data
- hasil pengiriman
- retry data gagal

Satu catatan praktis: mekanisme audit trail ini sebaiknya sekaligus menjadi sumber "Riwayat Aktivitas" pada dashboard. Dengan begitu, mengganti log dummy yang ada sekarang dan membangun audit trail bukan dua pekerjaan terpisah, melainkan satu.

### 7.4 Security Header Belum Diperiksa

Pada audit, header keamanan seperti CSP, HSTS, dan X-Frame-Options belum sempat diperiksa terpisah. Sebelum production, sebaiknya dipastikan header dasar ini terpasang agar aplikasi lebih tahan terhadap clickjacking dan beberapa kelas serangan umum. Ini pekerjaan konfigurasi yang relatif ringan.

## 8. Prinsip Desain Produk yang Disarankan

Agar pengembangan tetap terarah, berikut prinsip yang bisa dipakai.

### 8.1 Jangan Langsung Kirim Data Mentah

Data sebaiknya melalui tahap:

1. masuk dari sumber
2. masuk staging
3. validasi
4. komparasi
5. koreksi jika perlu
6. approval jika perlu
7. kirim
8. monitoring hasil

### 8.2 Bedakan Data Sumber, Data Staging, dan Data Feeder

Ini penting agar pengguna tidak bingung.

- Data Sumber: data asli dari SIAKAD
- Data Staging: data yang sudah dikurasi untuk pelaporan
- Data Feeder: data yang sudah ada di PDDIKTI/NeoFeeder

Catatan istilah: pada layar komparasi (4.3 dan Tahap 4), "Data Sumber" inilah yang ditampilkan sebagai kolom "Data Akademik". Keduanya merujuk hal yang sama, jadi cukup pakai satu istilah secara konsisten di UI agar operator tidak bingung.

Agar pembedaan ini berguna secara teknis, simpan juga ID milik Feeder (misalnya `id_reg_pd`, `id_kls`, `id_aktivitas_mahasiswa`) di sisi lokal begitu sebuah record dikenali atau berhasil dikirim. ID inilah yang dipakai untuk menentukan sebuah data perlu di-insert atau di-update, sehingga pengiriman ulang tidak menghasilkan data ganda. Tanpa menyimpan ID Feeder, sinkronisasi akan cenderung insert-oriented dan sulit melakukan koreksi data yang sudah ada di Feeder.

### 8.3 Semua Koreksi Harus Ada Jejak

Kebutuhan akreditasi sering membutuhkan data yang rapi dan konsisten. Namun aplikasi tetap perlu menjaga integritas data.

Karena itu, koreksi boleh dilakukan, tetapi harus:

- jelas field-nya
- jelas alasan koreksinya
- jelas user-nya
- jelas waktunya
- bisa dilihat kembali histori perubahannya

### 8.4 UX Dibuat Familiar, Bukan Sekadar Mirip Tampilan

Meniru pengalaman SEVIMA sebaiknya tidak berhenti di warna, layout, atau menu. Yang lebih penting adalah meniru alur kerja yang sudah dipahami operator:

- pilih periode
- pilih prodi
- cek ringkasan
- validasi
- lihat error
- komparasi
- koreksi
- kirim
- pantau hasil

## 9. Kesimpulan Rekomendasi

Hub-feeder sudah memiliki fondasi awal yang baik untuk dikembangkan menjadi aplikasi pelaporan Feeder. Namun, jika tujuan akhirnya adalah mendekati pengalaman SEVIMA ProFeeder, maka fokus pengembangan perlu bergeser dari sekadar menambah tabel dan tombol kirim menjadi membangun workflow pelaporan yang lengkap.

Prioritas terpenting bukan langsung mengejar semua fitur sekaligus, melainkan membangun tahapan berikut secara bertahap:

1. samakan pola struktur aplikasi dengan pengalaman yang familiar bagi pengguna SEVIMA
2. jadikan dashboard sebagai pusat status pelaporan
3. tambahkan validasi sebelum kirim
4. tambahkan rekap error yang bisa ditindaklanjuti
5. tambahkan staging/koreksi data untuk kebutuhan akreditasi dengan audit trail
6. tambahkan komparasi data akademik vs Feeder
7. tambahkan monitoring pengiriman dan retry data gagal
8. perluas modul dan operasi Feeder secara bertahap

Dengan pendekatan ini, hub-feeder tidak harus langsung menjadi ProFeeder penuh sejak awal, tetapi punya jalur pengembangan yang jelas menuju pengalaman yang diharapkan oleh pengguna.

# Konsep Integrasi Feeder & SISTER via Web Service

Repository ini berisi catatan belajar untuk memahami cara mengintegrasikan aplikasi akademik kampus dengan layanan Dikti melalui web service, khususnya:

- **PDDikti Feeder / Neo Feeder** untuk pelaporan data akademik perguruan tinggi ke PDDikti.
- **SISTER API** untuk integrasi data sumber daya dosen, kepegawaian, dan Tridharma.

Fokus repo ini bukan membuat aplikasi siap produksi, melainkan menyusun pemahaman arsitektur, alur data, autentikasi, strategi sinkronisasi, mapping data, dan contoh akses web service yang dapat dijadikan dasar implementasi di aplikasi akademik.

---

## Indeks Dokumen

| Dokumen | Fokus | Kapan Dibaca |
|---------|-------|--------------|
| [FEEDER.md](./FEEDER.md) | Konsep pelaporan PD-DIKTI dengan NeoFeeder melalui web service, struktur request/response, fungsi utama, entitas data, dan strategi otomatisasi. | Saat ingin memahami integrasi SIAKAD dengan Feeder/PDDikti. |
| [SISTER.md](./SISTER.md) | Konsep integrasi aplikasi akademik atau sistem kepegawaian dengan SISTER API, termasuk token, `id_sdm`, endpoint Tridharma, write via API, queue, retry, dan rate limiting. | Saat ingin memahami integrasi data dosen, kepegawaian, dan Tridharma dengan SISTER. |

File pendukung:

| File | Keterangan |
|------|------------|
| [Mapping Tabel Feeder.xlsx](./Mapping%20Tabel%20Feeder.xlsx) | Bahan mapping tabel/field untuk kebutuhan integrasi Feeder. |
| [python-script/feeder_connect.py](./python-script/feeder_connect.py) | Contoh script koneksi sederhana ke web service Feeder. |
| [feeder_utama.png](./feeder_utama.png) | Gambar pendukung dokumentasi Feeder. |

---

## Gambaran Umum

### PDDikti Feeder / Neo Feeder

Feeder adalah pintu integrasi pelaporan data akademik perguruan tinggi ke PDDikti. Melalui web service, aplikasi akademik kampus dapat mengirim atau mengambil data seperti mahasiswa, program studi, kelas kuliah, KRS, nilai, aktivitas perkuliahan, dan data pelaporan semester lain.

Pola umum integrasi Feeder:

1. Aplikasi akademik menyimpan data operasional kampus.
2. Data dipetakan ke struktur data Feeder/PDDikti.
3. Aplikasi mengambil token dari web service Feeder.
4. Aplikasi memanggil fungsi Feeder menggunakan pola request JSON, misalnya `GetToken`, `GetDictionary`, `GetListMahasiswa`, atau fungsi insert/update sesuai kebutuhan.
5. Data divalidasi, dikirim, lalu disinkronkan ke PDDikti sesuai alur operasional kampus.

### SISTER API

SISTER API digunakan oleh perguruan tinggi yang memiliki sistem akademik atau sistem kepegawaian sendiri agar data dosen dan aktivitas Tridharma dapat terhubung dengan SISTER Cloud. Integrasi ini mencakup data kepegawaian, pengajaran, penelitian, pengabdian, publikasi, jabatan, sertifikasi, dan data dosen lain.

Pola umum integrasi SISTER:

1. Aplikasi meminta token melalui endpoint `/authorize`.
2. Aplikasi mengambil data SDM dari `/referensi/sdm`.
3. `id_sdm` disimpan di database lokal sebagai kunci utama integrasi dosen.
4. Aplikasi mengambil atau mengirim data Tridharma dan kepegawaian berdasarkan endpoint yang tersedia.
5. Proses bulk sync sebaiknya dijalankan melalui queue, retry, dan rate limiting.

---

## Perbedaan Fokus Feeder dan SISTER

| Aspek | Feeder / PDDikti | SISTER |
|-------|-------------------|--------|
| Domain utama | Pelaporan akademik perguruan tinggi | Data dosen, kepegawaian, dan Tridharma |
| Objek utama | Mahasiswa, prodi, kelas, KRS, nilai, aktivitas kuliah | Dosen/SDM, pengajaran, penelitian, pengabdian, jabatan |
| Pola API | Web service Feeder dengan request JSON berbasis `act` | REST-like API dengan endpoint dan Bearer Token |
| Kunci integrasi penting | Token Feeder, kode/id entitas akademik | Token SISTER, `id_sdm` |
| Dokumen repo | [FEEDER.md](./FEEDER.md) | [SISTER.md](./SISTER.md) |

---

## Urutan Belajar yang Disarankan

1. Baca [FEEDER.md](./FEEDER.md) untuk memahami konteks pelaporan PDDikti dan pola request web service NeoFeeder.
2. Pelajari mapping data pada [Mapping Tabel Feeder.xlsx](./Mapping%20Tabel%20Feeder.xlsx).
3. Coba pahami contoh koneksi di [python-script/feeder_connect.py](./python-script/feeder_connect.py).
4. Baca [SISTER.md](./SISTER.md) untuk memahami integrasi data dosen dan Tridharma melalui SISTER API.
5. Bandingkan domain data Feeder dan SISTER agar tidak mencampur tanggung jawab kedua layanan.

---

## Catatan Implementasi

- Selalu mulai dari environment sandbox atau development sebelum menyentuh production.
- Jangan hardcode kredensial API di source code.
- Simpan token di cache, bukan di database permanen.
- Simpan identifier penting seperti `id_sdm` secara lokal setelah berhasil resolve.
- Gunakan queue untuk proses sinkronisasi massal.
- Tambahkan logging yang mencatat endpoint, payload ringkas, response, dan context dosen/mahasiswa/prodi terkait.
- Siapkan retry dan mekanisme dead-letter untuk data yang gagal diproses.

---

## Referensi Eksternal

- [Informasi API SISTER versi Cloud](https://sister.kemdiktisaintek.go.id/panduan/detail/21829793658649) - menjelaskan kebutuhan SISTER API untuk PT yang memiliki sistem kampus/kepegawaian sendiri, endpoint sandbox dan production, autentikasi token, serta penggunaan `id_sdm`.
- [Dokumentasi API SISTER Production](https://sister-api.kemdiktisaintek.go.id/ws.php/1.0#overview)
- [Dokumentasi API SISTER Sandbox](https://sister-api.kemdiktisaintek.go.id/ws-sandbox.php/1.0#overview)
- [Contoh dokumentasi publik API PDDikti Feeder di Postman](https://www.postman.com/winter-meteor-495675-1/feeder-unu/documentation/3oivat2/doc-api-feeder) - memuat contoh pola `POST /ws/live2.php`, `GetToken`, token, `filter`, `order`, `limit`, dan `offset`.
- [User Guide PDDikti Web Service](https://text-id.123dok.com/document/zw3lp4ly-3-user-guide-pddikti-web-service.html) - referensi historis web service PDDikti, termasuk konsep interoperabilitas dan daftar method seperti `GetToken`, `GetDictionary`, `GetRecordset`, `InsertRecord`, dan `UpdateRecord`.

---

## Status Repo

Repo ini bersifat dokumentatif dan eksploratif. Gunakan isinya sebagai bahan belajar dan rancangan awal sebelum membangun integrasi produksi yang lengkap, tervalidasi, dan sesuai aturan operasional perguruan tinggi.

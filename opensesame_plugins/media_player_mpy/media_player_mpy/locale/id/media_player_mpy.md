# Plugin Media Player berbasis MoviePy

Hak Cipta 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

Plugin media_player_mpy menambahkan kemampuan memutar video ke [pembuat eksperimen OpenSesame][opensesame]. Plugin ini menggunakan [Moviepy][mpy_home] sebagai basis. Plugin ini seharusnya mampu menangani sebagian besar format video dan audio modern, meskipun penting bahwa stream mereka tidak rusak. Jika file tidak tampak berfungsi, lihat apakah Anda dapat menemukan versi yang lebih baik, atau coba untuk meng-encode ulang ke format yang berbeda.

Pemutaran terbaik akan dicapai dengan menggunakan backend Psychopy atau Expyriment yang dipercepat oleh hardware. Kinerja mungkin kurang jika menggunakan legacy dan film memiliki resolusi tinggi atau frame rate tinggi.

## Pengaturan plugin
Plugin ini menawarkan opsi konfigurasi berikut dari GUI:

- *File Video* - file video yang akan diputar. Bidang ini memungkinkan notasi variabel seperti [video_file], di mana Anda dapat menentukan nilainya dalam item loop.
- *Memutar audio* - menentukan apakah video akan diputar dengan audio atau dalam keadaan hening (dibisukan).
- *Sesuaikan video ke layar* - menentukan apakah video harus diputar dalam ukuran aslinya, atau jika video tersebut harus ditingkatkan ukurannya untuk menyesuaikan ukuran jendela/layar. Prosedur penskalaan ini mempertahankan rasio aspek asli dari film.
- *Loop* - menentukan apakah video harus di-loop, yang berarti video itu akan memulai lagi dari awal begitu akhir film telah tercapai.
- *Durasi* - Menentukan berapa lama film harus ditampilkan. Meminta nilai dalam hitungan detik, 'keypress' atau 'mouseclick'. Jika memiliki salah satu dari nilai terakhir, pemutaran akan berhenti saat sebuah tombol ditekan atau tombol mouse di-klik.

## Kode Python yang disesuaikan untuk menangani kejadian tekan tombol dan klik mouse
Plugin ini juga menawarkan fungsi untuk mengeksekusi kode penanganan acara kustom setelah setiap frame, atau setelah penekanan tombol atau klik mouse (Perhatikan bahwa eksekusi kode setelah setiap frame membuat opsi 'keypress' dalam bidang durasi menjadi tidak berarti; Tekanan tombol Escape tetap diawasi). Hal ini misalnya berguna, jika seseorang ingin menghitung berapa kali peserta menekan spasi (atau tombol lainnya) selama waktu tayangan film.

Beberapa variabel yang dapat diakses dalam skrip yang Anda masukkan di sini adalah:

- `continue_playback` (True atau False) - Menentukan apakah film harus terus diputar. Variabel ini diatur True secara default selama film sedang diputar. Jika Anda ingin menghentikan pemutaran dari skrip Anda, cukup atur variabel ini ke False dan pemutaran akan berhenti.
- `exp` - Sebuah variabel kenyamanan yang mengarah ke objek self.experiment
- `frame` - Jumlah frame yang sedang ditampilkan
- `mov_width` - Lebar film dalam px
- `mov_height` - Tinggi film dalam px
- `paused` - *True* ketika pemutaran sedang dijeda, *False* jika film sedang berjalan
- `event` - Variabel ini agak spesial, karena isinya tergantung pada apakah sebuah tombol atau tombol mouse ditekan selama frame terakhir. Jika hal ini tidak terjadi, variabel event akan hanya mengarah ke *None*. Jika sebuah tombol ditekan, event akan berisi tuple dengan di posisi pertama nilai "key" dan di posisi kedua nilai tombol yang ditekan, misalnya ("key","space"). Jika tombol mouse di-klik, variabel event akan berisi tuple dengan di posisi pertama nilai "mouse" dan di posisi kedua jumlah tombol mouse yang ditekan, misalnya ("mouse", 2). Dalam kesempatan langka bahwa beberapa tombol atau tombol ditekan pada saat yang sama selama frame, variabel event akan berisi daftar acara-acara ini, misalnya [("key","space"),("key", "x"),("mouse",2)]. Dalam hal ini, Anda perlu melalui daftar ini dalam kode Anda dan menarik semua acara yang relevan bagi Anda.

Selain variabel-variabel ini, Anda juga memiliki fungsi-fungsi berikut tersedia:

- `pause()` - Menjeda pemutaran saat film sedang berjalan, dan tidak menjeda jika sebaliknya (Anda dapat menganggapnya sebagai tombol pause/unpause)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/
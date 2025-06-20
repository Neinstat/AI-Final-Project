<template>
  <div id="dashboard-modern">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Face AI Suite</h1>
        <p class="hero-subtitle">
          Explore Advanced Facial Analysis & Similarity
        </p>
        <button @click="goToFaceComparison" class="cta-button">
          Get Started <span class="arrow">&rarr;</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardPageModern", // Component name can also be 'DashboardPage' to match the filename
  methods: {
    // Method to navigate to the Face Comparison page
    goToFaceComparison() {
      this.$router.push("/face-comparison");
    },
  },
};
</script>

<style>
/* Mengimpor font modern dari Google Fonts */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"); /* Menambah weight 500 */

/* Global Box Sizing */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0; /* Reset margin default browser */
  padding: 0; /* Reset padding default browser */
}

html,
body {
  overflow-x: hidden; /* Mencegah scroll horizontal jika ada elemen yang keluar batas */
}

#dashboard-modern {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: "Poppins", Arial, sans-serif;
  background: linear-gradient(
    135deg,
    #e0eafc 0%,
    /* Warna lebih cerah untuk awal gradien */ #cfdef3 100%
      /* Warna lebih lembut untuk akhir gradien */
  );
  padding: 20px;
  perspective: 1000px; /* Untuk efek 3D pada animasi jika diinginkan */
}

.hero-section {
  background: #ffffff;
  padding: 45px 55px; /* Sedikit menambah padding */
  border-radius: 20px; /* Sudut lebih membulat */
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08), 0 5px 15px rgba(0, 0, 0, 0.05); /* Bayangan lebih halus dan berlapis */
  text-align: center;
  max-width: 700px;
  width: 100%;
  transition: transform 0.35s cubic-bezier(0.25, 0.8, 0.25, 1),
    box-shadow 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
  opacity: 0; /* Awalnya tidak terlihat, untuk animasi */
  transform: translateY(30px) scale(0.98); /* Posisi awal untuk animasi */
  animation: fadeInSlideUp 0.8s 0.2s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; /* Animasi masuk */
}

/* Keyframes untuk animasi masuk card */
@keyframes fadeInSlideUp {
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.hero-section:hover {
  transform: translateY(-8px) scale(1.01); /* Efek mengangkat sedikit lebih dinamis */
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.1), 0 8px 20px rgba(0, 0, 0, 0.07); /* Bayangan lebih kuat saat hover */
}

.hero-content {
  /* Menambahkan class ini untuk menampung elemen yang akan dianimasikan secara berurutan */
  /* Tidak perlu style khusus di sini jika hanya untuk grouping animasi,
     tapi bisa ditambahkan jika ada kebutuhan layout internal */
}

.hero-title {
  font-size: 3rem; /* Sedikit lebih besar */
  font-weight: 700;
  color: #2c3e50; /* Warna gelap yang lebih modern (biru tua keabuan) */
  margin-bottom: 18px;
  line-height: 1.25;
  letter-spacing: -0.5px; /* Mengurangi sedikit spasi antar huruf untuk judul besar */
  /* Animasi untuk judul */
  opacity: 0;
  transform: translateY(20px);
  animation: elementFadeInUp 0.7s 0.5s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}

.hero-subtitle {
  font-size: 1.25rem; /* Sedikit lebih besar */
  color: #525f7f; /* Warna abu-abu yang lebih kaya */
  margin-bottom: 35px;
  font-weight: 400; /* Menggunakan bobot reguler untuk kontras dengan judul */
  line-height: 1.6;
  /* Animasi untuk subjudul */
  opacity: 0;
  transform: translateY(20px);
  animation: elementFadeInUp 0.7s 0.7s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}

/* Keyframes untuk animasi masuk elemen teks dan tombol */
@keyframes elementFadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.cta-button {
  padding: 16px 40px; /* Padding lebih besar untuk area klik yang nyaman */
  font-size: 1.15rem;
  font-weight: 600; /* Atau 500 untuk tampilan yang sedikit lebih ringan */
  cursor: pointer;
  border: none;
  border-radius: 10px; /* Sudut tombol lebih membulat */
  background: linear-gradient(
    90deg,
    #5e72e4 0%,
    /* Biru yang lebih vibrant */ #825ee4 100%
      /* Ungu sebagai bagian dari gradien */
  );
  color: white;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 5px 20px rgba(94, 114, 228, 0.35);
  display: inline-flex;
  align-items: center;
  text-transform: uppercase; /* Opsi: membuat teks tombol kapital */
  letter-spacing: 0.5px; /* Menambah sedikit spasi antar huruf pada tombol */
  /* Animasi untuk tombol */
  opacity: 0;
  transform: translateY(20px);
  animation: elementFadeInUp 0.7s 0.9s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}

.cta-button:hover,
.cta-button:focus {
  /* Tambahkan :focus untuk aksesibilitas */
  background: linear-gradient(
    90deg,
    #4a5ccf 0%,
    /* Warna lebih gelap saat hover */ #7149cf 100%
  );
  box-shadow: 0 8px 25px rgba(94, 114, 228, 0.45);
  transform: translateY(-3px) scale(1.03); /* Efek mengangkat dan membesar sedikit */
  outline: none; /* Hapus outline default pada focus jika styling custom sudah cukup */
}

.cta-button:active {
  /* Efek saat tombol ditekan */
  transform: translateY(-1px) scale(1.01);
  box-shadow: 0 4px 15px rgba(94, 114, 228, 0.3);
}

.cta-button .arrow {
  margin-left: 12px;
  font-size: 1.4rem;
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.cta-button:hover .arrow,
.cta-button:focus .arrow {
  transform: translateX(6px);
}

/* Penyesuaian responsif */

/* Untuk tablet dan layar sedang */
@media (max-width: 768px) {
  #dashboard-modern {
    padding: 20px;
  }

  .hero-section {
    padding: 35px 40px;
    max-width: 90%;
  }

  .hero-title {
    font-size: 2.5rem; /* Disesuaikan dengan peningkatan ukuran dasar */
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .cta-button {
    padding: 14px 32px;
    font-size: 1.05rem;
  }
}

/* Untuk ponsel dan layar kecil */
@media (max-width: 480px) {
  #dashboard-modern {
    padding: 15px;
  }

  .hero-section {
    padding: 30px 25px; /* Padding lebih disesuaikan */
    max-width: 95%;
    border-radius: 15px; /* Mungkin sedikit mengurangi radius di layar kecil */
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 0.95rem;
  }

  .cta-button {
    padding: 12px 25px;
    font-size: 0.95rem;
  }

  .cta-button .arrow {
    font-size: 1.2rem;
  }
}
</style>

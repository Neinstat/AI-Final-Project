<template>
  <div id="dashboard-modern">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Face AI Suite</h1>
        <p class="hero-subtitle">
          Jelajahi Analisis & Kesamaan Wajah Tingkat Lanjut
        </p>
        <button @click="goToFaceComparison" class="cta-button">
          Mulai Sekarang <span class="arrow">&rarr;</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardPageModern", // Mengganti nama komponen untuk kejelasan
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
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap");

/* Global Box Sizing */
*,
*::before,
*::after {
  box-sizing: border-box;
}

#dashboard-modern {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* Menggunakan min-height untuk cakupan viewport penuh */
  font-family: "Poppins", Arial, sans-serif; /* Font modern */
  background: linear-gradient(
    135deg,
    #f5f7fa 0%,
    #c3cfe2 100%
  ); /* Latar belakang gradien halus */
  margin: 0;
  padding: 20px; /* Padding utama untuk halaman, akan disesuaikan di media query */
  /* box-sizing: border-box; sudah dicakup oleh global di atas */
}

.hero-section {
  background: #ffffff;
  padding: 40px 50px; /* Padding internal card, akan disesuaikan */
  border-radius: 15px; /* Sudut yang lebih membulat */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* Bayangan yang lebih menonjol untuk efek kedalaman */
  text-align: center;
  max-width: 680px; /* Sedikit ditingkatkan dari 600px untuk desktop yang lebih lebar */
  width: 100%; /* Memastikan card mengambil lebar penuh hingga max-width */
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out; /* Transisi halus untuk hover */
}

.hero-section:hover {
  transform: translateY(-5px); /* Efek mengangkat sedikit saat hover */
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12); /* Bayangan sedikit lebih besar saat hover */
}

.hero-title {
  font-size: 2.8rem; /* Ukuran judul lebih besar */
  font-weight: 700; /* Bobot font tebal untuk judul */
  color: #333; /* Warna lebih gelap untuk kontras yang lebih baik */
  margin-bottom: 15px;
  line-height: 1.2; /* Ketinggian baris untuk keterbacaan */
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #555; /* Warna lebih lembut untuk subjudul */
  margin-bottom: 30px;
  font-weight: 300; /* Bobot font lebih ringan */
}

.cta-button {
  padding: 15px 35px;
  font-size: 1.1rem;
  font-weight: 600; /* Bobot font sedang untuk tombol */
  cursor: pointer;
  border: none;
  border-radius: 8px; /* Sudut tombol yang sedikit membulat */
  background: linear-gradient(
    90deg,
    #4a90e2 0%,
    #2479e7 100%
  ); /* Gradien biru modern */
  color: white;
  transition: all 0.3s ease; /* Transisi halus untuk semua properti */
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4); /* Bayangan halus untuk kedalaman tombol */
  display: inline-flex; /* Untuk menyelaraskan teks dan panah */
  align-items: center; /* Untuk menyelaraskan teks dan panah */
}

.cta-button:hover {
  background: linear-gradient(
    90deg,
    #2479e7 0%,
    #4a90e2 100%
  ); /* Membalik gradien saat hover */
  box-shadow: 0 6px 20px rgba(74, 144, 226, 0.5); /* Bayangan yang ditingkatkan saat hover */
  transform: translateY(-2px); /* Efek mengangkat sedikit saat hover */
}

.cta-button .arrow {
  margin-left: 10px; /* Jarak antara teks dan panah */
  font-size: 1.3rem; /* Ukuran panah sedikit lebih besar */
  transition: transform 0.3s ease; /* Transisi untuk gerakan panah */
}

.cta-button:hover .arrow {
  transform: translateX(5px); /* Menggerakkan panah saat hover */
}

/* Penyesuaian responsif */

/* Untuk tablet dan layar sedang */
@media (max-width: 768px) {
  #dashboard-modern {
    padding: 20px; /* Pertahankan padding atau sesuaikan jika perlu */
  }

  .hero-section {
    padding: 30px 35px; /* Kurangi padding internal card */
    max-width: 90%; /* Memungkinkan card mengambil persentase lebih besar dari layar yang lebih kecil */
  }

  .hero-title {
    font-size: 2.2rem; /* Kurangi ukuran font judul */
  }

  .hero-subtitle {
    font-size: 1rem; /* Kurangi ukuran font subjudul */
  }

  .cta-button {
    padding: 12px 28px;
    font-size: 1rem;
  }
}

/* Untuk ponsel dan layar kecil */
@media (max-width: 480px) {
  #dashboard-modern {
    padding: 15px; /* Kurangi padding utama untuk layar sangat kecil */
  }

  .hero-section {
    padding: 25px 20px; /* Kurangi padding internal card lebih lanjut */
    max-width: 95%; /* Card mengambil hampir seluruh lebar yang tersedia */
  }

  .hero-title {
    font-size: 1.8rem; /* Ukuran font judul lebih kecil lagi */
  }

  .hero-subtitle {
    font-size: 0.9rem; /* Ukuran font subjudul lebih kecil lagi */
  }

  .cta-button {
    padding: 10px 20px;
    font-size: 0.9rem;
  }

  .cta-button .arrow {
    font-size: 1.1rem;
  }
}
</style>

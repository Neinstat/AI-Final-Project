<template>
  <div id="app">
    <aside class="sidebar">
      <div class="logo">FaceSim</div>
      <nav>
        <ul>
          <li :class="{ active: currentPage === 'home' }">
            <a href="#" @click.prevent="navigateTo('home')">Face Comparison</a>
          </li>
          <li :class="{ active: currentPage === 'analyze-photo' }">
            <a href="#" @click.prevent="navigateTo('analyze-photo')"
              >Analyze Photo</a
            >
          </li>
          <li :class="{ active: currentPage === 'about' }">
            <a href="#" @click.prevent="navigateTo('about')">About Us</a>
          </li>
          <li :class="{ active: currentPage === 'contact' }">
            <a href="#" @click.prevent="navigateTo('contact')">Contact</a>
          </li>
        </ul>
      </nav>
    </aside>

    <div class="main">
      <header class="header">
        <h1 v-if="currentPage === 'home'">Face Similarity Checker</h1>
        <h1 v-else-if="currentPage === 'analyze-photo'">Photo Analyzer</h1>
        <h1 v-else-if="currentPage === 'about'">About Us</h1>
        <h1 v-else-if="currentPage === 'contact'">Contact</h1>
      </header>

      <section class="page-content">
        <div v-if="currentPage === 'home'" class="page home-page">
          <section class="card">
            <div class="upload-section">
              <label
                class="file-drop"
                @dragover.prevent
                @drop.prevent="onDropComparison($event, 1)"
              >
                <input
                  type="file"
                  ref="file1Comparison"
                  @change="uploadImage1"
                  accept="image/*"
                  hidden
                />
                <span v-if="!image1Url">Drop or click to upload Image 1</span>
                <img v-if="image1Url" :src="image1Url" alt="Preview 1" />
              </label>
              <label
                class="file-drop"
                @dragover.prevent
                @drop.prevent="onDropComparison($event, 2)"
              >
                <input
                  type="file"
                  ref="file2Comparison"
                  @change="uploadImage2"
                  accept="image/*"
                  hidden
                />
                <span v-if="!image2Url">Drop or click to upload Image 2</span>
                <img v-if="image2Url" :src="image2Url" alt="Preview 2" />
              </label>
            </div>

            <div class="card-section model-selection-section">
              <label for="model-select" class="form-label"
                >Choose Comparison Model:</label
              >
              <select
                id="model-select"
                v-model="selectedModel"
                class="form-select"
              >
                <option
                  v-for="model in availableModels"
                  :key="model.value"
                  :value="model.value"
                >
                  {{ model.text }}
                </option>
              </select>
            </div>

            <button
              class="btn-predict"
              @click="predictSimilarity"
              :disabled="!image1 || !image2 || isProcessing"
            >
              <span v-if="!isProcessing">Predict Similarity</span>
              <span v-else class="btn-loading">Processing...</span>
            </button>
            <div v-if="comparisonResult !== null" class="result-box">
              Similarity:
              <strong
                >{{
                  comparisonResult.similarity_percentage.toFixed(2)
                }}%</strong
              >
              <br />
              Distance:
              <strong>{{ comparisonResult.distance.toFixed(4) }}</strong>
              <br />
              Verified: <strong>{{ comparisonResult.verified }}</strong>
              <br />
              Model Used: <strong>{{ comparisonResult.model_used }}</strong>
            </div>
            <div v-if="comparisonError" class="error-box">
              {{ comparisonError }}
            </div>
          </section>
        </div>

        <div v-if="currentPage === 'about'" class="page about-page">
          <div class="card">
            <h2>About Us</h2>
            <p>
              Welcome to FaceSim! We are dedicated to providing state-of-the-art
              face similarity detection and analysis services. Our team
              leverages AI and machine learning to deliver accurate results.
            </p>
          </div>
        </div>

        <div v-if="currentPage === 'contact'" class="page contact-page">
          <div class="card">
            <h2>Contact</h2>
            <p>
              Have questions or feedback? Reach out to us at:
              <a href="mailto:support@facesim.example.com"
                >support@facesim.example.com</a
              >
            </p>
            <p>Or follow us on social media for updates and news.</p>
          </div>
        </div>

        <div
          v-if="currentPage === 'analyze-photo'"
          class="page analyze-photo-page"
        >
          <section class="card">
            <h2 class="section-title">Analyze Age, Gender, and Emotion</h2>
            <div class="upload-section">
              <label
                class="file-drop"
                @dragover.prevent
                @drop.prevent="onDropAnalyze"
              >
                <input
                  type="file"
                  ref="analyzeFile"
                  @change="handleAnalysisFileChange"
                  accept="image/*"
                  hidden
                />
                <span v-if="!analysisImagePreview"
                  >Drop or click to upload an image for analysis</span
                >
                <img
                  v-if="analysisImagePreview"
                  :src="analysisImagePreview"
                  alt="Image Preview for Analysis"
                />
              </label>
            </div>

            <div class="submit-section">
              <button
                @click="submitAnalysis"
                :disabled="!analysisImage || analysisIsLoading"
                class="btn-submit"
              >
                <span v-if="!analysisIsLoading">Analyze Image</span>
                <span v-else class="btn-loading">Processing...</span>
              </button>
            </div>

            <div v-if="analysisResults" class="result">
              <h3>Age: {{ analysisResults.age }}</h3>
              <h3>Gender: {{ analysisResults.gender }}</h3>
              <h3>Emotion: {{ analysisResults.emotion }}</h3>
            </div>

            <div v-if="analysisIsLoading" class="loading-overlay">
              <div class="spinner"></div>
              <p>Processing...</p>
            </div>

            <div v-if="analysisErrorMessage" class="error">
              <p>{{ analysisErrorMessage }}</p>
            </div>
          </section>
        </div>
      </section>

      <footer class="footer">
        © {{ new Date().getFullYear() }} FaceSim. All rights reserved.
      </footer>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "FaceApplication", // Nama komponen diubah agar lebih umum
  data() {
    return {
      currentPage: "home", // Halaman default
      // Data untuk Face Comparison
      image1: null,
      image2: null,
      image1Url: null,
      image2Url: null,
      comparisonResult: null,
      comparisonError: null,
      isProcessing: false, // Loading state untuk comparison
      selectedModel: "DeepFace", // Model default untuk comparison
      availableModels: [
        // Daftar model yang bisa dipilih
        { value: "VGG-Face", text: "VGG-Face" },
        { value: "Facenet", text: "Facenet" },
        { value: "Facenet512", text: "Facenet512" },
        { value: "OpenFace", text: "OpenFace" },
        { value: "DeepFace", text: "DeepFace (Default)" },
        { value: "ArcFace", text: "ArcFace" },
        // { value: "Dlib", text: "Dlib SFace" },
      ],

      // Data untuk Analyze Photo
      analysisImage: null, // File untuk analisis
      analysisImagePreview: null, // URL preview untuk gambar analisis
      analysisResults: null, // Hasil analisis (usia, gender, emosi)
      analysisErrorMessage: null,
      analysisIsLoading: false, // Loading state untuk analisis
    };
  },
  methods: {
    navigateTo(page) {
      this.currentPage = page;
      // Reset state halaman sebelumnya jika perlu
      this.resetComparisonState();
      this.resetAnalysisState();
    },

    // --- Metode untuk Face Comparison ---
    resetComparisonState() {
      this.image1 = null;
      this.image2 = null;
      this.image1Url = null;
      this.image2Url = null;
      this.comparisonResult = null;
      this.comparisonError = null;
      this.isProcessing = false;
    },
    onDropComparison(e, slot) {
      const file = e.dataTransfer.files[0];
      if (!file || !file.type.startsWith("image/")) return;
      if (slot === 1) {
        // Menggunakan $refs yang spesifik untuk comparison
        if (this.$refs.file1Comparison)
          this.$refs.file1Comparison.files = e.dataTransfer.files;
        this.uploadImage1({ target: { files: e.dataTransfer.files } });
      } else {
        if (this.$refs.file2Comparison)
          this.$refs.file2Comparison.files = e.dataTransfer.files;
        this.uploadImage2({ target: { files: e.dataTransfer.files } });
      }
    },
    uploadImage1(event) {
      const file = event.target.files[0];
      if (!file) {
        this.image1 = null;
        this.image1Url = null;
        return;
      }
      this.image1 = file;
      this.image1Url = URL.createObjectURL(this.image1);
      this.comparisonResult = null;
      this.comparisonError = null;
    },
    uploadImage2(event) {
      const file = event.target.files[0];
      if (!file) {
        this.image2 = null;
        this.image2Url = null;
        return;
      }
      this.image2 = file;
      this.image2Url = URL.createObjectURL(this.image2);
      this.comparisonResult = null;
      this.comparisonError = null;
    },
    async predictSimilarity() {
      if (!this.image1 || !this.image2) {
        this.comparisonError = "Please upload both images.";
        return;
      }
      this.isProcessing = true;
      this.comparisonError = null;
      this.comparisonResult = null;

      try {
        // Upload image 1
        const formData1 = new FormData();
        formData1.append("image1", this.image1);
        await axios.post("http://127.0.0.1:5000/upload_image1", formData1);

        // Upload image 2
        const formData2 = new FormData();
        formData2.append("image2", this.image2);
        await axios.post("http://127.0.0.1:5000/upload_image2", formData2);

        // Compare photos dengan model yang dipilih
        const res = await axios.post("http://127.0.0.1:5000/compare_photos", {
          model_name: this.selectedModel, // Kirim model yang dipilih
        });
        this.comparisonResult = res.data;
      } catch (err) {
        this.comparisonError =
          err.response?.data?.error ||
          err.message ||
          "An error occurred during similarity prediction.";
      } finally {
        this.isProcessing = false;
      }
    },

    // --- Metode untuk Analyze Photo ---
    resetAnalysisState() {
      this.analysisImage = null;
      this.analysisImagePreview = null;
      this.analysisResults = null;
      this.analysisErrorMessage = null;
      this.analysisIsLoading = false;
    },
    onDropAnalyze(e) {
      const file = e.dataTransfer.files[0];
      if (!file || !file.type.startsWith("image/")) return;
      // Menggunakan $refs yang spesifik untuk analysis jika diperlukan & memanggil handler yang benar
      if (this.$refs.analyzeFile)
        this.$refs.analyzeFile.files = e.dataTransfer.files;
      this.handleAnalysisFileChange({
        target: { files: e.dataTransfer.files },
      });
    },
    handleAnalysisFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.analysisImage = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.analysisImagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
        this.analysisResults = null;
        this.analysisErrorMessage = null;
      } else {
        this.analysisImage = null;
        this.analysisImagePreview = null;
      }
    },
    async submitAnalysis() {
      if (!this.analysisImage) {
        this.analysisErrorMessage = "Please upload an image for analysis.";
        return;
      }
      this.analysisIsLoading = true;
      this.analysisErrorMessage = null;
      this.analysisResults = null;

      const formData = new FormData();
      // Backend untuk analysis menggunakan 'image1.jpg' setelah diupload oleh /upload_image1
      // Jadi, kita harus mengupload gambar analisis ke endpoint /upload_image1 terlebih dahulu.
      formData.append("image1", this.analysisImage);

      try {
        await axios.post("http://127.0.0.1:5000/upload_image1", formData);
        const response = await axios.post(
          "http://127.0.0.1:5000/analyze_photo"
        );
        this.analysisResults = response.data;
        if (response.data.error) {
          // Jika backend mengembalikan error dalam response.data
          this.analysisErrorMessage = response.data.error;
          this.analysisResults = null;
        }
      } catch (error) {
        this.analysisErrorMessage =
          error.response?.data?.error ||
          error.message ||
          "An error occurred during analysis.";
      } finally {
        this.analysisIsLoading = false;
      }
    },
  },
};
</script>

<style>
/* ... (CSS dari respons sebelumnya tetap sama) ... */
/* Tambahan CSS untuk Model Selection */

.card-section {
  /* Kelas umum untuk padding dan margin dalam card */
  margin-bottom: 1.5rem; /* Sesuaikan dengan kebutuhan */
  width: 100%;
}

.model-selection-section {
  display: flex;
  flex-direction: column; /* Label di atas dropdown */
  align-items: flex-start; /* Rata kiri */
  gap: 0.5rem; /* Jarak antara label dan select */
}

.form-label {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-select {
  width: 100%; /* Lebar penuh */
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: var(--text-primary);
  background-color: var(--white);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  appearance: none; /* Hilangkan tampilan default browser */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='%23333' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3E%3C/svg%3E"); /* Kustom panah dropdown */
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1em;
}

.form-select:focus {
  outline: none;
  border-color: var(--blue-primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--blue-primary-rgb, 48, 97, 232), 0.25); /* Definisikan --blue-primary-rgb jika perlu atau gunakan hex */
}

/* Perbaikan untuk --blue-primary-rgb (tambahkan ini di :root jika belum ada, atau ganti rgba dengan warna solid) */
:root {
  /* ... variabel lain ... */
  --blue-primary-rgb: 48, 97, 232; /* RGB dari #3061e8 */
}

/* CSS dari respons sebelumnya yang relevan harus disertakan di sini */
/* Global Resets & Box Sizing */
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow-x: hidden; /* Prevent horizontal scroll on body */
  font-smooth: antialiased;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

/* Global Color Palette - Disesuaikan untuk tampilan yang lebih modern */
:root {
  --blue-dark: #0a2540; /* Biru tua untuk sidebar, aksi primer */
  --blue-primary: #3061e8; /* Biru primer yang lebih cerah untuk aksen dan interaksi */
  --blue-primary-rgb: 48, 97, 232; /* RGB dari #3061e8 */
  --blue-accent: #596893; /* Biru aksen (sebelumnya primer) untuk teks sekunder atau elemen pendukung */
  --blue-light: #e0e7ff; /* Biru muda untuk highlight atau latar belakang sekunder */
  --bg: #f7f9fc; /* Latar belakang netral yang sangat terang */
  --text-primary: #1f2937; /* Teks gelap utama untuk keterbacaan */
  --text-secondary: #4b5563; /* Teks lebih terang untuk info sekunder */
  --white: #ffffff;
  --border-color: #d1d5db; /* Warna border netral */

  --success-bg: #e6f7f0; /* Latar belakang untuk pesan sukses */
  --success-text: #067647; /* Warna teks untuk pesan sukses */
  --success-border: #067647; /* Warna border untuk pesan sukses */

  --error-bg: #fdecea; /* Latar belakang untuk pesan error */
  --error-text: #c53030; /* Warna teks untuk pesan error */
  --error-border: #c53030; /* Warna border untuk pesan error */

  --sidebar-width: 250px; /* Lebar sidebar sedikit ditingkatkan */
  --header-height: 65px; /* Tinggi header disesuaikan */
}

/* Layout */
#app {
  display: flex;
  min-height: 100vh;
  font-family: "Roboto", sans-serif; /* Tetap menggunakan Roboto */
  background: var(--bg);
  color: var(--text-primary);
  width: 100%;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  background: var(--blue-dark);
  color: var(--white);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border-right: 1px solid #081e33; /* Border halus untuk pemisahan */
  flex-shrink: 0;
  transition: width 0.3s ease;
}
.logo {
  font-size: 2rem; /* Logo lebih besar dan tebal */
  font-weight: 700;
  margin-bottom: 2.5rem;
  color: var(--white);
  padding-left: 0.5rem; /* Penyesuaian padding kiri */
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  width: 100%;
}
.sidebar nav li {
  margin: 0.5rem 0; /* Spasi antar item menu */
}
.sidebar nav a {
  color: #a7b0c9; /* Warna teks untuk item tidak aktif */
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  display: block;
  padding: 0.85rem 1rem; /* Padding yang lebih nyaman */
  border-radius: 8px; /* Sudut membulat untuk tautan */
  transition: color 0.2s ease, background-color 0.2s ease, transform 0.2s ease;
}
.sidebar nav li.active a {
  /* State aktif yang lebih jelas */
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--white);
  font-weight: 600;
}
.sidebar nav a:hover:not(.active) {
  /* Hover untuk item tidak aktif */
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--white);
  transform: translateX(3px);
}

/* Main Content */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* Memungkinkan konten utama untuk scroll */
  height: 100vh;
}
.header {
  background: var(--white); /* Header lebih terang */
  color: var(--text-primary);
  padding: 0 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color); /* Border bawah halus */
  display: flex;
  align-items: center;
  height: var(--header-height);
  flex-shrink: 0; /* Mencegah header menyusut */
}
.header h1 {
  font-size: 1.5rem; /* Ukuran judul header disesuaikan */
  font-weight: 600;
  margin: 0;
}

.page-content {
  flex: 1;
  padding: 2rem; /* Padding lebih besar untuk konten halaman */
  display: flex;
  flex-direction: column;
  align-items: center; /* Memusatkan card secara horizontal */
  overflow-y: auto;
}

/* Card */
.card {
  background: var(--white);
  padding: 2.5rem; /* Padding internal card ditingkatkan */
  border-radius: 16px; /* Radius sudut lebih besar */
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.07); /* Bayangan lebih halus */
  width: 100%;
  max-width: 750px; /* Lebar maksimum card disesuaikan */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 2rem; /* Jarak antar card jika ada beberapa */
}

.section-title {
  /* Styling untuk judul seksi seperti di "Analyze Photo" */
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2rem;
  text-align: center;
}

/* Upload Section */
.upload-section {
  display: flex;
  gap: 2rem; /* Jarak antar area upload */
  justify-content: center;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}
.file-drop {
  flex: 1;
  min-width: 250px; /* Lebar minimum area upload */
  background-color: #f7f9fc; /* Latar belakang terang untuk dropzone */
  border: 2px dashed var(--border-color); /* Border dashed yang lebih halus */
  border-radius: 12px; /* Radius sudut konsisten */
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s ease, border-color 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 220px; /* Tinggi area upload disesuaikan */
  position: relative; /* Untuk ikon atau elemen terposition lainnya */
}
.file-drop::before {
  /* Ikon placeholder (Upload) - gunakan SVG untuk tampilan lebih baik */
  content: "↑"; /* Panah sederhana, ganti dengan ikon SVG/font */
  font-size: 2.5rem;
  color: var(--blue-primary);
  margin-bottom: 1rem;
  display: block;
  line-height: 1;
}
.file-drop:hover {
  background-color: var(--blue-light);
  border-color: var(--blue-primary); /* Warna border berubah saat hover */
}
.file-drop span {
  /* Teks di dalam area upload */
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.file-drop img {
  /* Preview gambar */
  max-width: calc(100% - 1rem);
  max-height: calc(100% - 3.5rem); /* Disesuaikan berdasarkan teks dan ikon */
  display: block;
  margin: 0.5rem auto 0;
  border-radius: 8px;
  object-fit: contain;
  position: absolute; /* Menutupi teks/ikon placeholder saat gambar ada */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--white); /* Jika gambar transparan */
  padding: 0.25rem;
}
/* Sembunyikan teks/ikon placeholder saat gambar ada */
.file-drop img ~ span,
.file-drop img ~ br,
.file-drop img ~ ::before {
  display: none;
}

/* Buttons (Gaya Terpadu) */
.btn-predict,
.btn-submit {
  width: 100%;
  background: var(--blue-primary); /* Menggunakan biru primer yang cerah */
  color: var(--white);
  border: none;
  padding: 0.9rem 1rem; /* Padding tombol disesuaikan */
  font-size: 1.1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.btn-predict:hover:not(:disabled),
.btn-submit:hover:not(:disabled) {
  background: var(--blue-dark); /* Lebih gelap saat hover */
  transform: translateY(-2px); /* Efek mengangkat halus */
}
.btn-predict:disabled,
.btn-submit:disabled {
  background-color: var(--blue-accent); /* Warna untuk state disabled */
  opacity: 0.7;
  cursor: not-allowed;
}
.btn-loading::after {
  /* Spinner pada tombol */
  content: "";
  display: inline-block;
  margin-left: 0.75rem;
  width: 16px; /* Spinner lebih kecil */
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.7);
  border-top-color: var(--white);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* Kotak Hasil & Error */
.result-box,
.analyze-photo-page .result {
  margin-top: 2rem;
  padding: 1.25rem;
  background: var(--success-bg);
  color: var(--success-text);
  border: 1px solid var(--success-border);
  border-left-width: 4px; /* Border kiri yang khas */
  border-radius: 8px;
  text-align: center;
}
.analyze-photo-page .result h3 {
  /* Styling untuk h3 di dalam hasil analisis */
  margin: 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 500;
}
/* Hilangkan margin atas/bawah untuk elemen h3 pertama/terakhir */
.analyze-photo-page .result h3:first-child {
  margin-top: 0;
}
.analyze-photo-page .result h3:last-child {
  margin-bottom: 0;
}

.error-box,
.analyze-photo-page .error {
  margin-top: 2rem;
  padding: 1.25rem;
  background: var(--error-bg);
  color: var(--error-text);
  border: 1px solid var(--error-border);
  border-left-width: 4px;
  border-radius: 8px;
  text-align: center;
}

/* Overlay Loading & Spinner (untuk "Analyze Photo") */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.85); /* Overlay lebih transparan */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 16px; /* Sesuaikan dengan radius card */
  z-index: 10;
}
.spinner {
  /* Spinner utama untuk overlay */
  width: 40px;
  height: 40px;
  border: 4px solid var(--blue-light);
  border-top-color: var(
    --blue-primary
  ); /* Warna primer untuk bagian aktif spinner */
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}
.loading-overlay p {
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 500;
}

/* Footer */
.footer {
  color: var(--text-secondary);
  text-align: center;
  padding: 1.5rem; /* Padding lebih besar */
  font-size: 0.875rem;
  background-color: var(--white); /* Latar belakang footer yang bersih */
  border-top: 1px solid var(--border-color); /* Border atas halus */
  margin-top: auto; /* Mendorong footer ke bawah jika konten pendek */
  flex-shrink: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsiveness */
/* Tablet besar / Desktop kecil */
@media (max-width: 992px) {
  .sidebar {
    width: 200px; /* Sidebar sedikit lebih sempit */
  }
  .logo {
    font-size: 1.75rem;
  }
  .card {
    max-width: 90%; /* Card mengambil persentase lebar */
  }
}

/* Tablet & Perangkat Mobile (Lanskap) */
@media (max-width: 768px) {
  .sidebar {
    /* Sidebar menjadi bar atas */
    width: 100%;
    height: auto;
    position: static; /* Atau 'sticky' jika ingin tetap di atas saat scroll */
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
  }
  .logo {
    margin-bottom: 0;
    font-size: 1.5rem;
  }
  .sidebar nav {
    width: auto;
  }
  .sidebar nav ul {
    display: flex;
    justify-content: flex-end;
    margin: 0;
  }
  .sidebar nav li {
    margin: 0 0.25rem;
  }
  .sidebar nav a {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
  .sidebar nav li.active a {
    /* State aktif untuk bar horizontal */
    background-color: transparent;
    color: var(--blue-primary);
    border-bottom: 2px solid var(--blue-primary);
    border-radius: 0; /* Hilangkan radius untuk efek garis bawah */
  }
  .sidebar nav a:hover:not(.active) {
    /* Hover untuk bar horizontal */
    background-color: transparent;
    color: var(--blue-primary);
    transform: none;
  }

  #app {
    flex-direction: column; /* Tata letak utama menjadi kolom */
  }
  .main {
    height: auto; /* Tinggi main content otomatis */
  }
  .header {
    height: var(--header-height);
    padding: 0 1rem;
  }
  .header h1 {
    font-size: 1.25rem;
  }
  .page-content {
    padding: 1.5rem 1rem; /* Padding konten halaman disesuaikan */
  }
  .card {
    width: 100%; /* Card mengambil lebar penuh */
    max-width: 100%;
    padding: 1.5rem; /* Padding card dikurangi */
    margin-top: 0; /* Hilangkan margin atas jika card adalah view utama */
    border-radius: 12px;
  }
  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .upload-section {
    /* Area upload menjadi kolom */
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .file-drop {
    min-width: unset;
    width: 100%;
    height: 180px; /* Tinggi area upload disesuaikan untuk mobile */
    padding: 1rem;
  }
  .file-drop::before {
    /* Ikon placeholder lebih kecil di mobile */
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
  .file-drop span {
    font-size: 0.875rem;
  }

  .btn-predict,
  .btn-submit {
    /* Tombol disesuaikan untuk mobile */
    padding: 0.8rem;
    font-size: 1rem;
  }
  .result-box,
  .analyze-photo-page .result,
  .error-box,
  .analyze-photo-page .error {
    /* Kotak hasil/error di mobile */
    margin-top: 1.5rem;
    padding: 1rem;
    font-size: 0.9rem;
  }
}

/* Perangkat Mobile Sangat Kecil */
@media (max-width: 480px) {
  .sidebar {
    /* Bar atas di layar sangat kecil */
    padding: 0.5rem;
  }
  .logo {
    font-size: 1.3rem;
  }
  .sidebar nav a {
    padding: 0.4rem 0.5rem;
    font-size: 0.8rem;
  }
  .header h1 {
    font-size: 1.1rem;
  }
  .page-content {
    padding: 1rem 0.75rem;
  }
  .card {
    padding: 1rem;
    border-radius: 8px; /* Radius sudut lebih kecil */
  }
  .section-title {
    font-size: 1.3rem;
  }
  .file-drop {
    height: 160px; /* Tinggi area upload lebih lanjut disesuaikan */
  }
}
</style>

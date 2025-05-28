<template>
  <div id="app">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="logo">FaceSim</div>
      <nav>
        <ul>
          <li :class="{ active: currentPage === 'home' }">
            <a href="#" @click.prevent="currentPage = 'home'"
              >Face Comparison</a
            >
          </li>
          <li :class="{ active: currentPage === 'analyze-photo' }">
            <a href="#" @click.prevent="currentPage = 'analyze-photo'"
              >Analyze Photo</a
            >
          </li>
          <li :class="{ active: currentPage === 'about' }">
            <a href="#" @click.prevent="currentPage = 'about'">About Us</a>
          </li>
          <li :class="{ active: currentPage === 'contact' }">
            <a href="#" @click.prevent="currentPage = 'contact'">Contact</a>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="main">
      <header class="header">
        <h1>Face Similarity Checker</h1>
      </header>

      <section class="page-content">
        <!-- Home Page -->
        <div v-if="currentPage === 'home'" class="page home-page">
          <section class="card">
            <div class="upload-section">
              <label
                class="file-drop"
                @dragover.prevent
                @drop.prevent="onDrop($event, 1)"
              >
                <input
                  type="file"
                  ref="file1"
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
                @drop.prevent="onDrop($event, 2)"
              >
                <input
                  type="file"
                  ref="file2"
                  @change="uploadImage2"
                  accept="image/*"
                  hidden
                />
                <span v-if="!image2Url">Drop or click to upload Image 2</span>
                <img v-if="image2Url" :src="image2Url" alt="Preview 2" />
              </label>
            </div>
            <button
              class="btn-predict"
              @click="predictSimilarity"
              :disabled="!image1 || !image2 || isProcessing"
            >
              <span v-if="!isProcessing">Predict Similarity</span>
              <span v-else class="btn-loading">Processing...</span>
            </button>
            <div v-if="result !== null" class="result-box">
              Similarity: <strong>{{ result }}%</strong>
            </div>
            <div v-if="error" class="error-box">
              {{ error }}
            </div>
          </section>
        </div>

        <!-- About Page -->
        <div v-if="currentPage === 'about'" class="page about-page">
          <div class="card">
            <h2>About Us</h2>
            <p>
              Welcome to FaceSim! We are dedicated to providing state-of-the-art
              face similarity detection services. Our team leverages AI and
              machine learning to deliver accurate results in real-time.
            </p>
          </div>
        </div>

        <!-- Contact Page -->
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

        <!-- Analyze Photo Page -->
        <div
          v-if="currentPage === 'analyze-photo'"
          class="page analyze-photo-page"
        >
          <section class="card">
            <h2>Analyze Age, Gender, and Emotion</h2>
            <div class="upload-section">
              <h3>Upload Image for Analysis</h3>
              <input type="file" @change="handleFileChange" accept="image/*" />
              <div v-if="imagePreview">
                <h4>Preview Image:</h4>
                <img
                  :src="imagePreview"
                  alt="Image Preview"
                  class="preview-img"
                />
              </div>
            </div>

            <div>
              <button @click="submitAnalysis" :disabled="isLoading">
                Analyze Image
              </button>
            </div>

            <div v-if="analysisResults" class="result">
              <h3>Age: {{ analysisResults.age }}</h3>
              <h3>Gender: {{ analysisResults.gender }}</h3>
              <h3>Emotion: {{ analysisResults.emotion }}</h3>
            </div>

            <div v-if="isLoading" class="loading-overlay">
              <div class="spinner"></div>
              <p>Processing...</p>
            </div>

            <div v-if="errorMessage" class="error">
              <p>{{ errorMessage }}</p>
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
  name: "FaceComparison",
  data() {
    return {
      currentPage: "home",
      image1: null,
      image2: null,
      image1Url: null,
      image2Url: null,
      result: null,
      error: null,
      isProcessing: false,
      image: null,
      imagePreview: null,
      analysisResults: null,
      errorMessage: null,
      isLoading: false,
    };
  },
  methods: {
    onDrop(e, slot) {
      const file = e.dataTransfer.files[0];
      if (!file || !file.type.startsWith("image/")) return;
      if (slot === 1) {
        this.$refs.file1.files = e.dataTransfer.files;
        this.uploadImage1({ target: { files: e.dataTransfer.files } });
      } else {
        this.$refs.file2.files = e.dataTransfer.files;
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
      this.result = null;
      this.error = null;
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
      this.result = null;
      this.error = null;
    },

    async predictSimilarity() {
      if (!this.image1 || !this.image2) {
        this.error = "Please upload both images.";
        return;
      }
      this.isProcessing = true;
      this.error = null;
      this.result = null;

      try {
        const formData1 = new FormData();
        formData1.append("image1", this.image1);
        await axios.post("http://127.0.0.1:5000/upload_image1", formData1, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        const formData2 = new FormData();
        formData2.append("image2", this.image2);
        await axios.post("http://127.0.0.1:5000/upload_image2", formData2, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        const res = await axios.post("http://127.0.0.1:5000/compare_photos");
        this.result = parseFloat(res.data.similarity_percentage).toFixed(2);
      } catch (err) {
        if (err.response) {
          this.error =
            err.response.data?.error || `Error: ${err.response.status}`;
        } else if (err.request) {
          this.error =
            "No response from server. Check if the backend is running.";
        } else {
          this.error = `Error: ${err.message}`;
        }
      } finally {
        this.isProcessing = false;
      }
    },

    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.image = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    async submitAnalysis() {
      if (!this.image) {
        this.errorMessage = "Please upload an image for analysis.";
        return;
      }

      const formData = new FormData();
      formData.append("image1", this.image);

      this.isLoading = true;
      this.errorMessage = null;
      this.analysisResults = null;

      try {
        const uploadResponse = await axios.post(
          "http://127.0.0.1:5000/upload_image1",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );

        if (uploadResponse.data.error) {
          this.errorMessage = "There was an error uploading the image.";
          this.isLoading = false;
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/analyze_photo"
        );

        if (response.data.age !== undefined) {
          this.analysisResults = response.data;
        } else {
          this.errorMessage = "There was an error processing the image.";
        }
      } catch (error) {
        this.errorMessage = "An error occurred while making the API request.";
      } finally {
        this.isLoading = false;
      }
    },

    goBack() {
      this.$router.push("/"); // Navigate back to the dashboard (App.vue)
    },
  },
};
</script>

<style>
/* Global Resets & Box Sizing */
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

/* Global Color Palette */
:root {
  --blue-dark: #0a2540;
  --blue-primary: #596893;
  --blue-light: #cbd6f3;
  --bg: #f0f4ff;
  --text: #1f2937;
  --white: #ffffff;
}

/* Layout */
#app {
  display: flex;
  min-height: 100vh;
  font-family: "Roboto", sans-serif;
  background: var(--bg);
  color: var(--text);
  width: 100%;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--blue-dark);
  color: var(--white);
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}
.logo {
  font-size: 1.75rem;
  font-weight: bold;
  margin-bottom: 2rem;
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  width: 100%;
}
.sidebar nav li {
  margin: 1rem 0;
}
.sidebar nav a {
  color: var(--white);
  text-decoration: none;
  font-size: 1rem;
  display: block;
  padding: 0.5rem 0;
  transition: color 0.3s, transform 0.3s;
}
.sidebar nav li.active a,
.sidebar nav a:hover {
  color: var(--blue-light);
  transform: translateX(4px);
}

/* Main Content */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.header {
  background: var(--blue-primary);
  color: var(--white);
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.page-content {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 20px;
  margin-top: 0; /* Fix gap */
}

/* Card */
.card {
  background: var(--white);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 800px;
  transition: transform 0.3s;
}
.card:hover {
  transform: translateY(-6px);
}

/* Upload Section */
.upload-section {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.file-drop {
  flex: 1;
  min-width: 200px;
  border: 2px dashed var(--blue-primary);
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: background 0.3s, border-color 0.3s;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 200px;
}
.file-drop:hover {
  background: var(--blue-light);
  border-color: var(--blue-dark);
}
.file-drop span {
  color: var(--blue-dark);
  font-size: 1rem;
  margin-bottom: 0.5rem;
}
.file-drop img {
  max-width: 100%;
  max-height: 120px;
  display: block;
  margin: 0 auto;
  border-radius: 6px;
  object-fit: contain;
}

/* Button */
.btn-predict {
  width: 100%;
  background: var(--blue-dark);
  color: var(--white);
  border: none;
  padding: 1rem;
  font-size: 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}
.btn-predict:hover:not(:disabled) {
  background: var(--blue-primary);
  transform: scale(1.02);
}
.btn-predict:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-loading::after {
  content: "";
  display: inline-block;
  margin-left: 0.75rem;
  width: 18px;
  height: 18px;
  border: 2px solid var(--white);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* Result & Error */
.result-box {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--blue-light);
  border-left: 4px solid var(--blue-primary);
  border-radius: 4px;
  font-weight: bold;
  text-align: center;
}
.error-box {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #ffebee;
  color: #c62828;
  border-left: 4px solid #c62828;
  border-radius: 4px;
  text-align: center;
}

/* Footer */
.footer {
  color: var(--blue-dark);
  text-align: center;
  padding: 1rem;
  font-size: 0.9rem;
  background-color: var(--blue-light);
  border-top: 1px solid var(--blue-primary);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsiveness */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: static;
    box-shadow: none;
    padding: 1rem;
  }
  .sidebar nav ul {
    display: flex;
    justify-content: space-around;
  }
  .sidebar nav li {
    margin: 0 0.5rem;
  }
  .logo {
    text-align: center;
    margin-bottom: 1rem;
  }
  #app {
    flex-direction: column;
  }
  .page-content {
    padding: 1rem;
  }
  .card {
    width: 95%;
    margin-top: 1rem;
  }
  .upload-section {
    flex-direction: column;
    gap: 1rem;
  }
  .file-drop {
    min-width: unset;
    width: 100%;
  }
}
</style>

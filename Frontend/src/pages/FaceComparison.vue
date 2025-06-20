<template>
  <div class="container">
    <div class="tool-card">
      <header class="tool-header">
        <h1>Face AI Suite</h1>
        <p>Analyze & Compare Faces with Modern Technology</p>
        <div class="tab-switcher">
          <button
            :class="{ active: activeTab === 'compare' }"
            @click="setActiveTab('compare')"
          >
            Compare Faces
          </button>
          <button
            :class="{ active: activeTab === 'analyze' }"
            @click="setActiveTab('analyze')"
          >
            Analyze Photo
          </button>
        </div>
      </header>

      <div class="content-wrapper">
        <div class="canvas-column">
          <div v-if="activeTab === 'compare'" class="compare-canvas">
            <div class="preview-pane">
              <img v-if="image1Url" :src="image1Url" alt="Image 1 Preview" />
              <div v-else class="placeholder-text"><span>Image 1</span></div>
            </div>
            <div class="preview-pane">
              <img v-if="image2Url" :src="image2Url" alt="Image 2 Preview" />
              <div v-else class="placeholder-text"><span>Image 2</span></div>
            </div>
          </div>
          <div v-if="activeTab === 'analyze'" class="analyze-canvas">
            <div class="preview-pane single">
              <img
                v-if="analysisImageUrl"
                :src="analysisImageUrl"
                alt="Analysis Preview"
              />
              <div v-else class="placeholder-text">
                <span>Image to Analyze</span>
              </div>
            </div>
          </div>
        </div>

        <div class="controls-column">
          <div v-if="activeTab === 'compare'">
            <div class="control-group">
              <label>Image 1</label>
              <div class="button-group">
                <button
                  class="upload-button"
                  @click="triggerFileUpload('fileInput1')"
                >
                  Upload Photo
                </button>
                <button
                  v-if="image1Url"
                  class="clear-button"
                  @click="clearImage('image1')"
                >
                  Clear
                </button>
              </div>
            </div>
            <div class="control-group">
              <label>Image 2</label>
              <div class="button-group">
                <button
                  class="upload-button"
                  @click="triggerFileUpload('fileInput2')"
                >
                  Upload Photo
                </button>
                <button
                  v-if="image2Url"
                  class="clear-button"
                  @click="clearImage('image2')"
                >
                  Clear
                </button>
              </div>
            </div>

            <div class="control-group">
              <label for="model-select">Select Model</label>
              <select
                id="model-select"
                v-model="selectedModel"
                class="model-select"
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
            <div class="control-group">
              <label for="detector-select">Select Face Detector</label>
              <select
                id="detector-select"
                v-model="selectedDetector"
                class="model-select"
              >
                <option v-for="d in availableDetectors" :key="d" :value="d">
                  {{ d }}
                </option>
              </select>
            </div>
            <div class="control-group">
              <label for="metric-select">Select Distance Metric</label>
              <select
                id="metric-select"
                v-model="selectedMetric"
                class="model-select"
              >
                <option v-for="m in availableMetrics" :key="m" :value="m">
                  {{ m }}
                </option>
              </select>
            </div>

            <button
              @click="compareFaces"
              :disabled="!image1 || !image2 || isLoading"
              class="action-button primary"
            >
              <span v-if="isLoading">Processing...</span>
              <span v-else>Compare Faces</span>
            </button>
          </div>

          <div v-if="activeTab === 'analyze'">
            <div class="control-group">
              <label>Analysis Image</label>
              <div class="button-group">
                <button
                  class="upload-button"
                  @click="triggerFileUpload('fileInputAnalysis')"
                >
                  Upload Photo
                </button>
                <button
                  v-if="analysisImageUrl"
                  class="clear-button"
                  @click="clearImage('analysis')"
                >
                  Clear
                </button>
              </div>
            </div>
            <button
              @click="analyzePhoto"
              :disabled="!analysisImage || isLoading"
              class="action-button primary"
            >
              <span v-if="isLoading">Processing...</span>
              <span v-else>Analyze Photo</span>
            </button>
          </div>

          <div class="result-wrapper">
            <div v-if="isLoading" class="skeleton-wrapper">
              <div class="skeleton-box">
                <div class="skeleton-line title"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line short"></div>
              </div>
            </div>

            <transition name="result-fade">
              <div
                v-if="comparisonResult && !isLoading"
                class="result-box success"
              >
                <h3>Comparison Result</h3>
                <p>
                  <strong>Similarity:</strong>
                  {{ comparisonResult.similarity_percentage.toFixed(2) }}%
                </p>
                <p>
                  <strong>Verified:</strong>
                  {{ comparisonResult.verified ? "Yes" : "No" }}
                </p>
              </div>
            </transition>

            <transition name="result-fade">
              <div
                v-if="analysisResult && !isLoading"
                class="result-box success"
              >
                <h3>Analysis Result</h3>
                <p><strong>Estimated Age:</strong> {{ analysisResult.age }}</p>
                <p><strong>Gender:</strong> {{ analysisResult.gender }}</p>
                <p><strong>Emotion:</strong> {{ analysisResult.emotion }}</p>
              </div>
            </transition>

            <transition name="result-fade">
              <div v-if="error && !isLoading" class="result-box error">
                <p>{{ error }}</p>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <input
        type="file"
        ref="fileInput1"
        @change="handleFileUpload($event, 'image1')"
        accept="image/*"
        hidden
      />
      <input
        type="file"
        ref="fileInput2"
        @change="handleFileUpload($event, 'image2')"
        accept="image/*"
        hidden
      />
      <input
        type="file"
        ref="fileInputAnalysis"
        @change="handleFileUpload($event, 'analysis')"
        accept="image/*"
        hidden
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ModernFaceTools",
  data() {
    return {
      activeTab: "compare",
      image1: null,
      image2: null,
      analysisImage: null,
      image1Url: null,
      image2Url: null,
      analysisImageUrl: null,
      comparisonResult: null,
      analysisResult: null,
      isLoading: false,
      error: null,
      selectedModel: "VGG-Face",
      availableModels: [
        { value: "VGG-Face", text: "VGG-Face" },
        { value: "Facenet", text: "Facenet" },
        { value: "Facenet512", text: "Facenet512" },
        { value: "OpenFace", text: "OpenFace" },
        { value: "DeepFace", text: "DeepFace" },
        { value: "ArcFace", text: "ArcFace" },
        { value: "Dlib", text: "Dlib" },
      ],
      selectedDetector: "opencv",
      availableDetectors: ["opencv", "ssd", "mtcnn", "dlib", "retinaface"],
      selectedMetric: "cosine",
      availableMetrics: ["cosine", "euclidean", "euclidean_l2"],
    };
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
      this.clearImage("image1");
      this.clearImage("image2");
      this.clearImage("analysis");
    },
    triggerFileUpload(refName) {
      this.$refs[refName].click();
    },
    handleFileUpload(event, target) {
      const file = event.target.files[0];
      if (!file) return;

      const url = URL.createObjectURL(file);
      if (target === "image1") {
        this.image1 = file;
        this.image1Url = url;
      } else if (target === "image2") {
        this.image2 = file;
        this.image2Url = url;
      } else if (target === "analysis") {
        this.analysisImage = file;
        this.analysisImageUrl = url;
      }
      event.target.value = "";
    },
    clearImage(target) {
      if (target === "image1") {
        this.image1 = null;
        this.image1Url = null;
      }
      if (target === "image2") {
        this.image2 = null;
        this.image2Url = null;
      }
      if (target === "analysis") {
        this.analysisImage = null;
        this.analysisImageUrl = null;
      }
      this.comparisonResult = null;
      this.analysisResult = null;
      this.error = null;
    },
    async compareFaces() {
      this.isLoading = true;
      this.error = null;
      this.comparisonResult = null;

      const formData = new FormData();
      formData.append("image1", this.image1);
      formData.append("image2", this.image2);
      formData.append("model_name", this.selectedModel);
      formData.append("detector_backend", this.selectedDetector);
      formData.append("distance_metric", this.selectedMetric);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/compare",
          formData
        );
        this.comparisonResult = response.data;
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          "An error occurred while contacting the server.";
      } finally {
        this.isLoading = false;
      }
    },
    async analyzePhoto() {
      this.isLoading = true;
      this.error = null;
      this.analysisResult = null;

      const formData = new FormData();
      formData.append("image", this.analysisImage);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/analyze",
          formData
        );
        this.analysisResult = response.data;
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          "An error occurred while contacting the server.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

.container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background-color: #f4f7f9;
  font-family: "Inter", sans-serif;
  padding: 3rem;
}

.tool-card {
  width: 100%;
  max-width: 960px;
  background-color: #ffffff;
  border-radius: 1.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.tool-header {
  text-align: center;
  padding: 2rem;
  border-bottom: 1px solid #e5e7eb;
}
.tool-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}
.tool-header p {
  color: #6b7280;
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
}

.tab-switcher {
  display: inline-flex;
  background-color: #f4f7f9;
  border-radius: 0.75rem;
  padding: 0.5rem;
}
.tab-switcher button {
  background: none;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 0.5rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}
.tab-switcher button.active {
  background-color: #3b82f6;
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.content-wrapper {
  display: flex;
  flex-wrap: wrap; /* Memungkinkan wrap di layar kecil */
  padding: 2rem;
  gap: 2rem;
}

.canvas-column {
  flex: 2;
  min-width: 300px; /* Lebar minimum untuk kanvas */
  background-color: #f9fafb;
  border-radius: 1rem;
  padding: 1rem;
}

.controls-column {
  flex: 1;
  min-width: 280px; /* Lebar minimum untuk kontrol */
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.compare-canvas {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.analyze-canvas {
  display: flex;
  justify-content: center;
  align-items: center;
}
.preview-pane {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background-color: #e5e7eb;
  border-radius: 0.75rem;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}
.preview-pane.single {
  max-width: 350px;
}
.preview-pane img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.placeholder-text {
  color: #9ca3af;
  font-weight: 500;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.control-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}
.button-group {
  display: flex;
  gap: 0.5rem;
}
.upload-button {
  flex-grow: 1;
  background-color: #ffffff;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.upload-button:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}
.clear-button {
  background-color: #fee2e2;
  color: #b91c1c;
  border: none;
  border-radius: 0.5rem;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}
.clear-button:hover {
  background-color: #fca5a5;
}

.model-select,
.action-button.primary {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
}
.model-select {
  border: 1px solid #d1d5db;
}
.action-button.primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  cursor: pointer;
}
.action-button.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.result-wrapper {
  margin-top: 1.5rem;
  min-height: 120px;
}

.result-box {
  padding: 1rem;
  border-radius: 0.75rem;
  font-size: 0.9rem;
}
.result-box p {
  margin: 0.5rem 0;
}
.result-box.success {
  background-color: #f0fdf4;
  color: #166534;
}
.result-box.error {
  background-color: #fef2f2;
  color: #991b1b;
}

/* === CSS UNTUK LOADING SKELETON & TRANSISI === */
@keyframes pulse-bg {
  0% {
    background-color: #f0f0f0;
  }
  50% {
    background-color: #e0e0e0;
  }
  100% {
    background-color: #f0f0f0;
  }
}

.skeleton-box {
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: #ffffff;
}
.skeleton-line {
  height: 1rem;
  width: 100%;
  background-color: #f0f0f0;
  border-radius: 0.25rem;
  margin: 1rem 0;
  animation: pulse-bg 1.5s infinite ease-in-out;
}
.skeleton-line.title {
  width: 40%;
  height: 1.25rem;
  margin-bottom: 1.5rem;
}
.skeleton-line.short {
  width: 60%;
}

.result-fade-enter-active,
.result-fade-leave-active {
  transition: opacity 0.5s ease;
}
.result-fade-enter-from,
.result-fade-leave-to {
  opacity: 0;
}
/* =============================================== */

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
}
</style>

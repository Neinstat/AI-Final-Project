<template>
  <div>
    <h2>Face Comparison</h2>

    <!-- Image Upload Section for Photo Comparison -->
    <div>
      <h3>Upload Image 1 for Comparison</h3>
      <input
        type="file"
        @change="handleFileChange(1, 'image1')"
        accept="image/*"
      />
      <div v-if="image1Preview">
        <h4>Preview Image 1:</h4>
        <img :src="image1Preview" alt="Image 1 Preview" class="preview-img" />
      </div>
    </div>

    <div>
      <h3>Upload Image 2 for Comparison</h3>
      <input
        type="file"
        @change="handleFileChange(2, 'image2')"
        accept="image/*"
      />
      <div v-if="image2Preview">
        <h4>Preview Image 2:</h4>
        <img :src="image2Preview" alt="Image 2 Preview" class="preview-img" />
      </div>
    </div>

    <!-- Model Selection -->
    <div>
      <h4>Select Model for Comparison:</h4>
      <select v-model="selectedModel">
        <option value="DeepFace">DeepFace</option>
        <option value="VGG-Face">VGG-Face</option>
        <option value="Facenet">Facenet</option>
        <option value="OpenFace">OpenFace</option>
        <option value="Dlib">Dlib</option>
      </select>
    </div>

    <!-- Submit for Comparison -->
    <div>
      <button @click="submitComparison" :disabled="isLoading">
        Submit for Comparison
      </button>
    </div>

    <!-- Similarity Result -->
    <div v-if="similarityPercentage !== null">
      <h4>Similarity Percentage: {{ similarityPercentage }}%</h4>
    </div>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Processing...</p>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error">
      <p>{{ errorMessage }}</p>
    </div>

    <!-- Back Button -->
    <div>
      <button @click="goBack">Back to Dashboard</button>
    </div>
  </div>
</template>

<script>
// Make sure to import axios if necessary
import axios from "axios";

export default {
  data() {
    return {
      image1: null,
      image2: null,
      selectedModel: "DeepFace",
      similarityPercentage: null,
      errorMessage: null,
      isLoading: false,
      image1Preview: null,
      image2Preview: null,
    };
  },
  methods: {
    handleFileChange(imageNumber, type) {
      const file = event.target.files[0];
      if (imageNumber === 1 && type === "image1") {
        this.image1 = file;
        this.createImagePreview(file, "image1Preview");
      } else if (imageNumber === 2 && type === "image2") {
        this.image2 = file;
        this.createImagePreview(file, "image2Preview");
      }
    },

    createImagePreview(file, previewKey) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this[previewKey] = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    async submitComparison() {
      if (!this.image1 || !this.image2) {
        this.errorMessage = "Please upload both images.";
        return;
      }

      const formData = new FormData();
      formData.append("image1", this.image1);
      formData.append("image2", this.image2);

      this.isLoading = true;
      this.errorMessage = null;
      this.similarityPercentage = null;

      try {
        const uploadResponse1 = await axios.post(
          "http://127.0.0.1:5000/upload_image1",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        const uploadResponse2 = await axios.post(
          "http://127.0.0.1:5000/upload_image2",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );

        if (uploadResponse1.data.error || uploadResponse2.data.error) {
          this.errorMessage = "There was an error uploading the images.";
          this.isLoading = false;
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/compare_photos",
          {
            model: this.selectedModel,
          }
        );

        if (response.data.similarity_percentage !== undefined) {
          this.similarityPercentage =
            response.data.similarity_percentage.toFixed(2);
        } else {
          this.errorMessage = "There was an error processing the images.";
        }
      } catch (error) {
        console.error(error);
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
/* Add styles for face comparison page */
.upload-section {
  margin-bottom: 20px;
}

.preview-img {
  max-width: 100%;
  max-height: 300px;
}

button {
  padding: 10px;
  font-size: 1rem;
  cursor: pointer;
}

button:disabled {
  background-color: #d3d3d3;
  cursor: not-allowed;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner {
  border: 8px solid #f3f3f3;
  border-top: 8px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error {
  color: red;
  font-size: 1.2rem;
}
</style>

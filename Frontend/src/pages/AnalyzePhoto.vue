<template>
  <div>
    <h2>Analyze Age, Gender, and Emotion</h2>

    <!-- Image Upload Section for Analysis -->
    <div>
      <h3>Upload Image for Analysis</h3>
      <input type="file" @change="handleFileChange" accept="image/*" />
      <div v-if="imagePreview">
        <h4>Preview Image:</h4>
        <img :src="imagePreview" alt="Image Preview" class="preview-img" />
      </div>
    </div>

    <!-- Submit for Analysis -->
    <div>
      <button @click="submitAnalysis" :disabled="isLoading">
        Analyze Image
      </button>
    </div>

    <!-- Analysis Result -->
    <div v-if="analysisResults" class="result">
      <h3>Age: {{ analysisResults.age }}</h3>
      <h3>Gender: {{ analysisResults.gender }}</h3>
      <h3>Emotion: {{ analysisResults.emotion }}</h3>
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
import axios from "axios";
export default {
  data() {
    return {
      image: null,
      imagePreview: null,
      analysisResults: null,
      errorMessage: null,
      isLoading: false,
    };
  },
  methods: {
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
/* Add styles for age, gender, and emotion analysis page */
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

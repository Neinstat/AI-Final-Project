<template>
  <div id="app">
    <h1>Face Similarity Checker</h1>
    <div class="container">
      <div class="form-container">
        <!-- Form untuk upload image 1 tanpa tombol load -->
        <input type="file" ref="file1" @change="uploadImage1" required />

        <!-- Form untuk upload image 2 tanpa tombol load -->
        <input type="file" ref="file2" @change="uploadImage2" required />

        <button @click="predictSimilarity" :disabled="isProcessing">
          Predict Similarity
        </button>
      </div>

      <!-- Indikator loading -->
      <div v-if="isProcessing" class="loading">
        <p>Processing... Please wait</p>
        <div class="spinner"></div>
      </div>

      <!-- Tampilkan gambar setelah di-upload -->
      <div v-if="image1Url && image2Url">
        <h3>Uploaded Images</h3>
        <div>
          <img :src="image1Url" alt="Image 1" class="uploaded-image" />
          <img :src="image2Url" alt="Image 2" class="uploaded-image" />
        </div>
      </div>

      <!-- Hasil Prediksi -->
      <div v-if="result !== null">
        <h3>Similarity Result: {{ result }}%</h3>
      </div>
      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      image1: null,
      image2: null,
      result: null,
      error: null,
      isProcessing: false, // Menandakan apakah sedang ada proses
      image1Url: null, // Menyimpan URL gambar 1
      image2Url: null, // Menyimpan URL gambar 2
    };
  },
  methods: {
    uploadImage1(event) {
      this.image1 = event.target.files[0]; // Menyimpan file yang dipilih untuk gambar 1
      this.image1Url = URL.createObjectURL(this.image1); // Menyimpan URL untuk ditampilkan

      // Mengupload gambar secara langsung setelah dipilih
      this.isProcessing = true; // Set isProcessing menjadi true untuk menampilkan spinner
      const formData = new FormData();
      formData.append("image1", this.image1); // Menambahkan file ke FormData

      axios
        .post("http://127.0.0.1:5000/upload_image1", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("Image 1 uploaded successfully", response.data);
          this.error = null;
          this.isProcessing = false;
        })
        .catch((error) => {
          console.error("Error uploading image:", error.response.data);
          this.error = error.response.data.error || "Error uploading Image 1";
          this.isProcessing = false;
        });
    },
    uploadImage2(event) {
      this.image2 = event.target.files[0]; // Menyimpan file yang dipilih untuk gambar 2
      this.image2Url = URL.createObjectURL(this.image2); // Menyimpan URL untuk ditampilkan

      // Mengupload gambar secara langsung setelah dipilih
      this.isProcessing = true;
      const formData = new FormData();
      formData.append("image2", this.image2); // Menambahkan file ke FormData

      axios
        .post("http://127.0.0.1:5000/upload_image2", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("Image 2 uploaded successfully", response.data);
          this.error = null;
          this.isProcessing = false;
        })
        .catch((error) => {
          console.error("Error uploading image:", error.response.data);
          this.error = error.response.data.error || "Error uploading Image 2";
          this.isProcessing = false;
        });
    },
    predictSimilarity() {
      this.isProcessing = true; // Menandakan proses sedang berjalan
      axios
        .post("http://127.0.0.1:5000/predict")
        .then((response) => {
          this.result = response.data.similarity_percentage; // Menyimpan hasil persentase kemiripan
          this.error = null;
          this.isProcessing = false; // Menyelesaikan proses dan sembunyikan spinner
        })
        .catch((error) => {
          console.error("Error during prediction!", error);
          this.error = "Error during similarity prediction";
          this.isProcessing = false; // Menyelesaikan proses jika terjadi error
        });
    },
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  font-family: Arial, sans-serif;
}

.container {
  margin-top: 20px;
}

.form-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

input[type="file"] {
  margin: 10px;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  margin-top: 20px;
}

.loading {
  text-align: center;
  margin-top: 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
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

.uploaded-image {
  width: 200px;
  height: auto;
  margin: 10px;
}
</style>

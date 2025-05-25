<template>
  <div id="dashboard">
    <div class="header">
      <h1>Face Similarity and Analysis Dashboard</h1>
    </div>

    <div class="main-content">
      <!-- Dashboard Navigation Buttons -->
      <div class="button-container">
        <button @click="goToFaceComparison">Go to Face Comparison</button>
        <button @click="goToAnalyzePhoto">
          Go to Age, Gender, and Emotion Analysis
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardPage",
  methods: {
    // Method to navigate to the Face Comparison page
    goToFaceComparison() {
      this.$router.push("/face-comparison");
    },
    // Method to navigate to the Age, Gender, and Emotion Analysis page
    goToAnalyzePhoto() {
      this.$router.push("/analyze-photo");
    },
  },
};
</script>

<style>
#dashboard {
  font-family: Arial, sans-serif;
  padding: 20px;
  text-align: center;
}

.header {
  background-color: #4caf50;
  color: white;
  padding: 10px;
  border-radius: 5px;
}

.main-content {
  margin-top: 20px;
}

.button-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

button {
  padding: 15px;
  font-size: 1.2rem;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  border: none;
  margin: 10px;
  border-radius: 5px;
  width: 250px;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}
</style>

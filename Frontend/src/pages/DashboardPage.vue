<template>
  <div id="dashboard">
    <div class="content-wrapper">
      <div class="header">
        <h1>Face Similarity and Analysis Dashboard</h1>
      </div>

      <div class="main-content">
        <!-- Dashboard Navigation Buttons -->
        <div class="button-container">
          <button @click="goToFaceComparison">Try Now!</button>
        </div>
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
  },
};
</script>

<style>
#dashboard {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
  max-width: 100%;
  width: 100%;
}

.header {
  background-color: #4caf50;
  color: white;
  padding: 20px;
  border-radius: 10px;
  font-size: 2rem;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
}

.main-content {
  margin-top: 20px;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

button {
  padding: 15px 30px;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  border-radius: 10px;
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .header {
    font-size: 1.5rem;
  }

  button {
    padding: 10px 20px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .header {
    font-size: 1.2rem;
  }

  button {
    padding: 8px 16px;
    font-size: 0.9rem;
  }
}
</style>

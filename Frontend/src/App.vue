<template>
  <div id="app">
    <!-- This is where the child components will be rendered -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Global Styles */
#app {
  font-family: Arial, sans-serif;
  padding: 20px;
}
</style>

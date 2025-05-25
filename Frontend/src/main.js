import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Make sure Vue Router is used

createApp(App).use(router).mount("#app"); // Mount the app with Vue Router

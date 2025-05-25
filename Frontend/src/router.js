import { createRouter, createWebHistory } from "vue-router";
import DashboardPage from "./pages/DashboardPage.vue"; // Updated name
import FaceComparison from "./pages/FaceComparison.vue";
import AnalyzePhoto from "./pages/AnalyzePhoto.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: DashboardPage }, // Default route points to the Dashboard
    { path: "/face-comparison", component: FaceComparison },
    { path: "/analyze-photo", component: AnalyzePhoto },
  ],
});

export default router;

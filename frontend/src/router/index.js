import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import History from "../views/History.vue";
import BucketDetail from "../views/BucketDetail.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/history",
    name: "History",
    component: History
  },
  {
  path: "/bucket/:id",
  name: "bucket-detail",
  component: BucketDetail
}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import History from "../views/History.vue";
import BucketDetail from "../views/BucketDetail.vue"
import login from "../views/auth/login.vue"

const routes = [

  {
  path: "/login",
  name: "Login",
  component: login,
  meta: { requiresAuth: false }
},
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: "/history",
    name: "History",
    component: History,
    meta: { requiresAuth: true }
  },
  {
  path: "/bucket/:id",
  name: "bucket-detail",
  component: BucketDetail,
  meta: { requiresAuth: true }
},
{
  path: "/:pathMatch(.*)*",
  redirect: "/"
}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem("token")
  const isAuthenticated = Boolean(token)

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login")
    return
  }

  if (to.path === "/login" && isAuthenticated) {
    next("/")
    return
  }

  next()
})

export default router;

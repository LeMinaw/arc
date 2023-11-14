import { createRouter, createWebHistory } from "vue-router"

import About from "./views/About.vue"
import Index from "./views/Index.vue"
import Error from "./views/Error.vue"
import Products from "./views/Products.vue"

const routes = [
  { path: "/", component: Index, name: "index" },
  { path: "/produits", component: Products, name: "products" },
  { path: "/a-propos", component: About, name: "about" },
  {
    path: "/:pathMatch(.*)",
    component: Error,
    props: { message: "Page introuvable." },
    name: "not-found",
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

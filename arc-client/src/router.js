import { createRouter, createWebHistory } from "vue-router"

import About from "./views/About.vue"
import CheckItem from "./views/CheckItem.vue"
import Error from "./views/Error.vue"
import Index from "./views/Index.vue"
import Product from "./views/Product.vue"
import Products from "./views/Products.vue"

const routes = [
  { path: "/", component: Index, name: "index" },
  { path: "/catalogue/:categories*", component: Products, name: "products" },
  { path: "/produit/:id(\\d+)", component: Product, name: "product" },
  { path: "/verification", component: CheckItem, name: "check" },
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

<script setup>
  import BaseLayout from "./layouts/BaseLayout.vue"
  import Footer from "./components/Footer.vue"
  import Navbar from "./components/Navbar.vue"
</script>

<template>
  <BaseLayout>
    <header>
      <Navbar />
    </header>

    <main class="flex-grow">
      <router-view />
    </main>

    <footer>
      <Footer />
    </footer>
  </BaseLayout>
</template>

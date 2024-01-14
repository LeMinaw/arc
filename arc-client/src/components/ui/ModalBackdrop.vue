<script setup>
  import { onMounted, onUnmounted } from "vue"

  const style = document.documentElement.style

  onMounted(() => (style.overflow = "hidden"))
  onUnmounted(() => (style.overflow = "unset"))
</script>

<template>
  <div
    class="fixed top-0 right-0 bottom-0 left-0 flex flex-col justify-center items-center backdrop-blur"
  >
    <slot />
  </div>
</template>

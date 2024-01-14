<script setup>
  import ModalBackdrop from "./ModalBackdrop.vue"
</script>

<template>
  <ModalBackdrop>
    <div class="m-4 bg-zinc-200 shadow-xl">
      <h3 class="px-4 py-2 font-bold text-lg bg-orange-400">
        <slot name="title">Information</slot>
      </h3>
      <div class="px-4 py-2">
        <slot />
      </div>
    </div>
  </ModalBackdrop>
</template>

<script setup>
  import { computed } from "vue"
  import {
    InformationCircleIcon,
    CheckCircleIcon,
    ExclamationCircleIcon,
    ExclamationTriangleIcon,
  } from "@heroicons/vue/24/outline"

  const props = defineProps({
    class: { default: "" },
  })

  const icons = {
    // Root element class name: icon component
    "alert-info": InformationCircleIcon,
    "alert-success": CheckCircleIcon,
    "alert-warning": ExclamationCircleIcon,
    "alert-error": ExclamationTriangleIcon,
  }

  const icon = computed(() => {
    for (const [className, icon] of Object.entries(icons)) {
      if (props.class.includes(className)) return icon
    }
  })
</script>

<template>
  <div class="alert m-6">
    <div class="flex w-full items-center gap-2 text-lg">
      <icon class="w-8" v-if="icon" />

      <slot></slot>
    </div>
  </div>
</template>

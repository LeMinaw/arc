<script setup>
  import { watchEffect, inject, ref, computed } from "vue"

  const products = inject("products")

  const props = defineProps({
    property: {
      type: String,
      required: true,
    },
    unit: {
      type: String,
      default: "",
      required: false,
    },
  })

  const filter = defineModel()

  const min = ref(null)
  const max = ref(null)

  const range = computed(() => {
    const values = products.value.map(product => product.specs[props.property])

    return [Math.min(...values), Math.max(...values)]
  })

  watchEffect(() => {
    filter.value = product =>
      (typeof min.value !== "number" || product.specs[props.property] >= min.value) &&
      (typeof max.value !== "number" || product.specs[props.property] <= max.value)
  })
</script>

<template>
  De
  <input v-model="min" type="number" :min="range[0]" :max="range[1]" class="w-16" />
  à
  <input v-model="max" type="number" :min="range[0]" :max="range[1]" class="w-16" />
  {{ unit }}
</template>

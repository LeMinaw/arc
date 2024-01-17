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

  const value = ref(null)

  const getRange = product => product.specs[props.property].toSorted()

  const range = computed(() => [
    Math.min(...products.value.map(product => getRange(product)[0])),
    Math.max(...products.value.map(product => getRange(product)[1])),
  ])

  watchEffect(() => {
    filter.value = product => {
      if (typeof value.value === "number") {
        const [min, max] = getRange(product)
        return value.value >= min && value.value <= max
      }

      return true
    }
  })
</script>

<template>
  <input v-model="value" type="number" :min="range[0]" :max="range[1]" />
  {{ unit }}
</template>

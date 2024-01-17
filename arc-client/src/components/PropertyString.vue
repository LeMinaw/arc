<script setup>
  import { watchEffect, ref } from "vue"

  import { normalize } from "../business/utils"

  const props = defineProps({
    property: {
      type: String,
      required: true,
    },
  })

  const filter = defineModel()

  const value = ref(null)

  watchEffect(() => {
    filter.value = product =>
      value.value
        ? normalize(product.specs[props.property]).includes(normalize(value.value))
        : true
  })
</script>

<template>
  <input v-model="value" class="w-16" />
</template>

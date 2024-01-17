<script setup>
  import { ref, watchEffect } from "vue"

  import Listbox from "./ui/listbox/Listbox.vue"
  import ListboxButton from "./ui/listbox/ListboxButton.vue"
  import ListboxOption from "./ui/listbox/ListboxOption.vue"
  import ListboxOptions from "./ui/listbox/ListboxOptions.vue"

  const props = defineProps({
    property: {
      type: String,
      required: true,
    },
    values: {
      type: Array,
      default: [],
    },
    unit: {
      type: String,
      default: "",
      required: false,
    },
  })

  const filter = defineModel()

  const selectedValues = ref([])

  watchEffect(() => {
    filter.value = product =>
      selectedValues.value.length
        ? selectedValues.value.includes(product.specs[props.property])
        : true
  })
</script>

<template>
  <Listbox v-model="selectedValues" multiple>
    <ListboxButton>
      {{ selectedValues.map(v => (v === null ? "Aucun·e" : v)).join(", ") || "Tous" }}
    </ListboxButton>

    <ListboxOptions>
      <ListboxOption v-for="value in values" :value="value">
        {{ value === null ? "Aucun·e" : `${value} ${unit}` }}
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>

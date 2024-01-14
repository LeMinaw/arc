<script setup>
  import { ref } from "vue"
  import {
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
  } from "@headlessui/vue"
  import { ChevronDownIcon } from "@heroicons/vue/24/outline"

  defineProps({
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

  // const modelValue = defineModel()
  const selectedValues = ref([])
</script>

<template>
  <Listbox v-model="selectedValues" multiple>
    <ListboxButton>
      {{ selectedValues.join(", ") || "Tous" }}
      <ChevronDownIcon class="inline h-6" />
    </ListboxButton>

    <ListboxOptions>
      <ListboxOption v-for="value in values" :value="value">
        {{ value }} {{ unit }}
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>

<script setup>
  import { ref, computed, watchEffect } from "vue"
  import {
    CheckCircleIcon,
    XCircleIcon,
    QuestionMarkCircleIcon,
  } from "@heroicons/vue/24/outline"

  import Listbox from "./ui/listbox/Listbox.vue"
  import ListboxButton from "./ui/listbox/ListboxButton.vue"
  import ListboxOption from "./ui/listbox/ListboxOption.vue"
  import ListboxOptions from "./ui/listbox/ListboxOptions.vue"

  const STATES = [
    { value: null, name: "Tous", icon: QuestionMarkCircleIcon },
    { value: false, name: "Non", icon: XCircleIcon },
    { value: true, name: "Oui", icon: CheckCircleIcon },
  ]

  const props = defineProps({
    property: {
      type: String,
      required: true,
    },
  })

  const filter = defineModel()

  const selectedValue = ref(null)

  const selectedState = computed(() =>
    STATES.find(state => state.value === selectedValue.value)
  )

  watchEffect(() => {
    filter.value = product =>
      selectedValue.value !== null
        ? product.specs[props.property] === selectedValue.value
        : true
  })
</script>

<template>
  <Listbox v-model="selectedValue">
    <ListboxButton>
      <component :is="selectedState.icon" class="w-5 mr-1" />

      {{ selectedState.name }}
    </ListboxButton>

    <ListboxOptions>
      <ListboxOption v-for="state in STATES" :value="state.value">
        <component :is="state.icon" class="w-5 mr-1" />
        {{ state.name }}
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>

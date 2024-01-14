<script setup>
  import { ref, computed } from "vue"
  import {
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
  } from "@headlessui/vue"
  import {
    CheckCircleIcon,
    NoSymbolIcon,
    RectangleGroupIcon,
  } from "@heroicons/vue/24/outline"

  const STATES = [
    { value: null, name: "Tous", icon: RectangleGroupIcon },
    { value: false, name: "Non", icon: NoSymbolIcon },
    { value: true, name: "Oui", icon: CheckCircleIcon },
  ]

  const value = ref(null)

  const selectedState = computed(() =>
    STATES.find(state => state.value === value.value)
  )
</script>

<template>
  <Listbox v-model="value">
    <ListboxButton>
      <component :is="selectedState.icon" class="inline h-6" />
      {{ selectedState.name }}
    </ListboxButton>

    <ListboxOptions>
      <ListboxOption v-for="state in STATES" :value="state.value">
        <component :is="state.icon" class="inline h-6" />
        {{ state.name }}
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>

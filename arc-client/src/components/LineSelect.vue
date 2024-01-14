<script setup>
  import { computed, ref, watch } from "vue"

  import {
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
  } from "@headlessui/vue"
  import { ChevronDownIcon } from "@heroicons/vue/24/outline"

  const props = defineProps({
    lines: {
      type: Array,
      default: [],
    },
  })

  const selected = defineModel()

  const selectedLines = ref([])
  const selectedManufacturers = ref([])

  const manufacturers = computed(() => [
    ...new Set(props.lines.map(line => line.manufacturer)),
  ])

  const selectedManufacturersLines = computed(() =>
    props.lines.filter(line => selectedManufacturers.value.includes(line.manufacturer))
  )

  watch(
    [selectedLines, selectedManufacturersLines],
    ([selectedLines, selectedManufacturersLines]) => {
      selected.value.length = 0
      if (selectedLines.length) {
        selected.value.push(...selectedLines)
      } else {
        selected.value.push(...selectedManufacturersLines)
      }
    }
  )

  watch(selectedManufacturersLines, selectedManufacturersLines => {
    selectedLines.value = selectedLines.value.filter(line =>
      selectedManufacturersLines.includes(line)
    )
  })

  const isDisabled = line => {
    selectedManufacturers.value.length
      ? !selectedManufacturersLines.value.includes(line.manufacturer)
      : false
  }
</script>

<template>
  Fabriquant
  <Listbox v-model="selectedManufacturers" multiple>
    <ListboxButton>
      {{ selectedManufacturers.map(m => m.name).join(", ") || "Tous" }}
      <ChevronDownIcon class="inline h-6" />
    </ListboxButton>

    <ListboxOptions>
      <ListboxOption v-for="manufacturer in manufacturers" :value="manufacturer">
        {{ manufacturer.name }}
      </ListboxOption>
    </ListboxOptions>
  </Listbox>

  Gamme

  <Listbox v-model="selectedLines" multiple>
    <ListboxButton>
      {{ selectedLines.map(m => m.name).join(", ") || "Toutes" }}
      <ChevronDownIcon class="inline h-6" />
    </ListboxButton>

    <ListboxOptions>
      <ListboxOption
        v-for="line in lines"
        :value="line"
        :disabled="isDisabled(line)"
        class="ui-disabled:text-red-500"
      >
        {{ line.manufacturer.name }} - {{ line.name }}
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>

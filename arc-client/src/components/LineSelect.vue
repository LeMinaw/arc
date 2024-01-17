<script setup>
  import { computed, ref, watch, watchEffect } from "vue"

  import Listbox from "./ui/listbox/Listbox.vue"
  import ListboxButton from "./ui/listbox/ListboxButton.vue"
  import ListboxOption from "./ui/listbox/ListboxOption.vue"
  import ListboxOptions from "./ui/listbox/ListboxOptions.vue"

  const props = defineProps({
    lines: {
      type: Array,
      default: [],
    },
  })

  const filter = defineModel()

  const selectedLines = ref([])
  const selectedManufacturers = ref([])

  const manufacturers = computed(() => [
    ...new Set(props.lines.map(line => line.manufacturer)),
  ])

  const selectedManufacturersLines = computed(() =>
    props.lines.filter(line => selectedManufacturers.value.includes(line.manufacturer))
  )

  watchEffect(() => {
    filter.value = product => {
      const linesToFilter = selectedLines.value.length
        ? selectedLines.value
        : selectedManufacturersLines.value

      return linesToFilter.length
        ? linesToFilter.map(line => line.id).includes(product.line_id)
        : true
    }
  })

  watch(selectedManufacturersLines, selectedManufacturersLines => {
    selectedLines.value = selectedLines.value.filter(line =>
      selectedManufacturersLines.includes(line)
    )
  })

  const isDisabled = line =>
    selectedManufacturers.value.length
      ? !selectedManufacturersLines.value.includes(line)
      : false
</script>

<template>
  <div class="mt-4">
    <span class="mr-2">Fabriquant :</span>

    <Listbox v-model="selectedManufacturers" multiple>
      <ListboxButton>
        {{ selectedManufacturers.map(m => m.name).join(", ") || "Tous" }}
      </ListboxButton>

      <ListboxOptions>
        <ListboxOption v-for="manufacturer in manufacturers" :value="manufacturer">
          {{ manufacturer.name }}
        </ListboxOption>
      </ListboxOptions>
    </Listbox>
  </div>

  <div class="mt-4">
    <span class="mr-2">Gamme :</span>

    <Listbox v-model="selectedLines" multiple>
      <ListboxButton>
        {{ selectedLines.map(m => m.name).join(", ") || "Toutes" }}
      </ListboxButton>

      <ListboxOptions>
        <ListboxOption v-for="line in lines" :value="line" :disabled="isDisabled(line)">
          {{ line.manufacturer.name }} - {{ line.name }}
        </ListboxOption>
      </ListboxOptions>
    </Listbox>
  </div>
</template>

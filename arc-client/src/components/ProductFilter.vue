<script setup>
  import PropertySelect from "../components/PropertySelect.vue"
  import PropertySwitch from "../components/PropertySwitch.vue"
  import LineSelect from "./LineSelect.vue"

  import { capitalize } from "../business/utils"

  defineProps({
    category: {
      type: Object,
      required: true,
    },
    lines: {
      type: Array,
      default: [],
    },
  })

  const selectedSpecs = defineModel("selectedSpecs")
  const selectedLines = defineModel("selectedLines")
</script>

<template>
  <LineSelect :lines="lines" v-model="selectedLines" />

  <div v-for="(schema, propertyName) of category.specs_schema.properties">
    <div>{{ capitalize(schema.title) }}</div>

    <PropertySwitch
      v-if="schema.type === 'boolean'"
      v-model="selectedSpecs[propertyName]"
    />
    <PropertySelect
      v-else-if="schema.enum"
      v-model="selectedSpecs[propertyName]"
      :values="schema.enum"
      :unit="schema.unit"
    />
    <input
      v-else-if="schema.type === 'integer'"
      v-model="selectedSpecs[propertyName]"
      type="number"
    />
    <input v-else v-model="selectedSpecs[propertyName]" />

    <i>{{ schema.description }}</i>
  </div>
</template>

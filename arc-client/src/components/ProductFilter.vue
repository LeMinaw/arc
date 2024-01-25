<script setup>
  import { ref, watchEffect, inject } from "vue"
  import { InformationCircleIcon } from "@heroicons/vue/24/outline"

  import PropertySelect from "../components/PropertySelect.vue"
  import PropertySwitch from "../components/PropertySwitch.vue"
  import PropertyRange from "./PropertyRange.vue"
  import PropertyNumber from "./PropertyNumber.vue"
  import PropertyString from "./PropertyString.vue"
  import LineSelect from "./LineSelect.vue"
  import Card from "./ui/Card.vue"

  import { capitalize } from "../business/utils"

  const category = inject("category")
  const products = inject("products")

  const filters = defineModel()

  // Fetch lines from products

  const lines = ref([])

  watchEffect(async () => {
    const uris = [...new Set(products.value.map(product => product.line))]

    lines.value = await Promise.all(
      uris.filter(uri => uri !== null).map(async uri => fetch(uri).then(r => r.json()))
    )
  })
</script>

<template>
  <Card title="Caractéristiques">
    <LineSelect :lines="lines" v-model="filters.$line" />

    <div
      v-for="(schema, propertyName) of category.specs_schema.properties"
      class="mt-4"
    >
      <span class="mr-2">{{ capitalize(schema.title || propertyName) }} :</span>

      <PropertySwitch
        v-if="schema.type === 'boolean'"
        v-model="filters[propertyName]"
        :property="propertyName"
      />
      <PropertySelect
        v-else-if="schema.enum"
        v-model="filters[propertyName]"
        :property="propertyName"
        :values="schema.enum"
        :unit="schema.unit"
      />
      <PropertyRange
        v-else-if="schema.$ref === '#/$defs/range'"
        v-model="filters[propertyName]"
        :property="propertyName"
        :unit="schema.unit"
      />
      <PropertyNumber
        v-else-if="schema.type === 'integer'"
        v-model="filters[propertyName]"
        :property="propertyName"
        :unit="schema.unit"
      />
      <PropertyString v-else v-model="filters[propertyName]" :property="propertyName" />

      <div
        v-if="schema.description"
        class="flex items-center gap-1 text-sm text-zinc-700"
      >
        <InformationCircleIcon class="w-5 shrink-0" /> <em>{{ schema.description }}</em>
      </div>
    </div>
  </Card>
</template>

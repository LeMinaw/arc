<script setup>
  import { computed } from "vue"
  import { InformationCircleIcon } from "@heroicons/vue/24/outline"

  import { capitalize } from "../business/utils"
  import BooleanStatus from "./ui/BooleanStatus.vue"

  const props = defineProps({
    product: Object,
    schema: Object,
  })

  const schema = computed(() => props.schema.properties)

  const properties = computed(() =>
    Object.entries(props.product.specs).map(([id, value]) => {
      const field_schema = schema.value[id]

      return {
        id,
        title: field_schema ? field_schema.title : null,
        value,
        unit: field_schema ? field_schema.unit : null,
        description: field_schema ? field_schema.description : null,
      }
    })
  )
</script>

<template>
  <ul>
    <li v-for="{ id, title, value, unit, description } in properties" class="mb-2">
      <p>
        {{ capitalize(title || id) }} :
        <BooleanStatus
          v-if="typeof value === 'boolean'"
          :value="value"
          class="align-middle"
        />
        <b v-else>{{ value }} {{ unit }}</b>
      </p>

      <div
        v-if="description"
        class="pl-1 flex items-center gap-1 text-sm text-zinc-700"
      >
        <InformationCircleIcon class="h-6" /> <em>{{ description }}</em>
      </div>
    </li>
  </ul>
</template>

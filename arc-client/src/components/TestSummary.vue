<script setup>
  import { computed } from "vue"
  import { InformationCircleIcon } from "@heroicons/vue/24/outline"
  import { formatDatetime } from "../business/time"

  const props = defineProps({ item: Object })

  const schema = computed(() => props.item.test_bench.data_schema.properties)

  const properties = computed(() =>
    Object.entries(props.item.test.data).map(([id, value]) => {
      const field_schema = schema.value[id]

      return {
        id,
        title: field_schema.title,
        value,
        unit: field_schema.unit,
        description: field_schema.description,
      }
    })
  )
</script>

<template>
  <ul>
    <li>
      Date d'essai :
      <b>{{ formatDatetime(item.test.date) }}</b>
    </li>

    <li v-for="{ id, title, value, unit, description } in properties">
      <p>
        {{ title || id }} :
        <b>{{ value }}{{ unit }}</b>
      </p>
      <div class="pl-1 flex items-center gap-1 text-sm text-zinc-700">
        <InformationCircleIcon class="h-6" /> <em>{{ description }}</em>
      </div>
    </li>
  </ul>
</template>

<script setup>
  import { reactive, ref } from "vue"
  import { createAjv } from "@jsonforms/core"
  import { JsonForms } from "@jsonforms/vue"
  import { vanillaRenderers } from "@jsonforms/vue-vanilla"

  import Button from "./ui/Button.vue"

  const defaultsAjv = createAjv({ useDefaults: true })

  const renderers = [...vanillaRenderers]

  const props = defineProps({
    schema: {
      type: Object,
      required: true,
    },
    initialData: {
      type: Object,
      default: {},
    },
  })

  const data = reactive({ ...props.initialData })
  const errors = ref([])

  const onChange = event => {
    Object.entries(event.data).forEach(([key, value]) => (data[key] = value))
    errors.value = event.errors
  }
</script>

<template>
  {{ data }}
  {{ errors }}

  <JsonForms
    :data="data"
    :schema="schema"
    :renderers="renderers"
    :ajv="defaultsAjv"
    @change="onChange"
  />

  <Button :disabled="errors.length" @click="$emit('submit', data)"> Valider </Button>
</template>

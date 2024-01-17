<script setup>
  defineProps({
    title: {
      type: String,
      default: "",
    },
    as: {
      type: String,
      default: "div",
    },
  })
</script>

<template>
  <component :is="as">
    <div class="m-2 bg-zinc-200 shadow-md">
      <div v-if="title" class="p-2 text-lg font-bold bg-orange-400 text-zinc-950">
        {{ title }}
      </div>

      <div class="p-2 border border-zinc-400" :class="{ 'border-t-0': title }">
        <slot />
      </div>
    </div>
  </component>
</template>

<script setup>
  import { watch } from "vue"
  import { XMarkIcon } from "@heroicons/vue/24/outline"

  import ModalBackdrop from "./ModalBackdrop.vue"

  const props = defineProps({
    show: {
      type: Boolean,
      default: false,
    },
  })

  const onKeydownEscape = event => {
    if (event.key === "Escape") this.$emit("close")
  }

  watch(props.show, show => {
    if (show) document.addEventListener("keydown", onKeydownEscape)
    else document.removeEventListener("keydown", onKeydownEscape)
  })
</script>

<template>
  <ModalBackdrop v-if="show" @click="$emit('close')">
    <div class="m-4 bg-zinc-200 shadow-xl" @click.stop>
      <div class="flex items-center h-12 bg-orange-400">
        <h3 class="flex-grow px-4 font-bold text-lg">
          <slot name="title">Information</slot>
        </h3>
        <div
          class="flex items-center bg-zinc-800 text-zinc-100 aspect-square h-full cursor-pointer hover:bg-red-600 active:bg-red-800 transition-all"
          tabindex="0"
          @click="$emit('close')"
        >
          <XMarkIcon class="m-auto h-8" />
        </div>
      </div>

      <div class="p-4">
        <slot />
      </div>
    </div>
  </ModalBackdrop>
</template>

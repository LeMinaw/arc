<script setup>
  import { computed, ref } from "vue"
  import { ArrowPathIcon } from "@heroicons/vue/24/outline"

  import { isDigit, capitalize } from "../business/utils"
  import { formatRelativeTime, formatDatetime } from "../business/time"
  import { fetchItem } from "../business/arc"
  import Title from "../components/ui/Title.vue"
  import Subtitle from "../components/ui/Subtitle.vue"
  import Button from "../components/ui/Button.vue"
  import TestSummary from "../components/TestSummary.vue"

  const id = ref()
  const item = ref()
  const loading = ref(false)

  const fetch = async () => {
    item.value = null
    loading.value = true
    item.value = await fetchItem(id.value)
    loading.value = false
  }

  const filterNumKeys = event => {
    if (event.key.length == 1 && !isDigit(event.key)) {
      event.preventDefault()
    }
  }
</script>

<template>
  <div class="max-w-prose mx-auto">
    <Title>Vérification d'article</Title>

    <p class="mx-2 my-4">
      Cette page permet d'accéder aux données de suivi des articles. Entrez un code
      d'identification, et vous pourrez obtenir les informations de traçabilité
      disponibles.
    </p>

    <form class="mx-2 my-4 p-2 bg-zinc-200 border border-zinc-300 shadow-md">
      <label class="text-lg text-zinc-700">Code d'identification de l'article</label>

      <div class="pt-2 flex justify-stretch">
        <input
          class="w-0 px-2 flex-grow text-4xl font-mono bg-zinc-50 border-transparent border-2 border-r-0 focus:border-zinc-900"
          v-model="id"
          type="number"
          min="0"
          @keydown="filterNumKeys"
        />

        <Button @click.prevent="fetch">Valider</Button>
      </div>
    </form>

    <div v-if="loading" class="flex justify-center">
      <ArrowPathIcon class="w-16 animate-spin" />
    </div>

    <div v-if="item" class="mx-2 my-4 bg-zinc-200 shadow-md">
      <div class="p-2 text-lg font-bold bg-orange-400 text-zinc-950">
        Correspondance trouvée
      </div>
      <div class="p-2 border border-t-0 border-zinc-300">
        <h4 class="text-lg">Données de produit</h4>
        <ul class="pl-2">
          <li>
            Gamme :
            <b>{{ item.product.line_name || "N.C." }}</b>
          </li>
          <li>
            Produit :
            <b>{{ item.product.name }}</b>
          </li>
          <li>
            Référence fabriquant :
            <b>{{ item.product.reference || "N.C." }}</b>
          </li>
        </ul>

        <h4 class="pt-2 text-lg">Données d'article</h4>
        <ul class="pl-2">
          <li>
            État d'inventaire :
            <b>{{ item.in_stock ? "En stock" : "Hors stock" }}</b>
          </li>
          <li v-if="!item.in_stock">
            Sortie d'inventaire :
            <b>{{ item.out_date }}</b>
          </li>
          <li>
            Ajout à la base :
            <b>{{ formatDatetime(item.add_date) }}</b>
          </li>
          <li>
            Dernière modification :
            <b>{{ formatDatetime(item.mod_date) }}</b>
          </li>
        </ul>

        <h4 class="pt-2 text-lg">Données métrologiques</h4>
        <div class="pl-2">
          <TestSummary v-if="item.test" :item="item" />
          <em v-else>Aucune donnée expérimentale n'est disponible.</em>
        </div>

        <div class="pt-2 flex justify-end">
          <a href="">
            <Button>Voir la fiche produit</Button>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  input[type="number"] {
    appearance: textfield;
    outline: none;
  }

  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }
</style>

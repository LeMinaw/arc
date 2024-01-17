<script setup>
  import { ref } from "vue"
  import { ArrowPathIcon } from "@heroicons/vue/24/outline"

  import { isDigit } from "../business/utils"
  import { formatDatetime } from "../business/time"
  import { fetchItem } from "../business/arc"
  import Title from "../components/ui/Title.vue"
  import Button from "../components/ui/Button.vue"
  import TestSummary from "../components/TestSummary.vue"
  import Card from "../components/ui/Card.vue"

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

    <Card as="form">
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
    </Card>

    <div v-if="loading" class="flex justify-center">
      <ArrowPathIcon class="w-16 animate-spin" />
    </div>

    <Card v-if="item" title="Correspondance trouvée">
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
    </Card>
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

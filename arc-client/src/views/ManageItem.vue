<script setup>
  import { ref, watchEffect } from "vue"
  import { useRoute } from "vue-router"

  import Title from "../components/ui/Title.vue"
  import Subtitle from "../components/ui/Subtitle.vue"
  import Modal from "../components/ui/Modal.vue"
  import Button from "../components/ui/Button.vue"
  import TestForm from "../components/TestForm.vue"

  import { formatDatetime, formatRelativeTime } from "../business/time"
  import { fetchItem, deleteItem, patchItem } from "../business/arc"

  const route = useRoute()

  const item = ref(null)
  const showDeleteModal = ref(false)
  const showStockModal = ref(false)
  const resultMessage = ref("")

  const editItemStock = async () => {
    const data = item.value.in_stock
      ? { in_stock: false, out_date: new Date().toISOString() }
      : { in_stock: true }

    resultMessage.value = (await patchItem(item.value.id, data)).detail || ""
  }

  const delItem = async () => {
    resultMessage.value = (await deleteItem(item.value.id)).detail || ""
  }

  watchEffect(async () => {
    item.value = await fetchItem(route.params.id)
  })
</script>

<template>
  <div v-if="item !== null">
    <Title>Édition de l'objet</Title>

    <p class="font-bold text-2xl">
      <span class="text-zinc-500">
        {{ item.product.name }}
      </span>
      #{{ item.id }}
    </p>

    <p>{{ item.product.line_name }}</p>

    <p v-if="item.product.reference">Réf. {{ item.product.reference }}</p>

    <router-link :to="{ name: 'product', params: { id: item.product.id } }">
      Voir la page produit
    </router-link>
    <a> Voir les données de suivi </a>

    <img :src="item.product.image" />

    <div class="flex gap-2">
      <Button @click="showStockModal = true">
        {{ item.in_stock ? "Sortie de stock" : "Retour en stock" }}
      </Button>
      <Button class="bg-red-500 text-zinc-950" @click="showDeleteModal = true">
        Supprimer
      </Button>
    </div>

    <p>Ajouté {{ formatRelativeTime(item.add_date) }}</p>
    <p>Dernière édition {{ formatRelativeTime(item.mod_date) }}</p>

    <Subtitle>Gestion de stock</Subtitle>

    <p>
      Actuellement : <b>{{ item.in_stock ? "en stock" : "hors stock" }}</b>
    </p>
    <p>
      Sortie d'inventaire : <b>{{ formatDatetime(item.out_date) }}</b>
    </p>

    <Subtitle>Édition des données de l'objet</Subtitle>

    {{ item }}

    <Subtitle>Édition des données de test</Subtitle>

    <TestForm />

    <pre>
      {{ item.test }}
    </pre>

    <Modal :show="showStockModal" @close="showStockModal = false">
      <p>
        Vous vous apprêtez à marquer l'objet
        <b>{{ item.product.name }}</b> d'identifiant <b>#{{ item.id }}</b> comme
        <b>{{ item.in_stock ? "hors stock" : "en stock" }}</b
        >.
      </p>

      <div class="flex justify-between mt-4">
        <Button @click="showStockModal = false">Annuler</Button>
        <Button @click="editItemStock">Confirmer</Button>
      </div>
    </Modal>

    <Modal :show="showDeleteModal" @close="showDeleteModal = false">
      <template #title>Avertissement</template>

      <p>
        Vous vous apprêtez à supprimer définitivement l'objet
        <b>{{ item.product.name }}</b> d'identifiant <b>#{{ item.id }}</b
        >.
      </p>
      <p class="mt-2">
        Cette action ne devrait servir qu'à corriger une erreur de saisie. Pour retirer
        un objet de l'inventaire, utilisez l'option <em>Sortie de stock</em>.
      </p>

      <div class="flex justify-between mt-4">
        <Button @click="showDeleteModal = false">Annuler</Button>
        <Button class="bg-red-500 text-zinc-950" @click="delItem">
          Supprimer l'objet
        </Button>
      </div>
    </Modal>

    <Modal :show="resultMessage.length" @close="resultMessage = ''">
      <p>{{ resultMessage }}</p>

      <div class="flex justify-between mt-4">
        <Button @click="resultMessage = ''">OK</Button>
      </div>
    </Modal>
  </div>

  <div v-else>
    <Title>Nouveau produit</Title>
  </div>
</template>

<script setup>
  import { Transition, onErrorCaptured, ref } from "vue"

  import BaseLayout from "./layouts/BaseLayout.vue"
  import Footer from "./components/Footer.vue"
  import Navbar from "./components/Navbar.vue"
  import Alert from "./components/ui/Alert.vue"

  const error = ref()

  onErrorCaptured((err, instance, info) => {
    error.value = err.toString()
  })
</script>

<template>
  <BaseLayout>
    <header>
      <Navbar />
    </header>

    <main class="flex-grow">
      <RouterView v-slot="{ Component }">
        <template v-if="Component">
          <Transition mode="out-in">
            <div>
              <Suspense>
                <component :is="Component" />

                <template #fallback>
                  <Alert>
                    <p>Chargement...</p>
                    <p>Ça ne prendra qu'une année ou deux.</p>
                  </Alert>
                </template>
              </Suspense>
            </div>
          </Transition>
        </template>
      </RouterView>

      <Alert v-if="error" class="mx-auto alert-error">{{ error }}</Alert>
    </main>

    <footer>
      <Footer />
    </footer>
  </BaseLayout>
</template>

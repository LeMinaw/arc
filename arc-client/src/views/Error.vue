<script setup>
	import Alert from '../components/ui/Alert.vue'

	const props = defineProps({
		message: {
			type: String,
			default: 'Une erreur innatendue est survenue. 😳'
		},
	})
</script>

<template>
	<Alert class="alert-error">
		<p>{{ message }}</p>
	</Alert>
</template>

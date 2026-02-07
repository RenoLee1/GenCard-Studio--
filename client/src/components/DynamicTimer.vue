<template>
  <div class="timer-container" :style="style">
    <div class="timer-label" v-if="title" :style="{ color: textColor }">{{ title }}</div>
    <div class="timer-value" :style="{ color: textColor }">{{ remaining }}s</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'

const props = defineProps({
  title: String,
  seconds: { type: Number, default: 60 },
  style: { type: Object, default: () => ({}) }
})

const remaining = ref(props.seconds)
let timer = null

const textColor = computed(() => props.style.color || 'inherit')

onMounted(() => {
  timer = setInterval(() => {
    if (remaining.value > 0) remaining.value--
    else clearInterval(timer)
  }, 1000)
})
onBeforeUnmount(() => clearInterval(timer))
</script>

<style scoped>
.timer-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
  border-radius: 6px;
  background: transparent;
}
.timer-value {
  font-size: 1.5em;
  font-weight: bold;
}
.timer-label {
  opacity: 0.8;
  font-size: 0.9em;
}
</style>
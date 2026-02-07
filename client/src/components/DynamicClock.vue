<template>
  <div class="atom-clock" :style="finalStyle">
    {{ timeStr }}
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'

const props = defineProps({
  format: { type: String, default: 'HH:mm:ss' },
  style: { type: Object, default: () => ({}) }
})

const timeStr = ref('')
let timer = null

const updateTime = () => {
  const now = new Date()
  if (props.format === 'HH:mm') {
    timeStr.value = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else {
    timeStr.value = now.toLocaleTimeString()
  }
}

const finalStyle = computed(() => ({
  fontFamily: 'monospace',
  fontWeight: 'bold',
  ...props.style
}))

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onBeforeUnmount(() => clearInterval(timer))
</script>

<style scoped>
.atom-clock {
  display: inline-block;
  line-height: 1;
}
</style>
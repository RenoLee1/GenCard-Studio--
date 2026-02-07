<template>
  <div
    class="motion-wrapper animate__animated"
    :class="[`animate__${type}`, { 'animate__infinite': loop }]"
    :style="style"
  >
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, default: 'fadeIn' },
  delay: { type: Number, default: 0 },
  duration: { type: Number, default: 1000 },
  loop: { type: Boolean, default: false }
})

const style = computed(() => ({
  '--animate-duration': `${props.duration}ms`,
  'animation-delay': `${props.delay}ms`
}))
</script>

<style scoped>
.motion-wrapper {
  display: block;
  width: 100%;
}
</style>
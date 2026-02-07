<template>
  <div class="atom-stack" :style="flexStyle">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  direction: { type: String, default: 'vertical' },
  gap: { type: [Number, String], default: 0 },
  align: { type: String, default: 'stretch' },
  justify: { type: String, default: 'start' },
  wrap: { type: Boolean, default: false },
  style: { type: Object, default: () => ({}) }
})

const flexStyle = computed(() => ({
  display: 'flex',
  flexDirection: props.direction === 'horizontal' ? 'row' : 'column',
  gap: typeof props.gap === 'number' ? `${props.gap}px` : props.gap,
  alignItems: props.align,
  justifyContent: props.justify,
  flexWrap: props.wrap ? 'wrap' : 'nowrap',
  width: '100%',
  ...props.style
}))
</script>
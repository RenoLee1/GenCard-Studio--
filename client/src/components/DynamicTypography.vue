<template>
  <component :is="tag" :style="textStyle">
    {{ content }}
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'body' },
  content: { type: String, default: '' },
  color: { type: String, default: 'inherit' },
  bold: { type: Boolean, default: false },
  align: { type: String, default: 'left' },
  style: { type: Object, default: () => ({}) }
})

const tag = computed(() => {
  if (['h1', 'h2', 'h3', 'h4'].includes(props.variant)) return props.variant
  return 'div'
})

const textStyle = computed(() => ({
  color: props.color,
  fontWeight: props.bold ? 'bold' : 'normal',
  textAlign: props.align,
  fontSize: props.variant === 'caption' ? '12px' : undefined,
  opacity: props.variant === 'caption' ? 0.7 : 1,
  lineHeight: 1.5,
  margin: 0,
  ...props.style
}))
</script>
<template>
  <div class="atom-box" :style="customStyle">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // 允许接收来自 LLM 的各种样式参数
  padding: { type: [String, Number], default: 0 },
  margin: { type: [String, Number], default: 0 },
  background: { type: String, default: 'transparent' },
  radius: { type: [String, Number], default: 0 },
  border: { type: String, default: 'none' },
  shadow: { type: String, default: 'none' },
  // 允许直接传 style 对象覆盖
  style: { type: Object, default: () => ({}) }
})

const customStyle = computed(() => {
  const toPx = (val) => (typeof val === 'number' ? `${val}px` : val)

  return {
    padding: toPx(props.padding),
    margin: toPx(props.margin),
    background: props.background,
    borderRadius: toPx(props.radius),
    border: props.border,
    boxShadow: props.shadow,
    ...props.style // 兜底混合
  }
})
</script>

<style scoped>
.atom-box {
  box-sizing: border-box;
  /* 默认相对定位，方便内部绝对定位 */
  position: relative;
  overflow: hidden;
}
</style>
<template>
  <div class="dynamic-card" :style="style">
    <div v-if="title" class="card-header">
      {{ title }}
    </div>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  style: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
/* 这里只写最基础的 reset 样式，具体的颜色/边框由 props 决定 */
.dynamic-card {
  box-sizing: border-box;
  overflow: hidden;
  /* 默认样式，会被 props.style 覆盖 */
  background: white;
  border-radius: 8px;
  padding: 16px;
}
.card-header {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 12px;
  opacity: 0.9;
}
</style>
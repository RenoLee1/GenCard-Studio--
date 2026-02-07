<template>
  <div :style="style">
    {{ content }}
  </div>
</template>

<script setup>
defineProps({
  content: String,
  style: { type: Object, default: () => ({}) }
})
</script>
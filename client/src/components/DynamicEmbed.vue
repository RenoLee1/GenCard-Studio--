<template>
  <div class="atom-embed" :style="containerStyle">
    <iframe
      class="embed-frame"
      v-if="blobUrl"
      :src="blobUrl"
      :style="iframeStyle"
      sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
      frameborder="0"
    ></iframe>
  </div>
</template>

<script setup>
import { computed, ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  code: { type: String, default: '' },
  width: { type: [String, Number], default: '100%' },
  height: { type: [String, Number], default: '400px' },
  style: { type: Object, default: () => ({}) }
})

const blobUrl = ref('')

watch(() => props.code, (newCode) => {
  // 1. 清理旧的 URL，防止内存泄漏
  if (blobUrl.value) URL.revokeObjectURL(blobUrl.value)

  if (!newCode) {
    blobUrl.value = ''
    return
  }

  const blob = new Blob([newCode], { type: 'text/html' })
  blobUrl.value = URL.createObjectURL(blob)
}, { immediate: true })

onBeforeUnmount(() => {
  if (blobUrl.value) URL.revokeObjectURL(blobUrl.value)
})

const containerStyle = computed(() => ({
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
  height: typeof props.height === 'number' ? `${props.height}px` : props.height,
  borderRadius: '12px',
  overflow: 'hidden',
  background: '#fff',
  ...props.style
}))

const iframeStyle = computed(() => ({
  width: '100%',
  height: '100%',
  display: 'block'
}))
</script>

<style scoped>
.atom-embed {
  display: block;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  position: relative;
}
</style>
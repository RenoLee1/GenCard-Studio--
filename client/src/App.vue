<template>
  <div class="studio-layout">

    <div class="panel-left">
      <div class="content-wrapper">
        <div class="brand-header">
          <div class="logo-icon">🔮</div>
          <div>
            <h1>GenCard Studio</h1>
            <p class="subtitle">AI UI Generator</p>
          </div>
        </div>

        <div class="status-bar">
          <div class="mode-tag" :class="schema ? 'mode-edit' : 'mode-create'">
            {{ schema ? '✏️ 修改模式 (Context Aware)' : '✨ 创建模式 (New)' }}
          </div>

          <div class="toolbar" v-if="schema">
            <button @click="handleRetry" class="tool-btn" title="重新生成">
              🔄 重新生成
            </button>
            <button @click="handleClear" class="tool-btn danger" title="清空">
              🗑️ 清空
            </button>
          </div>
        </div>

        <div class="input-box-container" :class="{ 'is-loading': loading }">
          <textarea
            v-model="prompt"
            :placeholder="inputPlaceholder"
            @keydown.enter.ctrl="handleGenerate"
          ></textarea>

          <div class="action-bar">
            <span class="hint">Ctrl + Enter</span>
            <button @click="handleGenerate" :disabled="loading" class="generate-btn">
              <span v-if="!loading">{{ schema ? '提交修改' : '生成 UI' }}</span>
              <span v-else class="loader"></span>
            </button>
          </div>
        </div>

        <div class="quick-prompts" v-if="!schema">
          <p>试试点击：</p>
          <div class="tags">
            <span @click="fillPrompt('生成一个赛博朋克风格的警告卡片，红黑色调，带倒计时')">🔴 警告卡片</span>
            <span @click="fillPrompt('生成一个极简时钟，黑色背景，绿色大字体')">⏰ 数字时钟</span>
            <span @click="fillPrompt('生成一个电商商品卡片，包含评分和购买按钮')">🛍️ 商品卡片</span>
          </div>
        </div>
      </div>
    </div>

    <div class="panel-divider"></div>

    <div class="panel-right">
      <div class="canvas-wrapper">

        <FormProvider :form="form" v-if="schema">
          <SchemaField :schema="schema" :key="renderKey" />
        </FormProvider>

        <div v-else class="empty-state">
          <div class="empty-icon">🎨</div>
          <p>在左侧输入描述，<br>AI 将在此处生成界面</p>
        </div>
      </div>

      <div class="debug-toggle" @click="showDebug = !showDebug">
        {{ showDebug ? '隐藏源码' : '查看 JSON' }}
      </div>
      <div v-if="showDebug" class="debug-panel">
        <pre>{{ JSON.stringify(schema, null, 2) }}</pre>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, shallowRef, computed } from 'vue'
import axios from 'axios'
import { createForm } from '@formily/core' // 1. 引入 createForm
import { createSchemaField, FormProvider } from '@formily/vue'
import { ComponentRegistry } from './components/index.js'

// --- Init Formily ---
const form = shallowRef(createForm())

const { SchemaField } = createSchemaField({
  components: ComponentRegistry
})

// --- State ---
const prompt = ref('')
const loading = ref(false)
const schema = shallowRef(null)
const lastPrompt = ref('')
const showDebug = ref(false)
const renderKey = ref(0)

// --- Computed ---
const inputPlaceholder = computed(() => {
  return schema.value
    ? '💡 哪里不满意？\n例如："把背景改成深蓝色" 或 "把按钮换成红色"'
    : '描述你想要的界面...\n例如：生成一个带有倒计时的任务卡片'
})

// --- Actions ---

const handleGenerate = async () => {
  if (!prompt.value.trim()) return
  loading.value = true
  lastPrompt.value = prompt.value

  try {
    const payload = {
      query: prompt.value,
      history: schema.value
    }

    const res = await axios.post('http://localhost:8000/generate', payload)

    console.log("New Schema:", res.data.schema)

    form.value = createForm()

    schema.value = res.data.schema
    renderKey.value++
    prompt.value = ''

  } catch (e) {
    alert('Error: ' + e.message)
  } finally {
    loading.value = false
  }
}

const handleRetry = async () => {
  if (!lastPrompt.value) return
  if(!confirm("确定要重新生成吗？当前修改将丢失。")) return

  loading.value = true
  try {
    const res = await axios.post('http://localhost:8000/generate', {
      query: lastPrompt.value,
      history: null
    })

    form.value = createForm()

    schema.value = res.data.schema
    renderKey.value++
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  form.value = createForm()
  schema.value = null
  prompt.value = ''
  lastPrompt.value = ''
  renderKey.value = 0
}

const fillPrompt = (text) => {
  prompt.value = text
}
</script>

<style scoped>
* { box-sizing: border-box; }
.studio-layout { display: flex; height: 100vh; width: 100vw; background-color: #0f0f11; color: #fff; overflow: hidden; font-family: 'Inter', sans-serif; }
.panel-left { width: 380px; background: #18181b; padding: 30px; display: flex; flex-direction: column; justify-content: center; border-right: 1px solid #27272a; z-index: 2; }
.content-wrapper { width: 100%; }
.brand-header { display: flex; gap: 10px; margin-bottom: 20px; align-items: center; }
.brand-header h1 { margin: 0; font-size: 20px; font-weight: bold; }
.logo-icon { font-size: 24px; }
.subtitle { color: #666; font-size: 12px; margin: 0; }
.status-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; height: 30px; }
.mode-tag { font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 4px; }
.mode-create { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.mode-edit { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
.toolbar { display: flex; gap: 8px; }
.tool-btn { background: transparent; border: 1px solid #3f3f46; color: #a1a1aa; font-size: 11px; padding: 4px 8px; border-radius: 4px; cursor: pointer; transition: 0.2s; }
.tool-btn:hover { background: #27272a; color: white; }
.tool-btn.danger:hover { border-color: #ef4444; color: #ef4444; }
.input-box-container { background: #27272a; border: 1px solid #3f3f46; border-radius: 12px; padding: 12px; transition: 0.3s; }
.input-box-container:focus-within { border-color: #10b981; box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1); }
textarea { width: 100%; height: 100px; background: transparent; border: none; color: white; resize: none; outline: none; font-family: inherit; font-size: 14px; line-height: 1.5; }
.action-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; border-top: 1px solid #333; padding-top: 10px; }
.hint { font-size: 12px; color: #666; }
.generate-btn { background: #10b981; color: white; border: none; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: bold; display: flex; align-items: center; gap: 6px; }
.generate-btn:disabled { opacity: 0.5; cursor: wait; }
.quick-prompts { margin-top: 20px; }
.quick-prompts p { font-size: 12px; color: #666; margin-bottom: 8px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; }
.tags span { font-size: 11px; background: #222; padding: 4px 8px; border-radius: 10px; color: #888; cursor: pointer; border: 1px solid #333; transition: 0.2s; }
.tags span:hover { border-color: #555; color: white; background: #333; }
.panel-divider { width: 1px; background: linear-gradient(to bottom, transparent, #333, transparent); }
.panel-right { flex: 1; background-color: #111; background-image: linear-gradient(#1f1f1f 1px, transparent 1px), linear-gradient(90deg, #1f1f1f 1px, transparent 1px); background-size: 40px 40px; display: flex; justify-content: center; align-items: center; overflow: auto; padding: 40px; position: relative; }
.canvas-wrapper { min-width: 400px; max-width: 1200px; transition: 0.3s; }
.empty-state { text-align: center; color: #444; }
.empty-icon { font-size: 40px; margin-bottom: 10px; opacity: 0.3; }
.debug-toggle { position: absolute; bottom: 20px; right: 20px; cursor: pointer; color: #666; font-size: 12px; background: #222; padding: 4px 8px; border-radius: 4px; border: 1px solid #333; }
.debug-panel { position: absolute; bottom: 50px; right: 20px; background: rgba(0,0,0,0.9); padding: 10px; border-radius: 8px; color: lime; max-height: 300px; overflow: auto; width: 400px; font-size: 12px; border: 1px solid #333; }
.loader { width: 14px; height: 14px; border: 2px solid #fff; border-bottom-color: transparent; border-radius: 50%; display: inline-block; animation: rotation 1s linear infinite; }
@keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
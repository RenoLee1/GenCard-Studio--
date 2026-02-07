// client/src/components/index.js

// 1. 引入 Ant Design 组件
import {
  Rate,
  Progress,
  Tag,
  Button,
  Alert,
  Avatar
} from 'ant-design-vue'

// 2. 引入你刚刚上传的原子组件
// ⚠️ 务必确保文件名和这里 import 的名字完全一致
import DynamicBox from './DynamicBox.vue'
import DynamicStack from './DynamicStack.vue'
import DynamicTypography from './DynamicTypography.vue'
import DynamicTimer from './DynamicTimer.vue'
import DynamicMotion from './DynamicMotion.vue'
import DynamicClock from "./DynamicClock.vue";
import DynamicEmbed from "./DynamicEmbed.vue"; // 如果你有这个文件的话，没有请注释掉

// 3. 【核心映射表】
// 左边是 LLM 输出的字符串 (JSON里的 x-component)
// 右边是 实际渲染的 Vue 组件
export const ComponentRegistry = {
  // --- 布局原子 ---
  Box: DynamicBox,          // LLM 说 "Box" -> 渲染 DynamicBox
  Stack: DynamicStack,      // LLM 说 "Stack" -> 渲染 DynamicStack

  // --- 内容原子 ---
  Typography: DynamicTypography, // LLM 说 "Typography" -> 渲染 DynamicTypography

  // --- 业务组件 ---
  Countdown: DynamicTimer,  // LLM 说 "Countdown" -> 渲染 DynamicTimer

  // --- 动画组件 ---
  Motion: DynamicMotion,

  // --- Ant Design ---
  Rate,
  Progress,
  Tag,
  Alert,
  Button,
  Avatar,

  // --- 兼容旧 Prompt (防止 LLM 偶尔抽风用旧名字) ---
  Card: DynamicBox,
  Text: DynamicTypography,
  Row: DynamicStack,
  Column: DynamicStack,
  Clock: DynamicClock,
  Embed: DynamicEmbed,
}
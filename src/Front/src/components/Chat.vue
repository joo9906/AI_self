<template>
  <div class="flex flex-col flex-1 h-full">
    <div class="flex-1 overflow-y-auto p-4 border border-gray-200 mb-4 bg-gray-50 rounded-lg min-h-0">
      <div v-for="(msg, i) in messages" :key="i" class="mb-6">
        <div v-if="msg.role !== 'system'" :class="msg.role === 'user' ? 'text-right' : 'text-left'">
          <div :class="msg.role === 'user' ? 'inline-block bg-blue-100 text-blue-900 px-4 py-2 rounded-lg max-w-xs lg:max-w-md' : 'inline-block bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-xs lg:max-w-md'">
            <div class="font-semibold text-xs mb-1">{{ msg.role === 'user' ? '사용자' : 'AI' }}</div>
            <div v-if="msg.role === 'user'" class="whitespace-pre-wrap">{{ msg.content }}</div>
            <div v-else v-html="renderMarkdown(msg.content)" class="markdown-content"></div>
          </div>
        </div>
      </div>
      <div v-if="messages.length === 0" class="text-center text-gray-500 py-8">
        <p>대화를 시작해보세요</p>
      </div>
    </div>
    <form @submit.prevent="send" class="flex pb-2 gap-2 flex-shrink-0">
      <input 
        v-model="input" 
        class="flex-1 border border-gray-300 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400" 
        placeholder="메시지를 입력하세요" 
      />
      <button 
        type="submit"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition font-semibold"
      >
        전송
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { marked } from 'marked'

const props = defineProps(['messages'])
const emit = defineEmits(['send'])
const input = ref('')

function renderMarkdown(content) {
  return marked(content)
}

function send() {
  if (!input.value.trim()) return
  emit('send', { content: input.value.trim() })
  input.value = ''
}
</script>

<style scoped>
.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-weight: bold;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.markdown-content h1 { font-size: 1.5rem; }
.markdown-content h2 { font-size: 1.25rem; }
.markdown-content h3 { font-size: 1.125rem; }

.markdown-content p {
  margin-bottom: 0.75rem;
}

.markdown-content ul,
.markdown-content ol {
  margin-left: 1.5rem;
  margin-bottom: 0.75rem;
}

.markdown-content li {
  margin-bottom: 0.25rem;
}

.markdown-content strong {
  font-weight: bold;
}

.markdown-content em {
  font-style: italic;
}

.markdown-content code {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: monospace;
  font-size: 0.875rem;
}

.markdown-content pre {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 0.75rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 0.75rem 0;
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
}

.markdown-content blockquote {
  border-left: 4px solid #e5e7eb;
  padding-left: 1rem;
  margin: 0.75rem 0;
  color: #6b7280;
}

.markdown-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.75rem 0;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
  text-align: left;
}

.markdown-content th {
  background-color: #f9fafb;
  font-weight: bold;
}
</style> 
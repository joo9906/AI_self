<template>
  <div class="w-full max-w-4xl bg-white rounded-lg shadow-lg p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-blue-700">대화 기록</h2>
      <button 
        @click="$emit('back-to-chat')" 
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        채팅으로 돌아가기
      </button>
    </div>
    
    <div class="space-y-4 max-h-[600px] overflow-y-auto">
      <div v-for="(msg, idx) in messages.filter(m => m.role !== 'system')" :key="idx" 
           :class="msg.role === 'user' ? 'text-right' : 'text-left'">
        <div class="mb-2">
          <span class="text-xs text-gray-500">
            {{ msg.role === 'user' ? '사용자' : 'AI' }} - {{ formatTime(msg.timestamp) }}
          </span>
        </div>
        <div :class="msg.role === 'user' ? 'inline-block bg-blue-100 text-blue-900 px-4 py-2 rounded-lg max-w-xs lg:max-w-md' : 'inline-block bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-xs lg:max-w-md'">
          {{ msg.content }}
        </div>
      </div>
    </div>
    
    <div class="mt-6 pt-4 border-t">
      <div class="text-sm text-gray-600">
        <p><strong>총 대화 수:</strong> {{ messages.filter(m => m.role !== 'system').length }}개</p>
        <p><strong>세션 ID:</strong> {{ sessionId }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  messages: {
    type: Array,
    required: true
  },
  sessionId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['back-to-chat'])

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script> 
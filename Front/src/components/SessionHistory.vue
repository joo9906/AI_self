<template>
  <div class="w-full bg-white border-t border-gray-200 p-4 overflow-y-auto">
    <h2 class="text-lg font-bold mb-4 text-gray-800">대화 기록(최근 10개)</h2>
    <div v-if="patient && patient.messages.length > 0">
        <div v-for="(msg, i) in patient.messages.slice(-10)" :key="i" class="mb-2">
            <span class="font-bold">{{ msg.role === 'user' ? '사용자' : 'AI' }}:</span>
            <span>{{ msg.content }}</span>
        </div>
    </div>
    <div v-else class="text-center text-gray-500 py-8">
      <p>대화 기록이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { usePatientStore } from '@/stores/usePatientStore';

const store = usePatientStore();
const patient = computed(() => store.selectedPatient);
</script>

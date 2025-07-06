<template>
  <div class="flex flex-1 h-full">

    <!-- Left Panel: Patient Info and Session History -->
    <div class="w-1/3 min-w-[300px] max-w-[400px] p-4 border-r border-gray-200 flex flex-col">
      <PatientInfo :patient="patient.info" :session-id="patient.id" class="mb-4" />
      <button @click="toggleSessionHistory" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
        {{ showSessionHistory ? '대화 기록 숨기기' : '대화 기록 보기' }}
      </button>
      <SessionHistory v-if="showSessionHistory" class="flex-1 overflow-y-auto" />
    </div>

    <!-- Right Panel: Chat -->
    <div class="flex-1 flex flex-col p-4">
      <Chat :messages="patient.messages" @send="onSend" />
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePatientStore } from '@/stores/usePatientStore';
import PatientInfo from './PatientInfo.vue';
import Chat from './Chat.vue';
import SessionHistory from './SessionHistory.vue';

const route = useRoute();
const router = useRouter();
const store = usePatientStore();

const patient = computed(() => store.patients.find(p => p.id === route.params.id));

if (!patient.value) {
  // 잘못된 접근 시 메인으로
  router.replace('/');
}

const showSessionHistory = ref(false);

function toggleSessionHistory() {
  showSessionHistory.value = !showSessionHistory.value;
}

function makeLLMPrompt(patientData) {
  return `
[New_Patient]
1. 환자 기본 정보: 나이 ${patientData.age ?? ''}세, 성별 ${patientData.gender ?? ''}, 체중 ${patientData.weight ?? ''}kg, 흡연 여부: ${patientData.smoke ?? ''}
2. 진단 질병 정보: ${patientData.comorbidity || '없음'}
3. 약물 투여 기록: ${patientData.drug || '없음'}
4. 알러지 반응 기록: ${patientData.allergies || '없음'}
5. 바이탈/검사 수치: 최고혈압 ${patientData.sbp ?? ''}, 최저혈압 ${patientData.dbp ?? ''}
6. 수술/시술 이력: ${patientData.procedures || '없음'}
전문 의료진들이 사용하는 언어로 답변해주세요.
대답은 보기 쉽게 정리하여 마크다운 형식으로 주세요.
`.trim();
}

async function onSend(message) {
  if (!patient.value) return;

  // 사용자 메시지 추가
  store.addMessage(patient.value.id, { ...message, role: 'user' });

  // system prompt 생성 (최초 메시지일 때만)
  let systemPrompt = '';
  const existingSystemPrompt = patient.value.messages.find(m => m.role === 'system');

  if (!existingSystemPrompt) {
    systemPrompt = makeLLMPrompt(patient.value.info);
    // Pinia store에 system 메시지 추가
    store.addMessage(patient.value.id, { role: 'system', content: systemPrompt });
  } else {
    systemPrompt = existingSystemPrompt.content;
  }

  // 서버로 메시지 전송
  let messageToSend = '';
  // 첫 메시지이거나, system prompt가 있고 assistant의 응답이 아직 없을 때
  if (!existingSystemPrompt || patient.value.messages.filter(m => m.role === 'assistant').length === 0) {
    messageToSend = `system: ${systemPrompt}\nuser: ${message.content}`;
  } else {
    messageToSend = `user: ${message.content}`;
  }

  try {
    const res = await fetch(`${import.meta.env.VITE_SERVER_API}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: patient.value.id,
        message: messageToSend
      })
    });
    const data = await res.json();
    const reply = data.reply?.answer || data.reply || 'AI 응답이 없습니다.';
    store.addMessage(patient.value.id, { role: 'assistant', content: reply });
  } catch (err) {
    console.error('Error fetching chat response:', err);
    store.addMessage(patient.value.id, { content: '서버 연결 실패.', role: 'assistant' });
  }
}
</script>
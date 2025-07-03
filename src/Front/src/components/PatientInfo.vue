<template>
  <div>
    <div class="w-72 min-w-[18rem] max-w-xs border border-gray-200 rounded-lg p-6 shadow-sm bg-white flex flex-col gap-2">
      <h3 class="font-bold text-lg mb-3 text-gray-800 border-b pb-2">환자 정보</h3>
      <div class="flex flex-col gap-2 text-sm">
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">환자 번호</span>
          <span class="font-semibold text-gray-900 break-all ml-5">{{ sessionId }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">나이</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.age }}세</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">성별</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.gender }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">체중</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.weight }}kg</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">흡연여부</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.smoke }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">최고혈압</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.sbp }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">최저혈압</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.dbp }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">기저질환</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.comorbidity || '없음' }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">투약 약물</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.drug || '없음' }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">알러지</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.allergies || '없음' }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-700">수술/시술</span>
          <span class="font-semibold text-gray-900 ml-4">{{ patient.procedures || '없음' }}</span>
        </div>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  patient: {
    type: Object,
    required: true
  },
  sessionId: {
    type: String,
    required: true
  }
})
</script> 
<template>
  <div class="h-full overflow-y-auto p-4">
    <form @submit.prevent="submit" class="space-y-4 bg-white p-6 rounded-lg shadow-lg max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-6 text-center text-blue-700">환자 정보 입력</h2>
    
    <div>
      <label class="block text-gray-700 mb-1">나이</label>
      <input v-model="form.age" type="number" min="0" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">체중 (kg)</label>
      <input v-model="form.weight" type="number" min="0" step="0.1" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
    </div>
    
    <div class="flex gap-4">
      <div class="flex-1">
        <label class="block text-gray-700 mb-1">최고혈압</label>
        <input v-model="form.sbp" type="number" min="0" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
      </div>
      <div class="flex-1">
        <label class="block text-gray-700 mb-1">최저혈압</label>
        <input v-model="form.dbp" type="number" min="0" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
      </div>
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">기저질환</label>
      <input v-model="form.comorbidity" type="text" placeholder="예: 당뇨, 고혈압" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" />
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">성별</label>
      <div class="flex gap-4">
        <button type="button" :class="['flex-1 py-2 rounded border', form.gender === '남' ? 'bg-blue-500 text-white border-blue-500' : 'bg-white text-gray-700 border-gray-300']" @click="form.gender = '남'">남</button>
        <button type="button" :class="['flex-1 py-2 rounded border', form.gender === '여' ? 'bg-pink-500 text-white border-pink-500' : 'bg-white text-gray-700 border-gray-300']" @click="form.gender = '여'">여</button>
      </div>
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">흡연 여부</label>
      <div class="flex gap-4">
        <button type="button" :class="['flex-1 py-2 rounded border', form.smoke === '흡연자' ? 'bg-blue-500 text-white border-blue-500' : 'bg-white text-gray-700 border-gray-300']" @click="form.smoke = '흡연자'">흡연</button>
        <button type="button" :class="['flex-1 py-2 rounded border', form.smoke === '비흡연자' ? 'bg-blue-500 text-white border-green-500' : 'bg-white text-gray-700 border-gray-300']" @click="form.smoke = '비흡연자'">비흡연</button>
      </div>
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">투약 약물 정보</label>
      <input v-model="form.drug" type="text" placeholder="예: Epinephrine 1 MG Auto-Injection" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" />
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">알러지 정보</label>
      <input v-model="form.allergies" type="text" placeholder="예: 페니실린 알러지" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" />
    </div>
    
    <div>
      <label class="block text-gray-700 mb-1">수술 및 시술 정보</label>
      <input v-model="form.procedures" type="text" placeholder="예: 충수절제술" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" />
    </div>
    
    <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded font-semibold hover:bg-blue-700 transition">등록</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['submit'])

const form = reactive({
  age: '',
  gender: '',
  weight: '',
  sbp: '',
  dbp: '',
  smoke: '',
  comorbidity: '',
  drug: '',
  allergies: '',
  procedures: ''
})

function submit() {
  if (!form.gender) return alert('성별을 선택해주세요.')
  if (!form.smoke) return alert('흡연 여부를 선택해주세요.')
  
  // 비어 있는 항목 기본값 설정
  form.procedures ||= '없음'
  form.drug ||= '없음'
  form.allergies ||= '없음'
  form.comorbidity ||= '없음'
  
  emit('submit', { ...form })
}
</script> 
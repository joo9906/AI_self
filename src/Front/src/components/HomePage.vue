<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <div class="w-full max-w-xl bg-white rounded-2xl shadow-lg p-8">
      <h1 class="text-2xl font-bold text-blue-700 mb-6 text-center">환자 선택 또는 등록</h1>
      <div v-if="patients.length > 0" class="mb-8">
        <h2 class="text-lg font-semibold mb-2">기존 환자 목록</h2>
        <ul class="space-y-2">
          <li v-for="p in patients" :key="p.id" class="flex items-center justify-between bg-blue-50 rounded px-4 py-2">
            <span>{{ p.info.name || (p.info.age + '세/' + p.info.gender) }} ({{ p.id }})</span>
            <button class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700" @click="goChat(p.id)">대화 보기</button>
          </li>
        </ul>
      </div>
      <button class="w-full bg-green-600 text-white py-2 rounded font-semibold hover:bg-green-700 mb-2" @click="showForm = !showForm">+ 새 환자 등록</button>
      <div v-if="showForm" class="mt-4">
        <PatientForm @submit="registerPatient" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { usePatientStore } from '@/stores/usePatientStore';
import PatientForm from '@/components/PatientForm.vue';

const store = usePatientStore();
const patients = store.patients;
const router = useRouter();
const showForm = ref(false);

function registerPatient(form) {
  const newPatient = store.addPatient(form);
  store.selectPatient(newPatient.id);
  router.push(`/patient/${newPatient.id}`);
}

function goChat(id) {
  store.selectPatient(id);
  router.push(`/patient/${id}`);
}
</script>

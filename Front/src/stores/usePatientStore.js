import { defineStore } from 'pinia';
import { v4 as uuidv4 } from 'uuid';

export const usePatientStore = defineStore('patient', {
  state: () => ({
    patients: [], // { id, info, messages, summary }
    selectedPatientId: null,
  }),
  getters: {
    selectedPatient(state) {
      return state.patients.find(p => p.id === state.selectedPatientId);
    },
  },
  actions: {
    addPatient(patientInfo) {
      const newPatient = {
        id: uuidv4().slice(0, 8),
        info: patientInfo,
        messages: [],
        summary: null, // 요약 정보 추가
      };
      this.patients.push(newPatient);
      return newPatient;
    },
    selectPatient(id) {
      this.selectedPatientId = id;
    },
    addMessage(patientId, message) {
      const patient = this.patients.find(p => p.id === patientId);
      if (patient) {
        patient.messages.push(message);
      }
    },
    setSummary(patientId, summary) {
      const patient = this.patients.find(p => p.id === patientId);
      if (patient) {
        patient.summary = summary;
      }
    },
    // 기존 useChatStore의 기능들
    setLoading(status) {
      if (this.selectedPatient) {
        this.selectedPatient.isLoading = status;
      }
    },
    clearSession() {
        const index = this.patients.findIndex(p => p.id === this.selectedPatientId);
        if (index !== -1) {
            this.patients.splice(index, 1);
            this.selectedPatientId = null;
        }
    },
  },
  persist: {
    storage: sessionStorage,
  },
});
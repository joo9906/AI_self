<template>
  <div id="app" class="flex flex-col h-screen">
    <!-- Fixed navbar -->
    <div class="w-full flex justify-center pt-4 pb-2 sticky top-0 z-20">
      <nav class="w-[90%] bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 text-white shadow-lg rounded-2xl flex items-center justify-between px-6 py-3">
        <div class="flex items-center gap-3">
          <div class="bg-white bg-opacity-10 rounded-full p-2 shadow">
            <IdentificationIcon class="w-7 h-7 text-white drop-shadow" />
          </div>
          <span class="text-2xl font-extrabold drop-shadow-sm text-white">약물 투약 제안 챗봇</span>
        </div>
        <div class="flex items-center gap-4">
          <router-link to="/" class="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg font-semibold shadow transition">환자 목록/등록</router-link>
        </div>
      </nav>
    </div>
    <!-- Main content area -->
    <main class="flex-1 overflow-y-auto p-4 bg-gray-50">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { IdentificationIcon } from '@heroicons/vue/24/outline'
</script>

<style>
body {
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}
</style>

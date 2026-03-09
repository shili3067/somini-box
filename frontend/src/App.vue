<script setup lang="ts">
import { ref } from 'vue'
import {
  NConfigProvider,
  NGlobalStyle,
  NMessageProvider,
  darkTheme,
  NModal
} from 'naive-ui'
import axios from 'axios'

const theme = darkTheme
const url = ref('')
const loading = ref(false)
const videoInfo = ref<any>(null)
const previewVisible = ref(false)

// Download state
const isDownloading = ref(false)
const downloadPercent = ref(0)
const downloadStatus = ref('') // 'downloading', 'processing', 'completed', 'failed'
const taskId = ref('')
let pollInterval: any = null

const handleResolve = async () => {
  if (!url.value) return
  loading.value = true
  try {
    const res = await axios.post('http://127.0.0.1:18000/api/resolve', { url: url.value })
    if (res.data.success) {
      videoInfo.value = res.data.data
    } else {
      alert("解析失败: " + res.data.error)
    }
  } catch (err: any) {
    alert("请求失败: " + err.message + "，请确保后端服务正常运行。")
  } finally {
    loading.value = false
  }
}

const openPreview = () => {
  previewVisible.value = true
}

const startDownload = async () => {
  if (isDownloading.value || !videoInfo.value) return
  isDownloading.value = true
  downloadPercent.value = 0
  downloadStatus.value = 'starting'
  
  try {
    const res = await axios.post('http://127.0.0.1:18000/api/download', { url: videoInfo.value.url })
    if (res.data.success) {
      taskId.value = res.data.task_id
      pollDownloadStatus()
    } else {
      alert("下载启动失败: " + res.data.error)
      isDownloading.value = false
    }
  } catch (err: any) {
    alert("请求失败: " + err.message)
    isDownloading.value = false
  }
}

const pollDownloadStatus = () => {
  if (pollInterval) clearInterval(pollInterval)
  pollInterval = setInterval(async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:18000/api/download/${taskId.value}`)
      const data = res.data
      
      downloadStatus.value = data.status
      if (data.status === 'downloading') {
        downloadPercent.value = data.percent
      } else if (data.status === 'completed') {
        clearInterval(pollInterval)
        downloadPercent.value = 100
        
        // Trigger browser native download!
        const downloadUrl = `http://127.0.0.1:18000/api/download/file/${taskId.value}`
        const a = document.createElement('a')
        a.href = downloadUrl
        a.download = '' 
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)

        setTimeout(() => {
          isDownloading.value = false
        }, 4000)
      } else if (data.status === 'failed') {
        clearInterval(pollInterval)
        alert('下载失败: ' + data.error)
        isDownloading.value = false
      }
    } catch {
       clearInterval(pollInterval)
       isDownloading.value = false
    }
  }, 1000)
}

const getBestVideoUrl = () => {
  if (!videoInfo.value?.formats) return ''
  const formats = videoInfo.value.formats
  const mp4Formats = formats.filter((f: any) => f.ext === 'mp4' && f.vcodec !== 'none' && f.acodec !== 'none')
  if (mp4Formats.length > 0) return mp4Formats[mp4Formats.length - 1].url
  return formats[formats.length - 1].url
}
</script>

<template>
  <n-config-provider :theme="theme">
    <n-global-style />
    <n-message-provider>
      <div class="min-h-screen bg-[#0a0a0a] text-slate-200 flex flex-col font-sans selection:bg-blue-500/30 overflow-x-hidden">
        
        <!-- Navbar -->
        <header class="h-16 border-b border-white/5 bg-black/40 backdrop-blur-xl sticky top-0 z-50 flex items-center px-6 md:px-12">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <span class="text-white font-black text-sm">OV</span>
            </div>
            <span class="font-bold text-lg tracking-wide text-zinc-100">OmniVid<span class="text-blue-500">.</span></span>
          </div>
          <div class="ml-auto flex items-center gap-4">
             <div class="text-xs font-medium text-slate-500 px-3 py-1.5 rounded-full bg-white/5 border border-white/5">
                v1.0.0 Alpha
             </div>
          </div>
        </header>

        <!-- Main Content -->
        <main class="flex-1 flex flex-col items-center pt-24 pb-12 px-6 relative w-full">
          <!-- Ambient Glow Backgrounds -->
          <div class="absolute top-[5%] left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-blue-600/10 blur-[120px] rounded-[100%] pointer-events-none"></div>
          <div class="absolute top-[20%] left-[-10%] w-[400px] h-[400px] bg-purple-600/10 blur-[120px] rounded-[100%] pointer-events-none"></div>

          <!-- Hero Text -->
          <div class="text-center z-10 max-w-4xl space-y-6">
            <h1 class="text-5xl md:text-7xl font-extrabold tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-white/50">
              全平台视频轻巧解析
            </h1>
            <p class="text-lg md:text-xl text-zinc-400 tracking-wide font-light max-w-2xl mx-auto leading-relaxed">
              彻底告别繁杂的工具。只需粘贴链接，不论是 Bilibili 还是 YouTube，
              <br class="hidden md:block"/> 即刻享受极速原画解析、云端预览与高速下载体验。
            </p>
          </div>

          <!-- Search Bar Interactive Area -->
          <div class="w-full max-w-3xl mt-16 z-10">
            <div class="relative group">
              <!-- Glow effect behind the input -->
              <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-2xl blur opacity-20 group-hover:opacity-50 transition duration-700"></div>
              
              <div class="relative flex items-center bg-zinc-900 border border-white/10 rounded-2xl p-2 shadow-2xl transition-all h-20">
                <div class="pl-4 flex items-center justify-center text-zinc-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-13.35a4.5 4.5 0 0 0-6.364 0l-1.757 1.757m-4.596 4.606a4.5 4.5 0 0 0-1.242 7.244"/></svg>
                </div>
                <!-- Input field -->
                <input
                  v-model="url"
                  placeholder="https://www.bilibili.com/video/BV1..."
                  class="flex-1 bg-transparent text-lg md:text-xl text-zinc-100 placeholder-zinc-600 font-mono tracking-tight outline-none px-4 h-full"
                  @keyup.enter="handleResolve"
                />
                
                <!-- Action button -->
                <button
                  class="ml-2 h-full px-8 rounded-xl font-bold tracking-wide text-white bg-white/10 hover:bg-white/20 border border-white/5 transition-all outline-none flex items-center gap-2 group-hover:bg-blue-600 transform active:scale-95"
                  :disabled="loading"
                  @click="handleResolve"
                >
                  <span v-if="loading" class="animate-pulse flex items-center gap-2">
                     <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                     </svg>
                     解析中
                  </span>
                  <span v-else class="flex items-center gap-2 text-[15px]">
                     <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-7-7l7 7l-7 7"/></svg>
                  </span>
                </button>
              </div>
            </div>
            
            <div class="mt-8 flex items-center justify-center gap-6 text-[13px] text-zinc-500 font-medium tracking-wider">
              <span class="mr-2">Trusted by 1000+ Platforms</span>
              <div class="flex items-center gap-1.5 hover:text-white transition-colors cursor-default"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="#ff0000" d="M21.543 6.498C22 8.28 22 12 22 12s0 3.72-.457 5.502c-.254.985-.997 1.76-1.938 2.022C17.896 20 12 20 12 20s-5.893 0-7.605-.476c-.945-.266-1.687-1.04-1.938-2.022C2 15.72 2 12 2 12s0-3.72.457-5.502c.254-.985.997-1.76 1.938-2.022C6.107 4 12 4 12 4s5.896 0 7.605.476c.945.266 1.687 1.04 1.938 2.022M10 15.5l6-3.5l-6-3.5v7z"/></svg> YouTube</div>
              <div class="flex items-center gap-1.5 hover:text-white transition-colors cursor-default"><span class="text-[#00a1d6] font-bold text-lg leading-none">B</span> Bilibili</div>
              <div class="flex items-center gap-1.5 hover:text-white transition-colors cursor-default"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 448 512"><path fill="currentColor" d="M448 209.91a210.06 210.06 0 0 1-122.77-39.25v178.72A162.55 162.55 0 1 1 162.6 182.17v74.32c-35.15 1.58-63.51 30.54-63.51 66.15c0 37.07 30 67.11 67.07 67.11c37.06 0 67.06-30.04 67.06-67.11V0h74.32c0 62.47 50.41 113 113.43 113.84v63.07z"/></svg> TikTok</div>
            </div>
          </div>

          <!-- Result Info Card -->
          <Transition name="slide-up">
            <div v-if="videoInfo" class="w-full max-w-3xl mt-16 z-10 pb-20">
              <div class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-3xl p-6 shadow-[0_0_80px_rgba(0,0,0,0.8)] flex flex-col md:flex-row gap-8 relative overflow-hidden group">
                <!-- Inner glow for the card -->
                <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 blur-[80px] rounded-full pointer-events-none transition-all group-hover:bg-blue-500/10 duration-700"></div>
                
                <div class="relative w-full md:w-[320px] aspect-video rounded-xl overflow-hidden shadow-2xl bg-black shrink-0 border border-white/5 mx-auto">
                  <img :src="videoInfo.thumbnail" class="w-full h-full object-cover transition-transform duration-700 hover:scale-105 opacity-80" />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
                  
                  <!-- Play Button overlay directly on thumbnail -->
                  <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300">
                    <button class="w-16 h-16 rounded-full bg-white/10 backdrop-blur-xl border border-white/20 flex items-center justify-center shadow-2xl hover:scale-110 transition-transform duration-300" @click="openPreview">
                      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="white" d="M8 19V5l11 7l-11 7Z"/></svg>
                    </button>
                  </div>

                  <!-- Duration Badge -->
                  <div v-if="videoInfo.duration" class="absolute bottom-3 right-3 px-2 py-1 bg-black/60 backdrop-blur-md rounded border border-white/10 text-[11px] font-mono font-medium text-white shadow-lg">
                    {{ Math.floor(videoInfo.duration / 60) }}:{{ (videoInfo.duration % 60).toString().padStart(2, '0') }}
                  </div>
                </div>
                
                <div class="flex-1 flex flex-col justify-between py-1 z-10">
                  <div>
                    <div class="flex items-center gap-2 mb-3">
                      <span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded text-[10px] font-bold tracking-widest uppercase">
                        {{ videoInfo.extractor }}
                      </span>
                      <span class="text-zinc-500 text-xs font-medium">Ready to download</span>
                    </div>
                    <h3 class="text-xl md:text-2xl font-bold text-zinc-100 leading-snug line-clamp-2 md:line-clamp-3" :title="videoInfo.title">
                      {{ videoInfo.title }}
                    </h3>
                  </div>
                  
                  <div class="mt-8 flex gap-3">
                    <button class="flex-1 py-3 rounded-xl font-medium text-sm text-zinc-300 bg-white/5 hover:bg-white/10 border border-white/10 transition-colors flex items-center justify-center gap-2" @click="openPreview">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 1 1-18 0a9 9 0 0 1 18 0Z"/><path fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 8l6 4l-6 4V8Z"/></svg>
                      在线预览
                    </button>
                    <!-- Download Button -->
                    <button 
                      class="relative flex-1 group/btn overflow-hidden rounded-xl font-medium text-sm text-black transition-colors flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(255,255,255,0.15)] hover:shadow-[0_0_25px_rgba(255,255,255,0.3)] disabled:opacity-80"
                      :class="downloadStatus === 'completed' ? 'bg-green-400' : 'bg-white'"
                      :disabled="isDownloading && downloadStatus !== 'completed'"
                      @click="startDownload"
                    >
                      <!-- Progress background fill -->
                      <div v-if="isDownloading && downloadStatus !== 'completed'" 
                           class="absolute left-0 top-0 bottom-0 bg-blue-500/20 transition-all duration-300" 
                           :style="{ width: downloadPercent + '%' }">
                      </div>

                      <div v-if="!isDownloading" class="absolute inset-0 bg-gradient-to-r from-transparent via-white/80 to-transparent translate-x-[-100%] group-hover/btn:animate-[shimmer_1.5s_infinite]"></div>
                      
                      <span class="relative z-10 flex items-center justify-center gap-2 w-full h-full py-3">
                        <template v-if="!isDownloading">
                           <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M7 11l5 5l5-5m-5-7v12"/></svg>
                           保存到本地
                        </template>
                        <template v-else-if="downloadStatus === 'downloading' || downloadStatus === 'starting'">
                           <svg class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                           </svg>
                           下载中 {{ downloadPercent }}%
                        </template>
                        <template v-else-if="downloadStatus === 'processing'">
                           <svg class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                           </svg>
                           正在合并音视频...
                        </template>
                        <template v-else-if="downloadStatus === 'completed'">
                           <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path fill="currentColor" opacity="1" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5l1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                           下载完成
                        </template>
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </main>
        
        <!-- Premium Video Modal Backdrop -->
        <n-modal v-model:show="previewVisible" class="w-[95vw] md:w-[85vw] max-w-6xl bg-transparent shadow-none" transform-origin="center">
          <div class="rounded-2xl overflow-hidden bg-black border border-white/10 shadow-[0_0_100px_rgba(0,0,0,1)] relative group">
            <div class="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/80 to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex justify-between items-center pointer-events-none">
                <span class="text-white font-medium drop-shadow-md px-2">{{ videoInfo?.title }}</span>
            </div>
            <video
              id="preview-video"
              controls
              autoplay
              crossorigin="anonymous"
              class="w-full max-h-[85vh] focus:outline-none"
              :src="getBestVideoUrl()"
            ></video>
          </div>
        </n-modal>
        
      </div>
    </n-message-provider>
  </n-config-provider>
</template>

<style>
/* Global CSS variables & keyframes for this specific view */
@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  filter: blur(10px);
}
</style>

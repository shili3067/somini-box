# 🌊 OmniBox (全能极客工具箱)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs" alt="Vue.js">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/TailwindCSS-v4-38B2AC?logo=tailwind-css" alt="Tailwind CSS">
</p>

一款基于 Python 开发的现代化全平台视频下载架构。拥有极简黑金拟物体（Dark Glassmorphism）视觉设计的浏览器内 Web 应用。

支持上百种流媒体网站的视频提取、云端无损音视频合并、在线实时预览以及基于原生浏览器的直接下载机制。

---

## ✨ 核心特性 / Features

1. **🎨 顶级暗黑模式界面 (Premium Web UI)**
   - 采用 **Vue 3 + TailwindCSS v4 + Naive UI** 打造的极其流畅精美、响应式的 Dopamine 毛玻璃黑夜风格界面。
   - 拥有平滑水波下载进度框以及晶体反射动画，带来沉浸式体验。
2. **🔗 极简链接下载 (URL Only)**
   - 全局仅需一行输入框，黏贴 URL（Bilibili, YouTube, Tiktok/抖音, Vimeo 等），系统会自动越过限制进行云端提取。
3. **📺 云端直链全预览 (Live Cloud Preview)**
   - 解析成功后立刻提取出 MP4 及最高清原直链供 HTML5 Native 播放使用，**一秒体验高速视频画质全预览**。
4. **🧠 后端合并 + 原生高速分发流 (Backend Merge & Browser Stream)**
   - 区别于残缺画质提取：所有复杂的最高画质拆分合并都在后端的独立沙盒缓存中靠 **FFmpeg** 并发完成运算。
   - 运算到达 100% 后，采用 **阅后即焚（Background Task Clean）** 技术和 `Content-Disposition` 直接唤醒浏览器官方超速下载弹窗落盘至本地！不再占用电脑一分一毫冗余存储。

---

## 🏗️ 项目架构 / Architecture

采用 **前后端分离 / C-S (Client-Server) 的 Web 环境** 架构设计。
抛弃了沉重的 Electron 等外壳引擎，后台跑接口，直接通过您的浏览器弹出页面交互。

| 模块 | 技术选型 | 说明 |
| --- | --- | --- |
| **前端界面** | Vue 3 + Tailwind CSS V4 | 抛光拟态，提供极为流畅和现代的用户交互体验响应端 |
| **后端驱动** | Python + FastAPI | 全自动跨域允许，处理多线程下载队列及本地文件分发的强劲极速引擎 |
| **解析引擎** | `yt-dlp` | 深度反爬识别、过滤 ANSI 颜色、进行年龄突破及中文释义错误库预装 |
| **运行平台** | OS Native Browser | 使用任何如 Chrome/Edge，一键呼叫即可自动弹出及使用 |

### 核心运作流 (Data Flow)

1. **精准解析阶段**: 过滤所有报错抛错，通过正则获取全格式及标题海报资源。
2. **生成缓存引擎队列**: `前端` ➡️ `启动任务` ➡️ `生成 UUID task_id` ➡️ `后端启动后台进程 Threading 进行下载与合块`
3. **前端状态机全双工轮询**: `Interval 1000ms 探测 /api/download/`，回显极光的进度条百分比与各种下载期状态（下载中 / 正在合并音视频... 等）。
4. **原生分发及毁尸灭迹**: 100% 合并好最终的 MP4 落盘缓存区后，前端接收 `completed` 信号通过流触发 Native `<a>` 点击；由于文件被挂载 FastAPI 后台销毁函数，用户接管最终文件的一刹那，硬盘上的缓存将被彻底清除销毁。

---

## 🚀 安装与一键部署 (Installation & Usage)

### 1. 准备环境 (Prerequisites)

- **Python 3.10+**
- **Node.js 16+** (仅在前端部署阶段使用)
- **FFmpeg** (需加入操作系统的全局环境变量 Path 中，核心音视频合流强依赖)

### 2. 初始化项目

```bash
git clone https://github.com/your-username/OmniBox.git
cd OmniBox

# 后端环境
cd backend
python -m venv venv
venv\Scripts\Activate.ps1   # (如果是 Mac/Linux，请运行 source venv/bin/activate)
pip install -r requirements.txt
pip install -U yt-dlp

# 前端环境
cd ../frontend
npm install
npm run build
```

### 3. 一击必杀启动脚本 (One-Click Start) ⚡

无论在哪儿，在根目录直接打开脚本，自动同时运行后端的 `18000` 端口服务器，并全自动打开您的默认浏览器到 `localhost:5173`。

- **Windows 系统**:
  ```cmd
  .\start.bat
  ```

- **Linux / Mac**:
  ```bash
  ./start.sh
  ```
## 🍏 macOS / Linux 开发与维护

1. `start.sh` 已为 Mac 系统深度优化。由于 macOS 默认未提供旧版本 `python`，脚本将自动探测挂载 `python3`；它同时也包含了原生虚拟环境 `bin/activate` 的探测能力。
2. 退出时脚本利用守护进程模式 `trap`，即便是强杀（`Ctrl + C`）或终端意外退出，后台 Node 挂载进程也绝不会残留。

### 推送至个人远程仓库 (Git Remote Push)
由于该架构属于为您个人定制的纯净版代码体（已处理好纯净的 gitignore）。当您要在 GitHub、GitLab 或 Gitee 建仓追踪它时，请直接执行以下终端命令：

```bash
# 1. 关联您的远程空仓库 (将下面链接替换为您实际建立的远端URL)
git remote add origin https://github.com/您的用户名/您的仓库名.git

# 2. 将主分支强制推送到云端远程仓库备份
git push -u origin master
```

---

## 📝 许可证 / License
基于 [MIT License](LICENSE) 约定，仅供学习、交流使用。请勿用于违背各大协议爬虫法的任何黑市商用以及侵害原版权持有人的使用！

# 📖 星光图书馆 — Galgame 视觉小说

一个基于 **Docker + Flask + PostgreSQL** 的在线视觉小说游戏。

## 🎮 故事简介

神谷凑转学到私立图书馆学园，在图书馆里遇见了两位"书灵"——开朗的星野灯和安静的月之濑静。她们是书本记忆的化身，守护着一本被遗忘的魔法书。你和她们一起修复魔法书，过程中逐渐揭开秘密，也拉近彼此的距离。

- **5 种结局**: 星野结局、月之濑结局、普通结局、坏结局、隐藏结局
- **2 位女主角**: 星野灯（推理小说爱好者）、月之濑静（古典诗歌爱好者）
- **游戏时长**: 约 20 分钟

## 🚀 快速启动

### 前置要求
- Docker & Docker Compose
- Python 3.8+ (仅用于生成占位素材)

### 1. 生成占位素材

```bash
pip install Pillow
python generate_placeholders.py
```

### 2. 启动服务

```bash
docker-compose up -d --build
```

### 3. 开始游戏

打开浏览器访问: **http://localhost**

## 📁 项目结构

```
galgame/
├── docker-compose.yml          # Docker 编排配置
├── init.sql                    # 数据库初始化脚本
├── generate_placeholders.py    # 占位素材生成器
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                  # Flask 后端 (含完整剧本)
├── frontend/
│   ├── index.html              # 游戏主界面
│   ├── style.css               # 视觉样式
│   ├── script.js               # 游戏核心逻辑
│   └── assets/
│       ├── bg/                 # 背景图片
│       ├── character/          # 角色立绘
│       └── audio/              # BGM 和音效
└── nginx/
    └── nginx.conf              # Nginx 反向代理配置
```

## 🎨 替换为真实素材

### 背景图片 (7张)
放到 `frontend/assets/bg/`，文件名:
- `library.jpg`, `library_sunset.jpg`, `bookshelf.jpg`
- `garden.jpg`, `garden_night.jpg`, `library_magic.jpg`, `ending.jpg`

### 角色立绘 (7张)
放到 `frontend/assets/character/`，文件名:
- `hotaru_happy.png`, `hotaru_sad.png`, `hotaru_excited.png`
- `shizuka_normal.png`, `shizuka_sad.png`, `shizuka_happy.png`, `shizuka_blush.png`

### BGM (5首) + 音效 (1个)
放到 `frontend/assets/audio/`，文件名:
- `bgm_normal.mp3`, `spring.mp3`, `hotaru.mp3`, `shizuka.mp3`, `tense.mp3`, `click.mp3`

### 推荐免费素材网站
- **背景**: Pixabay, Unsplash
- **立绘**: Picrew (捏脸生成), Kohaku's Lab
- **BGM**: DOVA-SYNDROME, 魔王魂, Freesound

## 🗄️ 数据库表结构

| 表名 | 说明 |
|------|------|
| `saves` | 玩家存档 (进度、好感度、剧情标记) |
| `choices_stats` | 选项统计 (每个选项被选中的次数) |
| `game_stats` | 全局统计 (总游玩次数、各结局达成数) |

## 🛠️ 技术栈

| 技术 | 作用 |
|------|------|
| Docker Compose | 一键部署全部服务 |
| Nginx | 静态文件服务 + API 反向代理 |
| Flask | 后端 API (剧情管理、存档、统计) |
| PostgreSQL | 数据持久化 (存档、统计) |
| HTML/CSS/JS | 前端 Galgame 界面 |

## 🎯 功能特性

- ✅ 完整 4 章剧情 + 5 种结局
- ✅ 好感度系统 + 剧情分支
- ✅ 存档/读档 (跨设备)
- ✅ 逐字打字动画
- ✅ 自动模式 / 跳过模式
- ✅ BGM 切换 + 音效
- ✅ 角色立绘系统
- ✅ 背景切换动画
- ✅ 全球玩家统计
- ✅ 键盘快捷键 (空格继续, Esc 返回标题)

## ⌨️ 快捷键

| 按键 | 功能 |
|------|------|
| 空格 / 回车 | 推进对话 |
| Esc | 返回标题菜单 |

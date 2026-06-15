// ========== 游戏状态 ==========
const gameState = {
    playerName: '',
    chapter: 0,
    step: 0,
    affectionHotaru: 0,
    affectionShizuka: 0,
    flags: {},
    isAuto: false,
    isSkipping: false,
    autoTimer: null,
    currentLines: [],
    currentChoices: [],
    currentLineIndex: 0,
    currentBg: 'library'
};

// API 基础地址
const API_BASE = '/api';

// BGM 映射 (优先 MP3，不存在则回退到 WAV 占位)
const BGM_MAP = {
    'spring': 'assets/audio/spring.mp3',
    'normal': 'assets/audio/bgm_normal.mp3',
    'hotaru': 'assets/audio/hotaru.mp3',
    'shizuka': 'assets/audio/shizuka.mp3',
    'tense': 'assets/audio/tense.mp3'
};

// WAV 占位回退
const BGM_FALLBACK = {
    'spring': 'assets/audio/spring_placeholder.wav',
    'normal': 'assets/audio/bgm_normal_placeholder.wav',
    'hotaru': 'assets/audio/hotaru_placeholder.wav',
    'shizuka': 'assets/audio/shizuka_placeholder.wav',
    'tense': 'assets/audio/tense_placeholder.wav'
};

// 立绘映射
const SPRITE_MAP = {
    'hotaru_happy': 'assets/character/hotaru_happy.png',
    'hotaru_sad': 'assets/character/hotaru_sad.png',
    'hotaru_excited': 'assets/character/hotaru_excited.png',
    'shizuka_normal': 'assets/character/shizuka_normal.png',
    'shizuka_sad': 'assets/character/shizuka_sad.png',
    'shizuka_happy': 'assets/character/shizuka_happy.png',
    'shizuka_blush': 'assets/character/shizuka_blush.png'
};

// 背景映射
const BG_MAP = {
    'library': 'assets/bg/library.jpg',
    'library_sunset': 'assets/bg/library_sunset.jpg',
    'bookshelf': 'assets/bg/bookshelf.jpg',
    'garden': 'assets/bg/garden.jpg',
    'garden_night': 'assets/bg/garden_night.jpg',
    'library_magic': 'assets/bg/library_magic.jpg',
    'ending': 'assets/bg/ending.jpg'
};

// ========== DOM 元素 ==========
const bgImage = document.getElementById('bg-image');
const spriteLeft = document.getElementById('sprite-left');
const spriteRight = document.getElementById('sprite-right');
const spriteCenter = document.getElementById('sprite-center');
const dialogueBox = document.getElementById('dialogue-box');
const speakerName = document.getElementById('speaker-name');
const messageText = document.getElementById('message-text');
const continueIcon = document.getElementById('continue-icon');
const choicesBox = document.getElementById('choices-box');
const choicesList = document.getElementById('choices-list');
const titleMenu = document.getElementById('title-menu');
const saveLoadMenu = document.getElementById('save-load-menu');
const statsMenu = document.getElementById('stats-menu');
const endingMenu = document.getElementById('ending-menu');
const nameInputArea = document.getElementById('name-input-area');
const bgmPlayer = document.getElementById('bgm-player');
const sePlayer = document.getElementById('se-player');
const affHotaruFill = document.getElementById('aff-hotaru-fill');
const affShizukaFill = document.getElementById('aff-shizuka-fill');
const affHotaruVal = document.getElementById('aff-hotaru-val');
const affShizukaVal = document.getElementById('aff-shizuka-val');

// ========== 工具函数 ==========
function playSE() {
    sePlayer.currentTime = 0;
    sePlayer.play().catch(() => {});
}

function changeBGM(bgmKey) {
    const url = BGM_MAP[bgmKey] || BGM_MAP['normal'];
    if (bgmPlayer.src && bgmPlayer.src.includes(bgmKey)) return;

    // 尝试 MP3
    bgmPlayer.src = url;
    bgmPlayer.play().catch(() => {
        // 回退到 WAV 占位
        const fallback = BGM_FALLBACK[bgmKey];
        if (fallback) {
            bgmPlayer.src = fallback;
            bgmPlayer.play().catch(() => {});
        }
    });
}

function changeBG(bgKey) {
    const url = BG_MAP[bgKey] || BG_MAP['library'];
    if (bgImage.src && bgImage.src.endsWith(url.split('/').pop())) return;
    bgImage.style.opacity = '0';
    setTimeout(() => {
        bgImage.src = url;
        bgImage.style.opacity = '1';
    }, 400);
    gameState.currentBg = bgKey;
}

function setSprite(spriteKey, position) {
    const url = SPRITE_MAP[spriteKey];
    const spriteMap = { 'left': spriteLeft, 'right': spriteRight, 'center': spriteCenter };

    // 隐藏所有立绘
    [spriteLeft, spriteRight, spriteCenter].forEach(el => {
        if (el.src && !el.classList.contains('hidden')) {
            el.style.opacity = '0';
        }
    });

    if (!url) {
        setTimeout(() => {
            [spriteLeft, spriteRight, spriteCenter].forEach(el => el.classList.add('hidden'));
        }, 300);
        return;
    }

    // 显示目标立绘
    const target = spriteMap[position] || spriteCenter;
    target.src = url;
    target.classList.remove('hidden');
    // 强制回流后设置透明度
    void target.offsetWidth;
    target.style.opacity = '1';

    // 隐藏不需要的
    Object.entries(spriteMap).forEach(([pos, el]) => {
        if (el !== target) {
            el.classList.add('hidden');
        }
    });
}

function hideSprites() {
    [spriteLeft, spriteRight, spriteCenter].forEach(el => {
        el.classList.add('hidden');
        el.style.opacity = '0';
    });
}

function updateAffectionDisplay() {
    affHotaruFill.style.width = Math.min(gameState.affectionHotaru / 12 * 100, 100) + '%';
    affShizukaFill.style.width = Math.min(gameState.affectionShizuka / 12 * 100, 100) + '%';
    affHotaruVal.textContent = gameState.affectionHotaru;
    affShizukaVal.textContent = gameState.affectionShizuka;
}

// ========== 保存/加载 ==========
async function saveGame() {
    if (!gameState.playerName) return;

    const saveData = {
        player_name: gameState.playerName,
        chapter: gameState.chapter,
        step: gameState.step,
        hotaru: gameState.affectionHotaru,
        shizuka: gameState.affectionShizuka,
        flags: gameState.flags
    };

    try {
        const res = await fetch(`${API_BASE}/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(saveData)
        });
        if (res.ok) {
            showTemporaryMessage('💾 存档成功！');
            playSE();
        }
    } catch (e) {
        console.error('保存失败:', e);
        showTemporaryMessage('⚠️ 存档失败，请检查网络连接');
    }
}

async function loadGame(playerName) {
    try {
        const res = await fetch(`${API_BASE}/load/${encodeURIComponent(playerName)}`);
        const data = await res.json();

        if (data.exists) {
            gameState.playerName = playerName;
            gameState.chapter = data.chapter;
            gameState.step = data.step;
            gameState.affectionHotaru = data.hotaru;
            gameState.affectionShizuka = data.shizuka;
            gameState.flags = data.flags || {};

            updateAffectionDisplay();
            await fetchScript();
            hideAllMenus();
            showDialogueBox();
            document.getElementById('control-bar').classList.remove('hidden');
            return true;
        }
        return false;
    } catch (e) {
        console.error('加载失败:', e);
        return false;
    }
}

async function newGame(playerName) {
    try {
        const res = await fetch(`${API_BASE}/new_game`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_name: playerName })
        });

        if (res.ok) {
            gameState.playerName = playerName;
            gameState.chapter = 0;
            gameState.step = 0;
            gameState.affectionHotaru = 0;
            gameState.affectionShizuka = 0;
            gameState.flags = {};

            updateAffectionDisplay();
            await fetchScript();
            hideAllMenus();
            showDialogueBox();
            document.getElementById('control-bar').classList.remove('hidden');
            document.getElementById('affection-display').classList.remove('hidden');
            return true;
        }
        return false;
    } catch (e) {
        console.error('新游戏失败:', e);
        return false;
    }
}

// ========== 获取剧情脚本 ==========
async function fetchScript() {
    try {
        const res = await fetch(`${API_BASE}/script`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chapter: gameState.chapter,
                step: gameState.step,
                hotaru: gameState.affectionHotaru,
                shizuka: gameState.affectionShizuka,
                flags: gameState.flags
            })
        });

        const data = await res.json();

        if (data.type === 'ending') {
            showEnding(data.ending_id, data.ending_text);
            return;
        }

        if (data.type === 'scene') {
            gameState.currentLines = data.lines || [];
            gameState.currentChoices = data.choices || [];
            gameState.currentLineIndex = 0;

            changeBG(data.bg);

            if (gameState.currentLines.length > 0) {
                displayCurrentLine();
            } else if (gameState.currentChoices.length > 0) {
                showChoices();
            }
            return;
        }

        // 错误处理
        console.error('未知的脚本响应:', data);
        messageText.innerText = '剧情加载出错，请刷新页面重试。';
    } catch (e) {
        console.error('获取脚本失败:', e);
        messageText.innerText = '连接服务器失败，请确认后端已启动。';
    }
}

function displayCurrentLine() {
    if (gameState.currentLineIndex >= gameState.currentLines.length) {
        // 当前场景行结束了
        if (gameState.currentChoices.length > 0) {
            showChoices();
        }
        return;
    }

    const line = gameState.currentLines[gameState.currentLineIndex];

    // 说话人映射
    const speakerMap = { 'system': '📖 旁白', 'Minato': '神谷凑', 'Hotaru': '星野灯', 'Shizuka': '月之濑静' };
    speakerName.innerText = speakerMap[line.speaker] || line.speaker;

    // 逐字显示
    typewriterEffect(line.text);

    // 立绘
    if (line.sprite) {
        setSprite(line.sprite, line.position || 'center');
    } else {
        switch (line.speaker) {
            case 'Hotaru':
                setSprite('hotaru_happy', 'right');
                break;
            case 'Shizuka':
                setSprite('shizuka_normal', 'left');
                break;
            default:
                hideSprites();
        }
    }

    // BGM
    if (line.bgm) {
        changeBGM(line.bgm);
    }
}

let typewriterTimeout = null;
let currentTyping = false;

function typewriterEffect(text) {
    if (typewriterTimeout) clearTimeout(typewriterTimeout);
    currentTyping = true;
    continueIcon.classList.add('hidden');

    messageText.innerText = '';
    let i = 0;
    const speed = gameState.isSkipping ? 5 : 40;

    function type() {
        if (i < text.length) {
            messageText.innerText += text[i];
            i++;
            typewriterTimeout = setTimeout(type, speed);
        } else {
            currentTyping = false;
            continueIcon.classList.remove('hidden');
        }
    }

    type();
}

function nextLine() {
    if (currentTyping) {
        // 跳过打字动画
        if (typewriterTimeout) clearTimeout(typewriterTimeout);
        const line = gameState.currentLines[gameState.currentLineIndex];
        if (line) messageText.innerText = line.text;
        currentTyping = false;
        continueIcon.classList.remove('hidden');
        return;
    }

    playSE();
    gameState.currentLineIndex++;
    displayCurrentLine();
}

function showChoices() {
    dialogueBox.classList.add('hidden');
    choicesBox.classList.remove('hidden');
    choicesList.innerHTML = '';

    gameState.currentChoices.forEach(choice => {
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.innerText = choice.text;
        btn.addEventListener('click', () => selectChoice(choice));
        choicesList.appendChild(btn);
    });
}

async function selectChoice(choice) {
    playSE();

    // 记录选择统计
    fetch(`${API_BASE}/choice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice_id: choice.id })
    }).catch(() => {});

    // 应用好感度效果
    if (choice.effects) {
        if (choice.effects.hotaru) {
            gameState.affectionHotaru = Math.max(0, gameState.affectionHotaru + choice.effects.hotaru);
        }
        if (choice.effects.shizuka) {
            gameState.affectionShizuka = Math.max(0, gameState.affectionShizuka + choice.effects.shizuka);
        }
    }

    // 记录关键选项
    if (['chap3_1', 'chap3_2', 'chap3_3', 'chap3_4'].includes(choice.id)) {
        gameState.flags.final_choice = choice.id;
    }

    updateAffectionDisplay();

    // 更新章节
    gameState.chapter = choice.next_chapter;
    gameState.step = choice.next_step;

    // 自动存档
    await saveGame();

    // 获取新脚本
    choicesBox.classList.add('hidden');
    dialogueBox.classList.remove('hidden');
    await fetchScript();
}

// ========== 自动模式 ==========
function startAutoMode() {
    stopAutoMode();
    gameState.isAuto = true;

    gameState.autoTimer = setInterval(() => {
        if (!gameState.isAuto) return;
        if (!currentTyping && dialogueBox.classList.contains('hidden') === false) {
            if (gameState.currentLineIndex < gameState.currentLines.length) {
                nextLine();
            }
        }
    }, 2500);
}

function stopAutoMode() {
    if (gameState.autoTimer) {
        clearInterval(gameState.autoTimer);
        gameState.autoTimer = null;
    }
    gameState.isAuto = false;
}

// ========== 界面控制 ==========
function showDialogueBox() {
    dialogueBox.classList.remove('hidden');
    choicesBox.classList.add('hidden');
}

function hideAllMenus() {
    titleMenu.classList.add('hidden');
    saveLoadMenu.classList.add('hidden');
    statsMenu.classList.add('hidden');
    endingMenu.classList.add('hidden');
}

function showTemporaryMessage(msg) {
    const originalText = messageText.innerText;
    messageText.innerText = msg;
    setTimeout(() => {
        if (!currentTyping && dialogueBox.classList.contains('hidden') === false) {
            messageText.innerText = originalText;
        }
    }, 1500);
}

// ========== 全局统计 ==========
async function showGlobalStats() {
    try {
        const res = await fetch(`${API_BASE}/stats`);
        const data = await res.json();
        const statsDiv = document.getElementById('stats-content');

        let endingsHtml = '';
        if (data.total_endings) {
            const endingNames = {
                'hotaru': '🌟 星野灯结局',
                'shizuka': '📖 月之濑静结局',
                'normal': '🌸 普通结局',
                'bad': '💔 坏结局',
                'hidden': '✨ 隐藏结局'
            };
            endingsHtml = '<h3>🏆 结局达成分布</h3><ul>';
            for (const [key, name] of Object.entries(endingNames)) {
                const count = (typeof data.total_endings === 'object') ? (data.total_endings[key] || 0) : 0;
                endingsHtml += `<li>${name} — ${count} 次</li>`;
            }
            endingsHtml += '</ul>';
        }

        statsDiv.innerHTML = `
            <p>📊 总游玩次数: <strong>${data.total_plays}</strong></p>
            ${endingsHtml}
            <h3>📝 选项人气排行</h3>
            <ul style="margin-top:10px;">
                ${data.choices_stats.map(c => `<li>${c.choice_text} — 被选了 <strong>${c.selected_count}</strong> 次</li>`).join('')}
            </ul>
        `;

        statsMenu.classList.remove('hidden');
    } catch (e) {
        console.error('获取统计失败:', e);
        document.getElementById('stats-content').innerHTML = '<p>⚠️ 获取统计失败，请确认后端已启动</p>';
        statsMenu.classList.remove('hidden');
    }
}

// ========== 结局 ==========
function showEnding(endingId, endingText) {
    stopAutoMode();
    hideAllMenus();

    const endingTitles = {
        'hotaru': '🌟 星野灯结局',
        'shizuka': '📖 月之濑静结局',
        'normal': '🌸 普通结局',
        'bad': '💔 坏结局',
        'hidden': '✨ 隐藏结局 · 星光永恒'
    };

    document.getElementById('ending-title').innerText = endingTitles[endingId] || '结局';
    document.getElementById('ending-text').innerText = endingText;
    endingMenu.classList.remove('hidden');
    dialogueBox.classList.add('hidden');
    choicesBox.classList.add('hidden');
    document.getElementById('affection-display').classList.add('hidden');

    changeBGM(endingId === 'bad' ? 'tense' : 'spring');
    changeBG('ending');
}

// ========== 事件绑定 ==========
// 点击对话框推进
dialogueBox.addEventListener('click', (e) => {
    // 防止触发按钮点击
    if (e.target.closest('button')) return;
    if (gameState.isAuto) {
        stopAutoMode();
        document.getElementById('auto-btn').innerHTML = '▶ 自动';
    }
    nextLine();
});

// 键盘操作
document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case ' ':
        case 'Enter':
            e.preventDefault();
            if (dialogueBox.classList.contains('hidden') === false) {
                if (gameState.isAuto) {
                    stopAutoMode();
                    document.getElementById('auto-btn').innerHTML = '▶ 自动';
                }
                nextLine();
            }
            break;
        case 'Escape':
            if (!titleMenu.classList.contains('hidden')) return;
            stopAutoMode();
            hideAllMenus();
            titleMenu.classList.remove('hidden');
            dialogueBox.classList.add('hidden');
            choicesBox.classList.add('hidden');
            break;
    }
});

// 自动模式
document.getElementById('auto-btn').addEventListener('click', () => {
    if (gameState.isAuto) {
        stopAutoMode();
        document.getElementById('auto-btn').innerHTML = '▶ 自动';
    } else {
        startAutoMode();
        document.getElementById('auto-btn').innerHTML = '⏸ 停止';
    }
    playSE();
});

// 存档
document.getElementById('save-btn').addEventListener('click', () => {
    saveGame();
});

// 快速读档
document.getElementById('load-quick-btn').addEventListener('click', async () => {
    if (gameState.playerName) {
        const success = await loadGame(gameState.playerName);
        if (!success) {
            showTemporaryMessage('⚠️ 读档失败');
        }
    }
    playSE();
});

// 返回标题
document.getElementById('title-btn').addEventListener('click', () => {
    stopAutoMode();
    hideAllMenus();
    titleMenu.classList.remove('hidden');
    dialogueBox.classList.add('hidden');
    choicesBox.classList.add('hidden');
    hideSprites();
    playSE();
});

// BGM 开关
let bgmMuted = false;
document.getElementById('bgm-toggle').addEventListener('click', () => {
    bgmMuted = !bgmMuted;
    bgmPlayer.muted = bgmMuted;
    document.getElementById('bgm-toggle').innerHTML = bgmMuted ? '🔇 BGM' : '🔊 BGM';
});

// 跳过模式
const skipBtn = document.getElementById('skip-btn');
let skipInterval = null;
skipBtn.addEventListener('click', () => {
    gameState.isSkipping = !gameState.isSkipping;
    if (gameState.isSkipping) {
        skipInterval = setInterval(() => {
            if (!gameState.isSkipping) return;
            if (!currentTyping && dialogueBox.classList.contains('hidden') === false) {
                if (gameState.currentLineIndex < gameState.currentLines.length) {
                    nextLine();
                }
            }
        }, 80);
        skipBtn.innerHTML = '⏹ 停止';
    } else {
        if (skipInterval) clearInterval(skipInterval);
        skipBtn.innerHTML = '⏩ 跳过';
    }
    playSE();
});

// ========== 标题菜单事件 ==========
document.getElementById('new-game-btn').addEventListener('click', () => {
    nameInputArea.classList.remove('hidden');
    document.getElementById('new-game-btn').style.display = 'none';
    document.getElementById('player-name').focus();
});

document.getElementById('confirm-name-btn').addEventListener('click', async () => {
    const name = document.getElementById('player-name').value.trim();
    if (!name) {
        alert('请输入你的名字');
        return;
    }
    const success = await newGame(name);
    nameInputArea.classList.add('hidden');
    document.getElementById('new-game-btn').style.display = 'block';
    document.getElementById('player-name').value = '';
    if (!success) {
        alert('创建新游戏失败，请确认后端已启动');
    }
});

// 回车确认名字
document.getElementById('player-name').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('confirm-name-btn').click();
    }
});

document.getElementById('load-game-btn').addEventListener('click', async () => {
    const name = prompt('请输入你的存档名字：');
    if (name) {
        const success = await loadGame(name.trim());
        if (!success) {
            alert('没有找到该名字的存档');
        }
    }
});

document.getElementById('stats-btn').addEventListener('click', () => {
    showGlobalStats();
});

document.getElementById('close-stats-btn').addEventListener('click', () => {
    statsMenu.classList.add('hidden');
});

document.getElementById('close-save-menu').addEventListener('click', () => {
    saveLoadMenu.classList.add('hidden');
});

document.getElementById('ending-return-btn').addEventListener('click', () => {
    endingMenu.classList.add('hidden');
    titleMenu.classList.remove('hidden');
    hideSprites();
    changeBG('library');
    document.getElementById('affection-display').classList.add('hidden');
    document.getElementById('control-bar').classList.add('hidden');
});

// ========== 初始化 ==========
function init() {
    changeBG('library');
    hideSprites();
    bgmPlayer.volume = 0.5;

    // 初始隐藏游戏UI
    document.getElementById('control-bar').classList.add('hidden');
    document.getElementById('affection-display').classList.add('hidden');
    dialogueBox.classList.add('hidden');

    // 显示标题菜单
    titleMenu.classList.remove('hidden');
}

init();

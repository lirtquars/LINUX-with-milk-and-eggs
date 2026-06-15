-- 玩家存档表
CREATE TABLE IF NOT EXISTS saves (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    current_chapter INTEGER DEFAULT 1,
    current_step INTEGER DEFAULT 0,
    affection_hotaru INTEGER DEFAULT 0,
    affection_shizuka INTEGER DEFAULT 0,
    flags JSON DEFAULT '{}',
    ending_unlocked VARCHAR(50),
    last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 选项统计表
CREATE TABLE IF NOT EXISTS choices_stats (
    choice_id VARCHAR(50) PRIMARY KEY,
    choice_text TEXT,
    selected_count INTEGER DEFAULT 0
);

-- 全局进度统计
CREATE TABLE IF NOT EXISTS game_stats (
    id INTEGER PRIMARY KEY DEFAULT 1,
    total_plays INTEGER DEFAULT 0,
    total_endings JSON DEFAULT '{}'
);

-- 插入初始统计记录
INSERT INTO game_stats (id, total_plays, total_endings)
VALUES (1, 0, '{"hotaru": 0, "shizuka": 0, "normal": 0, "bad": 0, "hidden": 0}')
ON CONFLICT (id) DO NOTHING;

-- 插入选项初始数据
INSERT INTO choices_stats (choice_id, choice_text, selected_count) VALUES
('prologue_1', '「你好，我叫神谷凑」', 0),
('prologue_2', '「...不好意思打扰了」', 0),
('chap1_1', '「我也喜欢推理小说！」', 0),
('chap1_2', '「推理小说有点难懂呢...」', 0),
('chap1_3', '「能给我推荐一本吗？」', 0),
('chap2_1', '「这首诗很美...能教我读吗？」', 0),
('chap2_2', '「我更喜欢现代诗」', 0),
('chap2_3', '「诗歌太难了，我可能学不会」', 0),
('chap3_1', '「我想留在这里」', 0),
('chap3_2', '「我想带你们一起离开」', 0),
('chap3_3', '「我还没想好...」', 0),
('chap3_4', '「图书馆是我永远的家」', 0)
ON CONFLICT (choice_id) DO NOTHING;

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import json

app = Flask(__name__)
CORS(app)


def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        database=os.environ.get('DB_NAME', 'galgame_db'),
        user=os.environ.get('DB_USER', 'galgame_user'),
        password=os.environ.get('DB_PASSWORD', 'galgame_pass')
    )


# ========== 剧情脚本 ==========
# 完整剧本：序章 + 4章（每章含子场景） + 结局判断
SCRIPT = {
    0: {  # 序章
        "bg": "library",
        "lines": [
            {"speaker": "system", "text": "四月，樱花飘落的季节。", "bgm": "spring"},
            {"speaker": "system", "text": "神谷凑转学到了这所历史悠久的私立图书馆学园。", "bgm": "spring"},
            {"speaker": "system", "text": "他听说学校的图书馆里藏着什么秘密...", "bgm": "spring"},
            {"speaker": "Minato", "text": "这里就是图书馆吗...好大。", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "欢迎光临～！你是新来的学生吗？", "bgm": "hotaru", "sprite": "hotaru_happy"},
            {"speaker": "Minato", "text": "啊、是的...我叫神谷凑。抱歉打扰你们了。", "bgm": "normal"},
            {"speaker": "Shizuka", "text": "...又有人来了呢。", "bgm": "shizuka", "sprite": "shizuka_normal"},
            {"speaker": "Hotaru", "text": "我是星野灯！她是月之濑静。我们是这里的...嗯，图书管理员！", "bgm": "hotaru",
             "sprite": "hotaru_happy"},
            {"speaker": "Minato", "text": "请多关照。", "bgm": "normal"}
        ],
        "choices": [
            {"id": "prologue_1", "text": "「你好，我叫神谷凑」(热情回应)", "next_chapter": 1, "next_step": 0,
             "effects": {"hotaru": 1}},
            {"id": "prologue_2", "text": "「...不好意思打扰了」(礼貌但保持距离)", "next_chapter": 1, "next_step": 0,
             "effects": {"shizuka": 1}}
        ]
    },
    1: {  # 第一章 - 与星野灯的推理冒险
        "bg": "library_sunset",
        "lines": [
            {"speaker": "Hotaru", "text": "凑君！你知道吗？这间图书馆里有一本传说中的魔法书。", "bgm": "hotaru",
             "sprite": "hotaru_excited"},
            {"speaker": "Minato", "text": "魔法书？", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "嗯！据说读懂它的人可以实现一个愿望。而且——", "bgm": "hotaru",
             "sprite": "hotaru_happy"},
            {"speaker": "Hotaru", "text": "它被藏在推理小说区的某个角落！我们一起去找吧！", "bgm": "hotaru",
             "sprite": "hotaru_excited"},
            {"speaker": "Minato", "text": "听起来很有趣。不过为什么找我？", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "因为你看上去很聪明呀～而且一个人找太寂寞了嘛。", "bgm": "hotaru",
             "sprite": "hotaru_happy"}
        ],
        "choices": [
            {"id": "chap1_1", "text": "「我也喜欢推理小说！让我们解开这个谜题」(热血)", "next_chapter": 1, "next_step": 1,
             "effects": {"hotaru": 3}},
            {"id": "chap1_2", "text": "「推理小说有点难懂呢...不过我愿意试试」(诚实)", "next_chapter": 1, "next_step": 1,
             "effects": {"hotaru": 2}},
            {"id": "chap1_3", "text": "「能给我推荐一本入门推理小说吗？」(谦虚)", "next_chapter": 1, "next_step": 1,
             "effects": {"hotaru": 1, "shizuka": 1}}
        ]
    },
    1.1: {  # 第一章后续 - 与灯一起探索
        "bg": "bookshelf",
        "lines": [
            {"speaker": "Hotaru", "text": "太好了！跟我来，我知道推理小说区在哪里～", "bgm": "hotaru",
             "sprite": "hotaru_happy"},
            {"speaker": "System", "text": "灯拉着凑的袖子，穿过一排排高耸的书架。午后的阳光透过彩色玻璃洒下来，在地板上照出斑斓的光斑。", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "你看这里——《福尔摩斯探案集》《东方快车谋杀案》《占星术杀人魔法》...", "bgm": "hotaru",
             "sprite": "hotaru_excited"},
            {"speaker": "Hotaru", "text": "每一本我都读过至少三遍哦！", "bgm": "hotaru", "sprite": "hotaru_happy"},
            {"speaker": "Minato", "text": "你对这里真的很熟悉。在这里...待了很久吗？", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "嗯...很久很久。", "bgm": "hotaru", "sprite": "hotaru_sad"},
            {"speaker": "System", "text": "灯的笑容一瞬间黯淡了下来。但很快她又恢复了活力。", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "啊！不说这个了。我发现那本魔法书就在推理区最深处——但我们得先解开一个谜题！", "bgm": "hotaru",
             "sprite": "hotaru_excited"}
        ],
        "choices": [
            {"id": "chap1_next", "text": "「什么谜题？让我试试」", "next_chapter": 2, "next_step": 0, "effects": {}}
        ]
    },
    2: {  # 第二章 - 与月之濑静的诗歌时光
        "bg": "garden",
        "lines": [
            {"speaker": "System", "text": "第二天放学后，凑来到图书馆后面的庭院。夕阳下，月之濑静坐在一棵老樱花树下，膝上放着一本泛黄的书。", "bgm": "shizuka"},
            {"speaker": "Shizuka", "text": "...凑君。", "bgm": "shizuka", "sprite": "shizuka_normal"},
            {"speaker": "Minato", "text": "静同学，你在读什么？", "bgm": "normal"},
            {"speaker": "Shizuka", "text": "一本...很古老的诗集。里面有些诗句...我看不懂。", "bgm": "shizuka", "sprite": "shizuka_sad"},
            {"speaker": "Shizuka", "text": "不，应该说...我能读懂文字，但不懂它想传达的感情。", "bgm": "shizuka", "sprite": "shizuka_normal"},
            {"speaker": "Minato", "text": "诗不只是文字，也是作者的心情。你想理解的是什么？", "bgm": "normal"},
            {"speaker": "Shizuka", "text": '...我想理解，她顿了顿，什么是"思念"。', "bgm": "shizuka", "sprite": "shizuka_blush"}
        ],
        "choices": [
            {"id": "chap2_1", "text": "「这首诗很美...能教我读吗？我们一起感受」(温柔)", "next_chapter": 2, "next_step": 1,
             "effects": {"shizuka": 3}},
            {"id": "chap2_2", "text": "「我更喜欢现代诗。不过或许可以试着理解古老的韵律」(理性)", "next_chapter": 2, "next_step": 1,
             "effects": {"shizuka": 1, "hotaru": 1}},
            {"id": "chap2_3", "text": "「诗歌太难了，我可能学不会」(退缩)", "next_chapter": 2, "next_step": 1,
             "effects": {"shizuka": -1}}
        ]
    },
    2.1: {  # 第二章后续 - 月光下的诗会
        "bg": "garden_night",
        "lines": [
            {"speaker": "System", "text": "夜幕降临，月光洒在庭院中。静轻轻翻开诗集，开始低声诵读。", "bgm": "shizuka"},
            {"speaker": "Shizuka", "text": "\"银河倾泻入窗来，照亮了未完成的信纸...我们在时间里对视，比星辰更沉默。\"", "bgm": "shizuka",
             "sprite": "shizuka_happy"},
            {"speaker": "Minato", "text": "好美的诗句。是在说等待某人吗？", "bgm": "normal"},
            {"speaker": "Shizuka", "text": "...你看出来了。", "bgm": "shizuka", "sprite": "shizuka_blush"},
            {"speaker": "Shizuka", "text": "这本诗集属于图书馆的创建者。据说他在等一个不会再回来的人。", "bgm": "shizuka",
             "sprite": "shizuka_sad"},
            {"speaker": "Shizuka", "text": "他把所有的思念都写进了这些诗里。但诗歌没有填满空白，只是让空白的形状变得清晰。", "bgm": "shizuka",
             "sprite": "shizuka_normal"},
            {"speaker": "Minato", "text": "那他的思念被听见了吗？", "bgm": "normal"},
            {"speaker": "Shizuka", "text": "...现在被你听见了。", "bgm": "shizuka", "sprite": "shizuka_happy"}
        ],
        "choices": [
            {"id": "chap2_next", "text": "「谢谢你让我听到这些」", "next_chapter": 3, "next_step": 0,
             "effects": {"shizuka": 1, "hotaru": 1}}
        ]
    },
    3: {  # 第三章 - 魔法书的真相
        "bg": "library_magic",
        "lines": [
            {"speaker": "System", "text": "经过几天的探索，凑和两位书灵终于找到了那本传说中的魔法书。它安放在图书馆最深处的玻璃柜中，书页闪烁着微弱的金色光芒。", "bgm": "tense"},
            {"speaker": "Hotaru", "text": "找到了！这就是传说中的魔法书——《群星之忆》！", "bgm": "hotaru", "sprite": "hotaru_excited"},
            {"speaker": "Shizuka", "text": "...但书页是空白的。一个字也没有。", "bgm": "shizuka", "sprite": "shizuka_sad"},
            {"speaker": "Minato", "text": "怎么会这样？传说是假的吗？", "bgm": "normal"},
            {"speaker": "Hotaru", "text": "不...我感觉到它在呼吸。它需要什么来激活。", "bgm": "hotaru", "sprite": "hotaru_sad"},
            {"speaker": "Shizuka", "text": "...需要记忆。这本书记录着图书馆里所有人的记忆。", "bgm": "shizuka", "sprite": "shizuka_normal"},
            {"speaker": "System", "text": "灯和静对视了一眼，表情变得复杂。", "bgm": "tense"},
            {"speaker": "Hotaru", "text": "凑君...我们有件事要告诉你。", "bgm": "hotaru", "sprite": "hotaru_sad"},
            {"speaker": "Hotaru", "text": "我们...不是人类。我们是这本魔法书创造出来的——书灵。", "bgm": "hotaru", "sprite": "hotaru_sad"},
            {"speaker": "Shizuka", "text": "我们存在的原因，就是守护这些被遗忘的记忆和故事。但是...", "bgm": "shizuka",
             "sprite": "shizuka_sad"},
            {"speaker": "Shizuka", "text": "如果魔法书被完全修复，作为书灵的我们...可能会消失。", "bgm": "shizuka", "sprite": "shizuka_sad"},
            {"speaker": "Minato", "text": "！", "bgm": "tense"},
            {"speaker": "System", "text": "凑的心脏猛地一沉。他看着灯和静——她们的表情里有期待，也有恐惧。", "bgm": "tense"}
        ],
        "choices": [
            {"id": "chap3_1", "text": "「我想留在这里——和你们一起守护图书馆」(坚定)", "next_chapter": 4, "next_step": 0,
             "effects": {"hotaru": 4, "shizuka": 4}},
            {"id": "chap3_2", "text": "「我想带你们一起离开，去看看外面的世界」(勇敢)", "next_chapter": 4, "next_step": 0,
             "effects": {"hotaru": 2, "shizuka": 2}},
            {"id": "chap3_3", "text": "「我还没想好...给我一点时间」(犹豫)", "next_chapter": 4, "next_step": 0,
             "effects": {"hotaru": -1, "shizuka": -1}},
            {"id": "chap3_4", "text": "「图书馆是我永远的家——我们一起写新的故事」(深情)", "next_chapter": 4, "next_step": 0,
             "effects": {"hotaru": 5, "shizuka": 5}}
        ]
    }
}

# 隐藏结局特殊条件标记
HIDDEN_ENDING_FLAG = {"chap3_4"}


# ========== 结局判断函数 ==========
def determine_ending(hotaru, shizuka, flags):
    total = hotaru + shizuka
    final_choice = flags.get("final_choice", "")
    read_all = flags.get("read_all_chapters", False)

    # 隐藏结局：选了chap3_4 + 总好感≥8 + 读完全部章节
    if final_choice in HIDDEN_ENDING_FLAG and total >= 8 and read_all:
        return "hidden", (
            "✨ 隐藏结局 · 星光永恒 ✨\n\n"
            "魔法书突然迸发出璀璨的光芒。\n"
            "书页不再是空白的——上面浮现出你在图书馆的每一天：\n"
            "和灯的推理冒险、和静的诗会、三人一起读书的时光...\n\n"
            "\"原来如此，\"灯轻轻说，\"书不是需要修复的东西。它需要的是——故事。\"\n"
            "\"...我们的故事。\"静微笑着补充。\n\n"
            "魔法书不需要用记忆来填补——它需要的是创造新的记忆。\n"
            "书灵们不会消失，因为她们已经成为了新故事的一部分。\n\n"
            "你和两位书灵共同成为了图书馆的守护者。\n"
            "图书馆不再是收藏遗忘的地方，而是一个创造回忆的家。\n\n"
            "——你们的羁绊，超越了时间的书页。\n"
            "——在新的故事里，永远在一起。"
        )

    # 星野结局
    if hotaru >= 10 and hotaru > shizuka + 2:
        return "hotaru", (
            "🌟 星野灯结局 · 灯火阑珊 🌟\n\n"
            "魔法书的书页终于浮现出一行字：\n"
            "\"灯火将永远照亮这座图书馆。\"\n\n"
            "灯没有消失。相反——她变得比以往更加明亮。\n"
            "真正让一个角色活着的，不是魔法，而是被一个人真诚地记住。\n\n"
            "神谷凑和星野灯一起成为了图书馆的管理员。\n"
            "每天放学后，他们会窝在推理小说区的角落。\n"
            "灯总是指着一本新书说：\n"
            "\"凑君！这本谜题超难！我们一起解开它！\"\n\n"
            "推理小说区的灯，永远亮着。\n"
            "不是魔法，而是因为——有人为她点亮了。"
        )

    # 月之濑结局
    if shizuka >= 10 and shizuka > hotaru + 2:
        return "shizuka", (
            "📖 月之濑静结局 · 静夜诗 📖\n\n"
            "魔法书的书页终于浮现出一行字：\n"
            "\"诗歌将永远留在这个庭院。\"\n\n"
            "静的轮廓没有变得透明。相反——她的声音第一次变得清晰有力。\n"
            "被听见，是最深的理解。被记住，是最长久的陪伴。\n\n"
            "神谷凑和月之濑静一起在图书馆的诗歌区整理诗集。\n"
            "偶尔他会偷偷看静，发现静也在偷偷看他。\n"
            "然后他们相视一笑，重新埋首于诗句之间。\n\n"
            "那个夜晚的诗歌，依然在月光下回响。\n"
            "\"...谢谢。\"静轻声说。\n"
            "\"谢谢你听了我的诗。\""
        )

    # 普通结局
    if total >= 5:
        return "normal", (
            "🌸 普通结局 · 朋友 🌸\n\n"
            "魔法书被修复了一部分，书页上浮现出模糊的字迹。\n"
            "书灵们没有消失，但她们的力量变弱了一些。\n\n"
            "你和星野灯、月之濑静成为了很好的朋友。\n"
            "你们经常在图书馆一起读书、讨论。\n"
            "灯为你们推荐新的推理小说，静为你们朗诵新的诗歌。\n\n"
            "魔法书最终被收藏在书架的最高处。\n"
            "它还没有被完全解开——\n"
            "但你已经拥有了比魔法更珍贵的东西：友谊。\n\n"
            "也许下次——你能做出更勇敢的选择。"
        )

    # 坏结局
    return "bad", (
        "💔 坏结局 · 遗忘之书 💔\n\n"
        "魔法书渐渐变得透明。\n"
        "书灵们的轮廓也开始模糊。\n\n"
        "\"对不起...\"灯的声音变得遥远。\n"
        "\"...没关系。\"静的最后一句话被风吹散了。\n\n"
        "当你再次走进图书馆时，推理小说区空无一人。\n"
        "庭院里的樱花树下，诗集安静地合着。\n\n"
        "书页上没有任何字。\n"
        "魔法需要记忆才能存在。\n"
        "而有些记忆——一旦错过，就真的失去了。\n\n"
        "没有人再叫出你的名字。"
    )


# ========== API 路由 ==========

@app.route('/api/save', methods=['POST'])
def save_game():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    # 检查是否已存在该玩家的存档
    cur.execute("SELECT id FROM saves WHERE player_name = %s", (data['player_name'],))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE saves SET
                current_chapter = %s, current_step = %s,
                affection_hotaru = %s, affection_shizuka = %s,
                flags = %s, last_played = NOW()
            WHERE player_name = %s
        """, (
            data['chapter'], data['step'],
            data['hotaru'], data['shizuka'],
            json.dumps(data.get('flags', {})),
            data['player_name']
        ))
    else:
        cur.execute("""
            INSERT INTO saves (player_name, current_chapter, current_step,
                              affection_hotaru, affection_shizuka, flags)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['player_name'], data['chapter'], data['step'],
            data['hotaru'], data['shizuka'],
            json.dumps(data.get('flags', {}))
        ))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "ok"})


@app.route('/api/load/<player_name>', methods=['GET'])
def load_game(player_name):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM saves WHERE player_name = %s", (player_name,))
    save = cur.fetchone()
    cur.close()
    conn.close()

    if save:
        return jsonify({
            "exists": True,
            "chapter": save['current_chapter'],
            "step": save['current_step'],
            "hotaru": save['affection_hotaru'],
            "shizuka": save['affection_shizuka'],
            "flags": save['flags']
        })
    return jsonify({"exists": False})


@app.route('/api/script', methods=['POST'])
def get_script():
    data = request.json
    chapter = data.get('chapter', 0)
    step = data.get('step', 0)

    # 处理结局
    if chapter == 4:
        hotaru = data.get('hotaru', 0)
        shizuka = data.get('shizuka', 0)
        flags = data.get('flags', {})

        # 标记已读完全部章节
        flags['read_all_chapters'] = True
        ending_id, ending_text = determine_ending(hotaru, shizuka, flags)

        # 更新统计数据
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT total_endings FROM game_stats WHERE id = 1")
        row = cur.fetchone()
        if row:
            endings = json.loads(row[0]) if isinstance(row[0], str) else row[0]
            endings[ending_id] = endings.get(ending_id, 0) + 1
            cur.execute(
                "UPDATE game_stats SET total_endings = %s WHERE id = 1",
                (json.dumps(endings),)
            )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "type": "ending",
            "ending_id": ending_id,
            "ending_text": ending_text,
            "bg": "ending"
        })

    # 获取当前剧情节点
    if step == 0:
        script_key = chapter
    else:
        script_key = round(chapter + step * 0.1, 1)

    if script_key in SCRIPT:
        scene = SCRIPT[script_key]
        return jsonify({
            "type": "scene",
            "bg": scene.get("bg", "library"),
            "lines": scene.get("lines", []),
            "choices": scene.get("choices", [])
        })

    return jsonify({"type": "error", "message": "脚本不存在"})


@app.route('/api/choice', methods=['POST'])
def record_choice():
    data = request.json
    choice_id = data.get('choice_id')

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE choices_stats SET selected_count = selected_count + 1 WHERE choice_id = %s",
        (choice_id,)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok"})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # 获取选项统计
    cur.execute(
        "SELECT choice_id, choice_text, selected_count FROM choices_stats ORDER BY selected_count DESC LIMIT 12")
    choices = [dict(row) for row in cur.fetchall()]

    # 获取总游玩次数
    cur.execute("SELECT total_plays, total_endings FROM game_stats WHERE id = 1")
    row = cur.fetchone()
    plays = row['total_plays'] if row else 0
    endings = row['total_endings'] if row else {}

    cur.close()
    conn.close()

    return jsonify({
        "choices_stats": choices,
        "total_plays": plays,
        "total_endings": endings
    })


@app.route('/api/new_game', methods=['POST'])
def new_game():
    data = request.json
    player_name = data.get('player_name')

    conn = get_db()
    cur = conn.cursor()

    # 增加总游玩次数
    cur.execute("UPDATE game_stats SET total_plays = total_plays + 1 WHERE id = 1")

    # 删除旧存档，创建新存档
    cur.execute("DELETE FROM saves WHERE player_name = %s", (player_name,))
    cur.execute("""
        INSERT INTO saves (player_name, current_chapter, current_step,
                          affection_hotaru, affection_shizuka, flags)
        VALUES (%s, 0, 0, 0, 0, '{}')
    """, (player_name,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "chapter": 0, "step": 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

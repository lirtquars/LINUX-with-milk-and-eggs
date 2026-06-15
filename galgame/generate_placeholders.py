"""生成 Galgame 占位素材图片和音频文件。

运行方式: python generate_placeholders.py
需要安装: pip install Pillow
如果不想安装 Pillow，游戏也能运行——图片加载失败时会显示纯色背景。
"""
import os
import struct
import wave
import math

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'frontend', 'assets')

# 颜色配置
BG_COLORS = {
    'library': (139, 119, 101),        # 暖棕色 - 图书馆内部
    'library_sunset': (210, 150, 100),  # 夕阳橙 - 傍晚图书馆
    'bookshelf': (120, 90, 70),         # 深棕色 - 书架
    'garden': (144, 200, 144),          # 绿色 - 庭院
    'garden_night': (25, 30, 60),       # 深蓝紫 - 夜晚庭院
    'library_magic': (80, 40, 120),     # 紫色 - 魔法书区域
    'ending': (30, 20, 50),             # 深紫 - 结局
}

CHARACTER_COLORS = {
    'hotaru_happy': (255, 150, 100),     # 橙红 - 星野灯开心
    'hotaru_sad': (200, 130, 120),       # 暗橙 - 星野灯悲伤
    'hotaru_excited': (255, 180, 80),    # 金黄 - 星野灯兴奋
    'shizuka_normal': (140, 180, 220),   # 淡蓝 - 月之濑静正常
    'shizuka_sad': (110, 150, 190),      # 灰蓝 - 月之濑静悲伤
    'shizuka_happy': (160, 200, 240),    # 亮蓝 - 月之濑静开心
    'shizuka_blush': (200, 170, 200),    # 粉紫 - 月之濑静害羞
}


def generate_bg_images():
    """生成背景占位图"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("(!) Pillow not installed, skipping image generation. Run: pip install Pillow")
        return False

    bg_dir = os.path.join(ASSETS_DIR, 'bg')
    os.makedirs(bg_dir, exist_ok=True)

    for name, color in BG_COLORS.items():
        img = Image.new('RGB', (1280, 720), color)
        # 添加渐变效果
        draw = ImageDraw.Draw(img)
        for i in range(720):
            alpha = 1 - i / 720 * 0.3
            r = int(color[0] * alpha)
            g = int(color[1] * alpha)
            b = int(color[2] * alpha)
            draw.line([(0, i), (1280, i)], fill=(r, g, b))

        # 添加文字标签
        try:
            font = ImageFont.truetype("simhei.ttf", 32)
        except (IOError, OSError):
            try:
                font = ImageFont.truetype("arial.ttf", 32)
            except (IOError, OSError):
                font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), name, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text((640 - text_w / 2, 360 - text_h / 2), name, fill=(255, 255, 255, 100), font=font)

        filepath = os.path.join(bg_dir, f'{name}.jpg')
        img.save(filepath, 'JPEG', quality=85)
        print(f'  [OK] Background: {name}.jpg')

    return True


def generate_character_sprites():
    """生成角色立绘占位图"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False

    char_dir = os.path.join(ASSETS_DIR, 'character')
    os.makedirs(char_dir, exist_ok=True)

    for name, color in CHARACTER_COLORS.items():
        # 创建 400x600 的立绘，底部透明效果
        img = Image.new('RGBA', (400, 600), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 绘制简单的角色形状
        # 头部（圆形）
        head_y = 80
        draw.ellipse([140, head_y, 260, head_y + 120], fill=color, outline=(255, 255, 255, 80), width=2)
        # 身体（梯形用矩形近似）
        draw.rectangle([120, 200, 280, 420], fill=color)
        # 衣服暗部
        draw.rectangle([130, 220, 270, 410], fill=tuple(max(0, c - 40) for c in color))

        # 眼睛
        eye_color = (255, 255, 255)
        draw.ellipse([170, 110, 185, 125], fill=eye_color)
        draw.ellipse([215, 110, 230, 125], fill=eye_color)
        # 瞳孔
        draw.ellipse([175, 115, 182, 122], fill=(50, 50, 50))
        draw.ellipse([218, 115, 225, 122], fill=(50, 50, 50))

        # 表情差异
        if 'happy' in name or 'excited' in name:
            draw.arc([170, 125, 230, 150], 0, 180, fill=(255, 255, 255), width=2)
        elif 'sad' in name:
            draw.arc([170, 140, 230, 155], 180, 360, fill=(255, 255, 255), width=2)
        elif 'blush' in name:
            # 腮红
            draw.ellipse([150, 125, 170, 135], fill=(255, 150, 150, 120))
            draw.ellipse([230, 125, 250, 135], fill=(255, 150, 150, 120))
            draw.arc([170, 125, 230, 150], 0, 180, fill=(255, 255, 255), width=2)
        else:
            draw.line([175, 140, 225, 140], fill=(255, 255, 255), width=2)

        # 头发（简化）
        hair_color = tuple(max(0, c - 60) for c in color)
        draw.arc([130, 65, 270, 130], 180, 360, fill=hair_color, width=5)

        # 标签
        try:
            font = ImageFont.truetype("simhei.ttf", 20)
        except (IOError, OSError):
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except (IOError, OSError):
                font = ImageFont.load_default()
        draw.text((10, 10), name, fill=(255, 255, 255, 180), font=font)

        filepath = os.path.join(char_dir, f'{name}.png')
        img.save(filepath, 'PNG')
        print(f'  [OK] Sprite: {name}.png')

    return True


def generate_audio_placeholders():
    """生成静默占位音频文件（WAV 格式）"""
    audio_dir = os.path.join(ASSETS_DIR, 'audio')
    os.makedirs(audio_dir, exist_ok=True)

    audio_files = ['bgm_normal', 'spring', 'hotaru', 'shizuka', 'tense', 'click']

    for name in audio_files:
        filepath = os.path.join(audio_dir, f'{name}.mp3')
        if os.path.exists(filepath):
            continue

        # 创建一个极短的 WAV 占位符（1秒静默）
        wav_path = os.path.join(audio_dir, f'{name}_placeholder.wav')
        sample_rate = 44100
        duration = 1  # seconds
        n_samples = sample_rate * duration

        with wave.open(wav_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(struct.pack('<' + 'h' * n_samples, *[0] * n_samples))

        print(f'  [OK] Audio placeholder: {name}.wav (1s silence)')

    print('\n(!) NOTE: Placeholder audio is WAV format and only 1 second long.')
    print('  游戏会尝试加载 .mp3，失败时会静默运行不影响体验。')
    print('  推荐从以下网站下载真正的 BGM:')
    print('  - DOVA-SYNDROME: https://dova-s.jp/')
    print('  - Freesound: https://freesound.org/')
    print('  - 魔王魂: https://maou.audio/')
    return True


def main():
    print('=' * 50)
    print('  Galgame Placeholder Assets Generator')
    print('=' * 50)
    print()

    # Generate backgrounds
    print('[1/3] Generating background images...')
    if generate_bg_images():
        print()
    else:
        print('(!) Skipped background generation\n')

    # Generate character sprites
    print('[2/3] Generating character sprites...')
    if generate_character_sprites():
        print()
    else:
        print('(!) Skipped sprite generation\n')

    # Generate audio placeholders
    print('[3/3] Generating audio placeholders...')
    generate_audio_placeholders()

    print()
    print('=' * 50)
    print('  Done! All placeholder assets generated.')
    print('  Run: docker-compose up -d --build')
    print('=' * 50)


if __name__ == '__main__':
    main()

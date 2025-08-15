from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

def create_beautiful_app_icon(size):
    # 고품질 앱 아이콘 생성
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 그라데이션 배경 (부드러운 블루 투 퍼플)
    for y in range(size):
        # 상단에서 하단으로 그라데이션
        r = int(59 + (120 - 59) * y / size)  # 59 -> 120
        g = int(130 + (81 - 130) * y / size)  # 130 -> 81 
        b = int(246 + (196 - 246) * y / size)  # 246 -> 196
        draw.rectangle([0, y, size, y+1], fill=(r, g, b))
    
    # 둥근 모서리 마스크
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size, size], radius=size//6, fill=255)
    
    # 마스크 적용
    img.putalpha(mask)
    
    # 중앙에 큰 태양 아이콘
    center_x, center_y = size//2, size//2 - size//10
    sun_radius = size//4
    
    # 태양 광선 (더 많고 우아하게)
    for i in range(16):
        angle = i * math.pi / 8
        inner_radius = sun_radius + size//15
        outer_radius = sun_radius + size//8
        
        x1 = center_x + math.cos(angle) * inner_radius
        y1 = center_y + math.sin(angle) * inner_radius
        x2 = center_x + math.cos(angle) * outer_radius
        y2 = center_y + math.sin(angle) * outer_radius
        
        # 광선에 그라데이션 효과
        draw.line([(x1, y1), (x2, y2)], fill='#FEF3C7', width=max(1, size//100))
    
    # 태양 본체 (그라데이션)
    sun_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    sun_draw = ImageDraw.Draw(sun_img)
    
    # 태양 그라데이션
    for r in range(sun_radius, 0, -1):
        alpha = int(255 * (sun_radius - r) / sun_radius)
        color = (254, 243, 199, alpha) if r > sun_radius * 0.7 else (252, 211, 77, alpha)
        sun_draw.ellipse([
            center_x - r, center_y - r,
            center_x + r, center_y + r
        ], fill=color)
    
    img = Image.alpha_composite(img, sun_img)
    
    # 하단에 아름다운 텍스트
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", size//5)
    except:
        font = ImageFont.load_default()
    
    # 텍스트 그림자
    text = "모닝"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size - text_width) // 2
    text_y = int(size * 0.72)
    
    # 그림자 효과
    shadow_offset = max(1, size//100)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, 
              fill=(0, 0, 0, 100), font=font)
    
    # 메인 텍스트 (흰색)
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    return img

def create_beautiful_feature_graphic():
    # 아름다운 기능 그래픽 (1024x500)
    width, height = 1024, 500
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 백그라운드 그라데이션 (더 화려하게)
    for y in range(height):
        # 멀티 컬러 그라데이션
        ratio = y / height
        if ratio < 0.5:
            # 상단: 퍼플 to 블루
            r = int(139 + (59 - 139) * (ratio * 2))
            g = int(69 + (130 - 69) * (ratio * 2))
            b = int(255 + (246 - 255) * (ratio * 2))
        else:
            # 하단: 블루 to 시안
            r = int(59 + (34 - 59) * ((ratio - 0.5) * 2))
            g = int(130 + (197 - 130) * ((ratio - 0.5) * 2))
            b = int(246 + (255 - 246) * ((ratio - 0.5) * 2))
        
        draw.rectangle([0, y, width, y+1], fill=(r, g, b))
    
    # 장식적인 원들 (백그라운드)
    for i in range(20):
        x = (i * 60) % width
        y = (i * 37) % height
        radius = 30 + (i % 50)
        alpha = 20 + (i % 30)
        
        circle_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle_img)
        circle_draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=(255, 255, 255, alpha))
        img = Image.alpha_composite(img, circle_img)
    
    # 왼쪽에 큰 태양 아이콘
    sun_center_x, sun_center_y = 200, height//2
    sun_radius = 100
    
    # 태양 광선
    for i in range(20):
        angle = i * math.pi / 10
        inner_radius = sun_radius + 30
        outer_radius = sun_radius + 80
        
        x1 = sun_center_x + math.cos(angle) * inner_radius
        y1 = sun_center_y + math.sin(angle) * inner_radius
        x2 = sun_center_x + math.cos(angle) * outer_radius
        y2 = sun_center_y + math.sin(angle) * outer_radius
        
        draw.line([(x1, y1), (x2, y2)], fill='#FEF3C7', width=6)
    
    # 태양 본체
    draw.ellipse([
        sun_center_x - sun_radius, sun_center_y - sun_radius,
        sun_center_x + sun_radius, sun_center_y + sun_radius
    ], fill='#FCD34D')
    
    # 태양 하이라이트
    highlight_radius = sun_radius // 3
    draw.ellipse([
        sun_center_x - highlight_radius, sun_center_y - sun_radius//2 - highlight_radius,
        sun_center_x + highlight_radius, sun_center_y - sun_radius//2 + highlight_radius
    ], fill='#FEF3C7')
    
    # 오른쪽에 텍스트
    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 100)
        font_medium = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 48)
        font_small = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 36)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 메인 타이틀 "모닝"
    title_x, title_y = 450, 120
    
    # 텍스트 그림자
    draw.text((title_x + 3, title_y + 3), "모닝", fill=(0, 0, 0, 80), font=font_large)
    # 메인 텍스트
    draw.text((title_x, title_y), "모닝", fill='white', font=font_large)
    
    # 서브 타이틀들
    draw.text((450, 240), "매일 아침 당신을 위한", fill='#E0E7FF', font=font_medium)
    draw.text((450, 300), "따뜻한 응원 메시지", fill='#E0E7FF', font=font_medium)
    
    # 하단 작은 텍스트
    draw.text((450, 380), "✨ 긍정적인 하루의 시작", fill='#C7D2FE', font=font_small)
    draw.text((450, 420), "💪 당신의 꿈을 응원합니다", fill='#C7D2FE', font=font_small)
    
    return img

# 아이콘들 생성
print("Creating beautiful app icon...")
icon512 = create_beautiful_app_icon(512)
icon512.save('public/logo512_beautiful.png')
print("OK - Beautiful app icon created: logo512_beautiful.png")

print("Creating beautiful feature graphic...")
feature = create_beautiful_feature_graphic()
feature.save('public/feature_graphic_beautiful.png')
print("OK - Beautiful feature graphic created: feature_graphic_beautiful.png")

print("\nAll beautiful graphics created successfully!")
print("Files location:")
print("- App Icon: public/logo512_beautiful.png")
print("- Feature Graphic: public/feature_graphic_beautiful.png")
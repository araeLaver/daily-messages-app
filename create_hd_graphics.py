from PIL import Image, ImageDraw, ImageFont
import math

def create_hd_app_icon():
    # 고해상도 앱 아이콘 (512x512)
    size = 512
    img = Image.new('RGB', (size, size), (255, 255, 255))  # RGB 모드로 변경
    draw = ImageDraw.Draw(img)
    
    # 그라데이션 배경 - 더 진한 색상
    for y in range(size):
        ratio = y / size
        r = int(59 + (37 - 59) * ratio)    # 블루 계열
        g = int(130 + (99 - 130) * ratio)
        b = int(246 + (235 - 246) * ratio)
        draw.rectangle([0, y, size, y+1], fill=(r, g, b))
    
    # 중앙 태양
    center_x, center_y = size//2, size//2 - 30
    sun_radius = 80
    
    # 태양 광선 (더 굵고 선명하게)
    for i in range(12):
        angle = i * math.pi / 6
        x1 = center_x + math.cos(angle) * (sun_radius + 25)
        y1 = center_y + math.sin(angle) * (sun_radius + 25)
        x2 = center_x + math.cos(angle) * (sun_radius + 60)
        y2 = center_y + math.sin(angle) * (sun_radius + 60)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 223, 0), width=8)
    
    # 태양 본체
    draw.ellipse([
        center_x - sun_radius, center_y - sun_radius,
        center_x + sun_radius, center_y + sun_radius
    ], fill=(255, 215, 0))
    
    # 태양 하이라이트
    draw.ellipse([
        center_x - 30, center_y - 50,
        center_x + 30, center_y + 10
    ], fill=(255, 255, 200))
    
    # 텍스트 "모닝"
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 72)
    except:
        font = ImageFont.load_default()
    
    text = "모닝"
    # 텍스트 위치 계산
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    text_y = size - 120
    
    # 텍스트 그림자 (더 진하게)
    draw.text((text_x + 3, text_y + 3), text, fill=(0, 0, 0), font=font)
    # 메인 텍스트
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    return img

def create_hd_feature_graphic():
    # 고해상도 기능 그래픽 (1024x500)
    width, height = 1024, 500
    img = Image.new('RGB', (width, height), (255, 255, 255))  # RGB 모드
    draw = ImageDraw.Draw(img)
    
    # 그라데이션 배경
    for y in range(height):
        ratio = y / height
        r = int(67 + (30 - 67) * ratio)    # 파란색 그라데이션
        g = int(56 + (144 - 56) * ratio)
        b = int(202 + (255 - 202) * ratio)
        draw.rectangle([0, y, width, y+1], fill=(r, g, b))
    
    # 왼쪽 태양
    sun_x, sun_y = 180, height//2
    sun_radius = 85
    
    # 태양 광선
    for i in range(16):
        angle = i * math.pi / 8
        x1 = sun_x + math.cos(angle) * (sun_radius + 20)
        y1 = sun_y + math.sin(angle) * (sun_radius + 20)
        x2 = sun_x + math.cos(angle) * (sun_radius + 55)
        y2 = sun_y + math.sin(angle) * (sun_radius + 55)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 223, 0), width=6)
    
    # 태양 본체
    draw.ellipse([
        sun_x - sun_radius, sun_y - sun_radius,
        sun_x + sun_radius, sun_y + sun_radius
    ], fill=(255, 215, 0))
    
    # 태양 하이라이트
    draw.ellipse([
        sun_x - 35, sun_y - 45,
        sun_x + 25, sun_y - 5
    ], fill=(255, 255, 200))
    
    # 오른쪽 텍스트
    try:
        font_xl = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 90)
        font_large = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 42)
        font_medium = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 32)
    except:
        font_xl = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    text_x = 400
    
    # 메인 타이틀 "모닝"
    draw.text((text_x + 2, 102), "모닝", fill=(0, 0, 0), font=font_xl)  # 그림자
    draw.text((text_x, 100), "모닝", fill=(255, 255, 255), font=font_xl)
    
    # 서브 타이틀
    draw.text((text_x, 220), "매일 아침 당신을 위한", fill=(255, 255, 255), font=font_large)
    draw.text((text_x, 280), "따뜻한 응원 메시지", fill=(255, 255, 255), font=font_large)
    
    # 하단 작은 텍스트
    draw.text((text_x, 360), "✨ 긍정적인 하루의 시작", fill=(240, 248, 255), font=font_medium)
    draw.text((text_x, 400), "💪 당신의 꿈을 응원합니다", fill=(240, 248, 255), font=font_medium)
    
    return img

# 고해상도 이미지 생성
print("Creating HD app icon (512x512)...")
app_icon = create_hd_app_icon()
app_icon.save('public/app_icon_hd.png', 'PNG', quality=95, optimize=True)
print("OK - HD app icon saved: app_icon_hd.png")

print("Creating HD feature graphic (1024x500)...")
feature_graphic = create_hd_feature_graphic()
feature_graphic.save('public/feature_graphic_hd.png', 'PNG', quality=95, optimize=True)
print("OK - HD feature graphic saved: feature_graphic_hd.png")

# 파일 크기 확인
import os
icon_size = os.path.getsize('public/app_icon_hd.png')
feature_size = os.path.getsize('public/feature_graphic_hd.png')

print(f"\nFile sizes:")
print(f"App icon: {icon_size:,} bytes ({icon_size/1024:.1f} KB)")
print(f"Feature graphic: {feature_size:,} bytes ({feature_size/1024:.1f} KB)")

print("\nFiles ready for Play Console upload!")
print("- App Icon: public/app_icon_hd.png (512x512)")
print("- Feature Graphic: public/feature_graphic_hd.png (1024x500)")
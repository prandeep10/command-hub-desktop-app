import os
from PIL import Image, ImageDraw, ImageFont

def generate_icon(output_path="assets/icon.png", size=(512, 512)):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    w, h = size
    padding = 24
    rect = [padding, padding, w - padding, h - padding]
    radius = 96

    # Draw rounded rectangle background (gradient dark slate / deep blue)
    # We can draw smooth rounded rectangle with solid color + border glow
    bg_color = (24, 25, 38, 255) # Dark slate background #181926
    border_color = (137, 180, 250, 255) # Soft cyan/blue accent #89b4fa
    
    draw.rounded_rectangle(rect, radius=radius, fill=bg_color, outline=border_color, width=8)

    # Inner decorative header bar (macOS / Linux terminal style dots)
    dot_y = padding + 50
    dots = [
        (padding + 60, dot_y, (255, 95, 87)),   # Red
        (padding + 90, dot_y, (254, 188, 46)),  # Yellow
        (padding + 120, dot_y, (40, 200, 64))   # Green
    ]
    for dx, dy, color in dots:
        draw.ellipse([dx - 10, dy - 10, dx + 10, dy + 10], fill=color)

    # Terminal prompt lines `>_`
    # Draw chevron `>`
    chevron_color = (137, 180, 250, 255) # Accent blue
    cursor_color = (166, 227, 161, 255)  # Soft green #a6e3a1

    # Draw `>` chevron using lines
    start_x, start_y = padding + 80, h // 2 - 40
    stroke_w = 20

    # Upper diagonal of >
    draw.line([start_x, start_y, start_x + 60, start_y + 50], fill=chevron_color, width=stroke_w)
    # Lower diagonal of >
    draw.line([start_x + 60, start_y + 50, start_x, start_y + 100], fill=chevron_color, width=stroke_w)

    # Draw `_` cursor line
    cur_x = start_x + 95
    cur_y = start_y + 100
    draw.line([cur_x, cur_y, cur_x + 80, cur_y], fill=cursor_color, width=stroke_w)

    # Save PNG
    img.save(output_path, "PNG")
    print(f"Icon generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_icon()

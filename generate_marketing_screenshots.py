import os
from PIL import Image, ImageDraw, ImageFont

# Define Canvas and Layout Constants for the base design (6.7" Display)
CANVAS_WIDTH = 1290
CANVAS_HEIGHT = 2796
SCREENSHOT_WIDTH = 960

# Background colors matching YenDidii identity
COLOR_CLAY = (214, 90, 49, 255)       # #D65A31 - primary terracotta clay
COLOR_GREEN = (0, 122, 51, 255)       # #007A33 - primary kente green
COLOR_CHARCOAL = (45, 36, 30, 255)     # #2D241E - deep charcoal background

# Text styling colors
TEXT_WHITE = (255, 255, 255, 255)
TEXT_LIGHT_CLAY = (255, 235, 230, 255)
TEXT_LIGHT_GREEN = (230, 245, 236, 255)
TEXT_LIGHT_CHARCOAL = (242, 234, 228, 255)

# Paths
INPUT_DIR = "app_store_screenshots/iphone"
OUTPUT_DIR_6_7 = "app_store_screenshots/iphone_promo_6.7"
OUTPUT_DIR_6_5 = "app_store_screenshots/iphone_promo_6.5"

# Ensure output directories exist
os.makedirs(OUTPUT_DIR_6_7, exist_ok=True)
os.makedirs(OUTPUT_DIR_6_5, exist_ok=True)

# Screenshot configuration
SCREENSHOTS_CONFIG = [
    {
        "filename": "Simulator Screenshot - iPhone 16 Pro - 2026-05-21 at 11.24.15.png",
        "bg_color": COLOR_CLAY,
        "text_color_sub": TEXT_LIGHT_CLAY,
        "title": "Taste Authentic Ghanaian Food",
        "subtitle": "Order delicious home-cooked meals prepared by passionate local hosts.",
        "output_name": "promo_1_home.png"
    },
    {
        "filename": "Simulator Screenshot - iPhone 16 Pro - 2026-05-21 at 11.24.39.png",
        "bg_color": COLOR_GREEN,
        "text_color_sub": TEXT_LIGHT_GREEN,
        "title": "Discover Cooks Near You",
        "subtitle": "Explore an interactive map of home kitchens and discover cooks in your neighborhood.",
        "output_name": "promo_2_map.png"
    },
    {
        "filename": "Simulator Screenshot - iPhone 16 Pro - 2026-05-21 at 11.25.36.png",
        "bg_color": COLOR_CHARCOAL,
        "text_color_sub": TEXT_LIGHT_CHARCOAL,
        "title": "Dine at the Cook's Table",
        "subtitle": "Experience warm Ghanaian hospitality by dining in directly at the host's home.",
        "output_name": "promo_3_dinein.png"
    },
    {
        "filename": "Simulator Screenshot - iPhone 16 Pro - 2026-05-21 at 11.25.46.png",
        "bg_color": COLOR_CLAY,
        "text_color_sub": TEXT_LIGHT_CLAY,
        "title": "Track Your Orders Live",
        "subtitle": "Receive real-time progress alerts from acceptance to the cooking pot.",
        "output_name": "promo_4_tracking.png"
    },
    {
        "filename": "Simulator Screenshot - iPhone 16 Pro - 2026-05-21 at 11.25.55.png",
        "bg_color": COLOR_GREEN,
        "text_color_sub": TEXT_LIGHT_GREEN,
        "title": "Share Food & Earn Extra",
        "subtitle": "Switch to Cook Mode, list your signature dishes, and host meals for others.",
        "output_name": "promo_5_cook.png"
    }
]

# Load system font
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"
font_title = ImageFont.truetype(FONT_PATH, 76, index=1)   # Bold
font_subtitle = ImageFont.truetype(FONT_PATH, 42, index=10) # Medium

def draw_wrapped_text(draw, text, font, color, max_width, start_x, start_y, line_spacing=15):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_text = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), line_text, font=font)
        w = bbox[2] - bbox[0]
        if w > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(' '.join(current_line))
        
    y = start_y
    for line in lines:
        # Center horizontally
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (CANVAS_WIDTH - w) // 2
        
        draw.text((x, y), line, font=font, fill=color)
        h = bbox[3] - bbox[1]
        y += h + line_spacing
        
    return y

def round_corners_with_bezel(img, radius, bezel_width=8):
    # Scale image to fit the screenshot width
    scale_factor = SCREENSHOT_WIDTH / img.width
    new_h = int(img.height * scale_factor)
    img_scaled = img.resize((SCREENSHOT_WIDTH, new_h), Image.Resampling.LANCZOS)
    
    # Create rounding mask
    mask = Image.new('L', img_scaled.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, img_scaled.width, img_scaled.height), radius, fill=255)
    
    # Paste scaled image onto an RGBA canvas
    rounded_img = Image.new('RGBA', img_scaled.size)
    rounded_img.paste(img_scaled, (0, 0), mask=mask)
    
    # Draw dark premium phone bezel outline
    draw_bezel = ImageDraw.Draw(rounded_img)
    draw_bezel.rounded_rectangle(
        (0, 0, rounded_img.width, rounded_img.height), 
        radius, 
        outline=(26, 20, 16, 255), 
        width=bezel_width
    )
    
    return rounded_img

def main():
    print("Starting screenshot generation script...")
    
    for config in SCREENSHOTS_CONFIG:
        input_path = os.path.join(INPUT_DIR, config["filename"])
        
        if not os.path.exists(input_path):
            print(f"Warning: Screenshot file not found: {input_path}")
            continue
            
        print(f"Processing: {config['filename']} -> {config['output_name']}")
        
        # Load screenshot
        screenshot = Image.open(input_path)
        
        # Create solid canvas with the requested background color (base size 6.7" display: 1290x2796)
        canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), config["bg_color"])
        draw = ImageDraw.Draw(canvas)
        
        # Draw dynamic title and subtitle centered at the top
        next_y = draw_wrapped_text(
            draw, 
            config["title"], 
            font_title, 
            TEXT_WHITE, 
            CANVAS_WIDTH - 160, 
            80, 
            160
        )
        
        draw_wrapped_text(
            draw, 
            config["subtitle"], 
            font_subtitle, 
            config["text_color_sub"], 
            CANVAS_WIDTH - 200, 
            100, 
            next_y + 25
        )
        
        # Round the screenshot corners and scale it
        rounded_screenshot = round_corners_with_bezel(screenshot, radius=48, bezel_width=8)
        
        # Centering screenshot horizontally, pinning to the bottom with 80px margin
        x_offset = (CANVAS_WIDTH - rounded_screenshot.width) // 2
        y_offset = CANVAS_HEIGHT - rounded_screenshot.height - 80
        
        # Paste rounded screenshot onto the canvas
        canvas.paste(rounded_screenshot, (x_offset, y_offset), mask=rounded_screenshot)
        
        # 1. Save Base 6.7" version (1290 x 2796)
        output_path_6_7 = os.path.join(OUTPUT_DIR_6_7, config["output_name"])
        canvas.save(output_path_6_7, "PNG")
        print(f"  Saved 6.7\" Display: {output_path_6_7}")
        
        # 2. Save 6.5" Display standard size (1242 x 2688)
        canvas_6_5_std = canvas.resize((1242, 2688), Image.Resampling.LANCZOS)
        output_path_6_5_std = os.path.join(OUTPUT_DIR_6_5, config["output_name"])
        canvas_6_5_std.save(output_path_6_5_std, "PNG")
        print(f"  Saved 6.5\" Display (1242x2688): {output_path_6_5_std}")
        
        # 3. Save 6.5" Display alternative size (1284 x 2778)
        canvas_6_5_alt = canvas.resize((1284, 2778), Image.Resampling.LANCZOS)
        output_path_6_5_alt = os.path.join(OUTPUT_DIR_6_5, config["output_name"].replace(".png", "_1284.png"))
        canvas_6_5_alt.save(output_path_6_5_alt, "PNG")
        print(f"  Saved 6.5\" Display Alternative (1284x2778): {output_path_6_5_alt}")

if __name__ == "__main__":
    main()

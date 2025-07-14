from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# === Configuration ===
FONT_PATH = "arial.ttf"
TITLE_SIZE = 48
SECTION_TITLE_SIZE = 36
BODY_SIZE = 24
MARGIN = 60
COLUMN_GAP = 80
LINE_SPACING = 12
CANVAS_WIDTH = 1600
BG_COLOR = "white"
HEADER_COLOR = "#1f4e79"

def extract_sections(text):
    sections = {}
    current = None
    buffer = []

    for line in text.splitlines():
        if ":" in line and line.strip().endswith(":"):
            if current and buffer:
                sections[current] = "\n".join(buffer).strip()
                buffer = []
            current = line.strip().replace(":", "")
        elif current:
            buffer.append(line.strip())
    if current and buffer:
        sections[current] = "\n".join(buffer).strip()
    return sections

def wrap_text_by_width(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            test_line = f"{line} {word}".strip()
            width = draw.textlength(test_line, font=font)
            if width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines

def draw_wrapped_block(draw, x, y, title, content, title_font, body_font, max_width):
    draw.text((x, y), title, font=title_font, fill=HEADER_COLOR)
    y += title_font.getbbox(title)[3] + LINE_SPACING

    if isinstance(content, list):
        for bullet in content:
            wrapped = wrap_text_by_width(draw, bullet, body_font, max_width - 40)
            draw.text((x + 20, y), "•", font=body_font, fill="black")
            y += 0
            for i, line in enumerate(wrapped):
                indent = 40 if i > 0 else 30
                draw.text((x + indent, y), line, font=body_font, fill="black")
                y += body_font.getbbox(line)[3] + LINE_SPACING
    else:
        lines = wrap_text_by_width(draw, content, body_font, max_width)
        for line in lines:
            draw.text((x, y), line, font=body_font, fill="black")
            y += body_font.getbbox(line)[3] + LINE_SPACING

    return y + LINE_SPACING * 2

def clean_quotes(raw_block):
    return [q.strip().strip('"“”') for q in raw_block.split(">") if len(q.strip()) > 30]

def calculate_required_height(sections, draw, title_font, header_font, body_font, col_width):
    y = MARGIN + title_font.getbbox("User Persona")[3] + LINE_SPACING * 3
    left_height = 0
    right_height = 0

    left_keys = ["Name", "Bio", "Interests", "Needs", "Frustrations"]
    right_keys = ["Personality Traits", "Tone of Voice", "Writing Style", "Notable Quotes"]

    for key in left_keys:
        content = sections.get(key, "—")
        left_height += estimate_block_height(draw, key, content, header_font, body_font, col_width)

    for key in right_keys:
        content = sections.get(key, "")
        if key == "Tone of Voice":
            content += "\n" + sections.get("Writing Style", "")
        if key == "Notable Quotes":
            quotes = clean_quotes(content)
            content = quotes
        right_height += estimate_block_height(draw, key, content, header_font, body_font, col_width)

    return max(left_height, right_height) + y + MARGIN

def estimate_block_height(draw, title, content, title_font, body_font, max_width):
    height = title_font.getbbox(title)[3] + LINE_SPACING
    if isinstance(content, list):
        for bullet in content:
            wrapped = wrap_text_by_width(draw, bullet, body_font, max_width - 40)
            height += len(wrapped) * (body_font.getbbox("A")[3] + LINE_SPACING)
    else:
        lines = wrap_text_by_width(draw, content, body_font, max_width)
        height += len(lines) * (body_font.getbbox("A")[3] + LINE_SPACING)
    return height + LINE_SPACING * 2

def generate_visual_persona(username):
    input_txt = f"output/{username}_persona.txt"
    output_img = f"output/{username}_persona.png"

    if not os.path.exists(input_txt):
        print(f"❌ Persona text not found: {input_txt}")
        return

    with open(input_txt, "r", encoding="utf-8") as f:
        raw_text = f.read()

    sections = extract_sections(raw_text)

    # Load fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
        header_font = ImageFont.truetype(FONT_PATH, SECTION_TITLE_SIZE)
        body_font = ImageFont.truetype(FONT_PATH, BODY_SIZE)
    except:
        print("⚠️ Using default font fallback")
        title_font = header_font = body_font = ImageFont.load_default()

    # Dummy draw object for measurement
    dummy_img = Image.new("RGB", (CANVAS_WIDTH, 2000))
    dummy_draw = ImageDraw.Draw(dummy_img)

    # Calculate dynamic height
    col_width = (CANVAS_WIDTH - 3 * MARGIN) // 2
    required_height = calculate_required_height(sections, dummy_draw, title_font, header_font, body_font, col_width)

    # Create final image
    img = Image.new("RGB", (CANVAS_WIDTH, required_height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Title
    y = MARGIN
    draw.text((MARGIN, y), f"User Persona: {username}", font=title_font, fill="black")
    y += title_font.getbbox(username)[3] + LINE_SPACING * 3

    left_x = MARGIN
    right_x = CANVAS_WIDTH // 2 + COLUMN_GAP // 2
    left_y = right_y = y

    left_keys = [
        ("🧑 Name", "Name"),
        ("📝 Bio", "Bio"),
        ("🎯 Goals", "Interests"),
        ("📌 Needs", "Needs"),
        ("💢 Frustrations", "Frustrations")
    ]

    right_keys = [
        ("💡 Personality", "Personality Traits"),
        ("🎙️ Tone & Style", "Tone of Voice"),
        ("💬 Notable Quotes", "Notable Quotes")
    ]

    for title, key in left_keys:
        content = sections.get(key, "—")
        left_y = draw_wrapped_block(draw, left_x, left_y, title, content, header_font, body_font, col_width)

    for title, key in right_keys:
        content = sections.get(key, "")
        if key == "Tone of Voice":
            style = sections.get("Writing Style", "")
            content += f"\n{style}".strip()
        if key == "Notable Quotes":
            content = clean_quotes(content)
        right_y = draw_wrapped_block(draw, right_x, right_y, title, content, header_font, body_font, col_width)

    img.save(output_img)
    print(f"✅ Visual persona saved to: {output_img}")

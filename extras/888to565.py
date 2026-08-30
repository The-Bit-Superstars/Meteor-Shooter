from PIL import Image
import sys

def rgb888_to_rgb565(r, g, b):
    return (
        ((r & 0xF8) << 8) |
        ((g & 0xFC) << 3) |
        (b >> 3)
    )

def parse_color(value):
    return int(value, 16) & 0xFFFF

def convert(input_file, output_file):
    img = Image.open(input_file).convert("RGBA")
    pixels = list(img.get_flattened_data())
    used_colors = set()
    for r, g, b, a in pixels:
        if a >= 128:
            used_colors.add(rgb888_to_rgb565(r, g, b))
    transparent_candidates = [
        0x0000,
        0x4000,
        0xD000,
        0x8000,
        0x9000,
        0xA000,
        0xA800,
        0xE000,
        0xF000,
        0xF800,
    ]
    transparent_color = 0x0000
    for candidate in transparent_candidates:
        if candidate not in used_colors:
            transparent_color = candidate
            break
    print(f"Transparent color: 0x{transparent_color:04X}")
    data = bytearray()
    for r, g, b, a in pixels:
        if a < 128:
            color = transparent_color
        else:
            color = rgb888_to_rgb565(r, g, b)
        data.append((color >> 8) & 0xFF)
        data.append(color & 0xFF)
    with open(output_file, "w") as f:
        f.write("bytearray(b'")
        for byte in data:
            f.write(f"\\x{byte:02x}")
        f.write("')\n")

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("  rgb888.py input.png output.txt")
        print("Example:")
        print("  rgb888.py image.png image.txt")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert(input_file, output_file)


if __name__ == "__main__":
    main()
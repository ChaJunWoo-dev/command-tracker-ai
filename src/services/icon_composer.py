from pathlib import Path
from PIL import Image
from typing import List

ASSETS_DIR = Path(__file__).parent.parent.parent / "assets" / "icons"
SUB_DIR = ASSETS_DIR / "subs"
ATTACKS_DIR = ASSETS_DIR / "attacks"

ICON_SIZE = 48
SPACING = 4
PADDING = 8
BG_COLOR = (0, 0, 0, 160)


class IconComposer:
    def __init__(self):
        self.icon_cache: dict[str, Image.Image] = {}

    def _load_icon(self, name: str) -> Image.Image:
        if name in self.icon_cache:
            return self.icon_cache[name]

        if name in ["plus", "arrow", "down", "left", "right", "down_left", "down_right"]:
            path = SUB_DIR / f"{name}.png"
        else:
            path = ATTACKS_DIR / f"{name}.png"

        icon = Image.open(path).convert("RGBA")
        icon = icon.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
        self.icon_cache[name] = icon
        return icon

    def compose(self, inputs: List[str], output_path: Path) -> Path:
        """입력 시퀀스를 조합하여 하나의 이미지로 생성(커맨드 완성)"""
        icons = [self._load_icon(name) for name in inputs]

        icons_width = ICON_SIZE * len(icons) + SPACING * (len(icons) - 1)
        total_width = icons_width + PADDING * 2
        total_height = ICON_SIZE + PADDING * 2

        combined = Image.new("RGBA", (total_width, total_height), BG_COLOR)

        x_offset = PADDING
        for icon in icons:
            combined.paste(icon, (x_offset, PADDING), icon)
            x_offset += ICON_SIZE + SPACING

        combined.save(output_path, "PNG")

        return output_path

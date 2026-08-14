import importlib.util
import unittest
from pathlib import Path

from PIL import Image

SKILL_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_DIR / "scripts" / "validate_atlas.py"
SPEC = importlib.util.spec_from_file_location("validate_atlas", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {MODULE_PATH}")
VALIDATE_ATLAS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE_ATLAS)


class ValidateAtlasChromaFringeTest(unittest.TestCase):
    def test_counts_key_colored_visible_pixel_at_transparency_boundary(self) -> None:
        image = Image.new("RGBA", (5, 5), (0, 0, 0, 0))
        for y in range(1, 4):
            for x in range(1, 4):
                image.putpixel((x, y), (20, 20, 20, 255))
        image.putpixel((1, 2), (255, 0, 255, 255))

        count = VALIDATE_ATLAS.chroma_fringe_count(
            image,
            chroma_key=(255, 0, 255),
            distance_threshold=1,
            edge_radius=1,
            alpha_minimum=16,
        )

        self.assertEqual(count, 1)

    def test_ignores_key_colored_pixel_away_from_transparency_boundary(self) -> None:
        image = Image.new("RGBA", (7, 7), (20, 20, 20, 255))
        image.putpixel((3, 3), (255, 0, 255, 255))

        count = VALIDATE_ATLAS.chroma_fringe_count(
            image,
            chroma_key=(255, 0, 255),
            distance_threshold=1,
            edge_radius=1,
            alpha_minimum=16,
        )

        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()

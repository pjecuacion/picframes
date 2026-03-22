# Purpose: Unit tests for picframes/processor.py core image processing logic
# Expected behavior: All transformation helpers produce correct RGBA output
# Related bug or lesson ID: N/A
# Preconditions: Pillow must be installed; no network access required

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from picframes.processor import (
    SUPPORTED_EXTENSIONS,
    ProcessingOptions,
    ProcessingJob,
    ProcessingResult,
    build_jobs,
    discover_files,
    _to_square,
    _apply_padding,
    _get_mask,
    _apply_mask,
    _process_file,
    _save_ico,
)


def _solid_rgba(size: int, color=(255, 0, 0, 255)) -> Image.Image:
    return Image.new("RGBA", (size, size), color)


def _rect_rgba(w: int, h: int, color=(0, 128, 0, 255)) -> Image.Image:
    return Image.new("RGBA", (w, h), color)


class TestSupportedExtensions(unittest.TestCase):
    def test_image_extensions_present(self):
        for ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"):
            self.assertIn(ext, SUPPORTED_EXTENSIONS)

    def test_non_image_excluded(self):
        self.assertNotIn(".txt", SUPPORTED_EXTENSIONS)
        self.assertNotIn(".pdf", SUPPORTED_EXTENSIONS)


class TestToSquare(unittest.TestCase):
    def test_already_square_unchanged(self):
        img = _solid_rgba(100)
        result = _to_square(img)
        self.assertEqual(result.size, (100, 100))

    def test_wide_image_cropped_to_height(self):
        img = _rect_rgba(200, 100)
        result = _to_square(img)
        self.assertEqual(result.size, (100, 100))

    def test_tall_image_cropped_to_width(self):
        img = _rect_rgba(80, 160)
        result = _to_square(img)
        self.assertEqual(result.size, (80, 80))


class TestApplyPadding(unittest.TestCase):
    def test_no_padding_same_size(self):
        img = _solid_rgba(100)
        result = _apply_padding(img, 0)
        self.assertEqual(result.size, (100, 100))

    def test_with_padding_same_canvas_size(self):
        img = _solid_rgba(100)
        result = _apply_padding(img, 10)
        self.assertEqual(result.size, (100, 100))

    def test_padding_leaves_transparent_border(self):
        img = _solid_rgba(100, (255, 0, 0, 255))
        result = _apply_padding(img, 20)
        self.assertEqual(result.getpixel((0, 0))[3], 0)

    def test_excessive_padding_returns_transparent(self):
        img = _solid_rgba(10)
        result = _apply_padding(img, 10)
        for x in range(10):
            for y in range(10):
                self.assertEqual(result.getpixel((x, y))[3], 0)


class TestGetMask(unittest.TestCase):
    def test_square_returns_none(self):
        self.assertIsNone(_get_mask("square", 100, 25))

    def test_circle_mask_is_L_mode(self):
        mask = _get_mask("circle", 100, 25)
        self.assertEqual(mask.mode, "L")
        self.assertEqual(mask.size, (100, 100))

    def test_circle_mask_center_is_white(self):
        self.assertEqual(_get_mask("circle", 100, 25).getpixel((50, 50)), 255)

    def test_circle_mask_corner_is_black(self):
        self.assertEqual(_get_mask("circle", 100, 25).getpixel((0, 0)), 0)

    def test_rounded_square_mask_center_is_white(self):
        self.assertEqual(_get_mask("rounded_square", 100, 25).getpixel((50, 50)), 255)

    def test_rounded_square_mask_extreme_corner_is_black(self):
        self.assertEqual(_get_mask("rounded_square", 100, 25).getpixel((0, 0)), 0)

    def test_unknown_shape_returns_none(self):
        self.assertIsNone(_get_mask("hexagon", 100, 25))


class TestApplyMask(unittest.TestCase):
    def test_full_mask_preserves_alpha(self):
        img = _solid_rgba(50, (255, 0, 0, 200))
        mask = Image.new("L", (50, 50), 255)
        self.assertEqual(_apply_mask(img, mask).getpixel((25, 25))[3], 200)

    def test_zero_mask_makes_transparent(self):
        img = _solid_rgba(50, (255, 0, 0, 255))
        mask = Image.new("L", (50, 50), 0)
        self.assertEqual(_apply_mask(img, mask).getpixel((25, 25))[3], 0)

    def test_half_mask_halves_alpha(self):
        img = _solid_rgba(50, (255, 0, 0, 255))
        mask = Image.new("L", (50, 50), 128)
        alpha = _apply_mask(img, mask).getpixel((25, 25))[3]
        self.assertAlmostEqual(alpha, 128, delta=2)


class TestBuildJobs(unittest.TestCase):
    def test_outputs_as_png(self):
        sources = [Path("photo.jpg"), Path("icon.webp")]
        jobs = build_jobs(sources, Path("out"), ProcessingOptions(output_format="png"))
        self.assertTrue(all(j.destination.suffix == ".png" for j in jobs))

    def test_outputs_as_ico(self):
        sources = [Path("photo.jpg"), Path("icon.webp")]
        jobs = build_jobs(sources, Path("out"), ProcessingOptions(output_format="ico"))
        self.assertTrue(all(j.destination.suffix == ".ico" for j in jobs))

    def test_unsupported_files_skipped(self):
        sources = [Path("doc.txt"), Path("image.png")]
        jobs = build_jobs(sources, Path("out"), ProcessingOptions())
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].source.name, "image.png")

    def test_destination_in_output_dir(self):
        sources = [Path("a/b/photo.png")]
        jobs = build_jobs(sources, Path("output"), ProcessingOptions())
        self.assertEqual(jobs[0].destination.parent, Path("output"))


class TestProcessFile(unittest.TestCase):
    def test_circle_frame_no_remove_bg(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src = tmp / "input.png"
            Image.new("RGBA", (80, 60), (200, 100, 50, 255)).save(src)
            dst = tmp / "out.png"
            _process_file(src, dst, ProcessingOptions(frame_shape="circle", remove_bg=False))
            result = Image.open(dst)
            self.assertEqual(result.mode, "RGBA")
            self.assertEqual(result.size, (60, 60))  # center-cropped to square
            self.assertEqual(result.getpixel((0, 0))[3], 0)  # corner transparent

    def test_square_frame_preserves_alpha(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src = tmp / "input.png"
            Image.new("RGBA", (100, 100), (50, 200, 50, 255)).save(src)
            dst = tmp / "out.png"
            _process_file(src, dst, ProcessingOptions(frame_shape="square", remove_bg=False))
            result = Image.open(dst)
            self.assertEqual(result.getpixel((50, 50))[3], 255)

    def test_ico_output_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src = tmp / "input.png"
            Image.new("RGBA", (200, 200), (100, 100, 200, 255)).save(src)
            dst = tmp / "out.ico"
            _process_file(src, dst, ProcessingOptions(frame_shape="circle", remove_bg=False, output_format="ico"))
            self.assertTrue(dst.exists())
            with Image.open(dst) as result:
                self.assertEqual(result.format, "ICO")


class TestSaveIco(unittest.TestCase):
    def test_creates_ico_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            img = Image.new("RGBA", (256, 256), (200, 100, 50, 255))
            dst = tmp / "icon.ico"
            _save_ico(img, dst)
            self.assertTrue(dst.exists())

    def test_ico_is_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            img = Image.new("RGBA", (256, 256), (50, 150, 250, 128))
            dst = tmp / "icon.ico"
            _save_ico(img, dst)
            with Image.open(dst) as result:
                self.assertEqual(result.format, "ICO")

    def test_small_image_still_produces_ico(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            img = Image.new("RGBA", (32, 32), (255, 0, 0, 255))
            dst = tmp / "small.ico"
            _save_ico(img, dst)
            self.assertTrue(dst.exists())


if __name__ == "__main__":
    unittest.main()

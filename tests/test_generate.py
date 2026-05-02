from __future__ import annotations

import argparse
import base64
import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "generate.py"
SPEC = importlib.util.spec_from_file_location("generate", SCRIPT_PATH)
generate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["generate"] = generate
SPEC.loader.exec_module(generate)


class GenerateScriptTest(unittest.TestCase):
    def test_sanitize_prefix_rejects_paths(self) -> None:
        with self.assertRaises(ValueError):
            generate.sanitize_prefix("../escape")

    def test_sanitize_prefix_normalizes_text(self) -> None:
        self.assertEqual(generate.sanitize_prefix("hero image 01"), "hero_image_01")

    def test_validate_args_rejects_empty_prefix(self) -> None:
        args = argparse.Namespace(
            prompt="a test prompt",
            guidance=None,
            steps=None,
            output=".",
            prefix="!!!",
        )
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            generate.validate_args(args)

    def test_save_images_avoids_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            existing = output_dir / "ernie_20990101_000000.png"
            existing.write_bytes(b"existing")
            response = SimpleNamespace(
                data=[
                    SimpleNamespace(
                        b64_json=base64.b64encode(b"new image bytes").decode("ascii")
                    )
                ]
            )
            args = argparse.Namespace(
                output=str(output_dir),
                prefix="ernie",
                n=1,
                response_format="b64_json",
            )
            original_datetime = generate.datetime

            class FixedDatetime:
                @classmethod
                def now(cls):
                    return cls()

                def strftime(self, _format: str) -> str:
                    return "20990101_000000"

            try:
                generate.datetime = FixedDatetime
                files = generate.save_images(response, args)
            finally:
                generate.datetime = original_datetime

            self.assertEqual(existing.read_bytes(), b"existing")
            self.assertEqual(Path(files[0]["path"]).name, "ernie_20990101_000000-1.png")
            self.assertEqual(Path(files[0]["path"]).read_bytes(), b"new image bytes")

    def test_save_images_rejects_invalid_base64(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            response = SimpleNamespace(data=[SimpleNamespace(b64_json="not base64")])
            args = argparse.Namespace(
                output=temp_dir,
                prefix="ernie",
                n=1,
                response_format="b64_json",
            )
            with self.assertRaises(RuntimeError):
                generate.save_images(response, args)


if __name__ == "__main__":
    unittest.main()

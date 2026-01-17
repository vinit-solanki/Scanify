import os
import sys
from pathlib import Path

# Ensure relative imports work if needed
BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from vision.ocr_agent import extract_text_blocks


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/olmocr_test.py <image_path> [engine]")
        sys.exit(1)
    image_path = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else os.getenv("OCR_ENGINE", "olmocr")
    blocks = extract_text_blocks(image_path, engine=engine)
    print(f"Engine: {engine}")
    print(f"Blocks: {len(blocks)}")
    for i, b in enumerate(blocks[:20]):
        print(f"[{i:02d}] conf={b.get('confidence')} text={b.get('text')[:120]}")


if __name__ == "__main__":
    main()

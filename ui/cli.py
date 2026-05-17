"""
CLI interface.

Usage:
    python ui/cli.py input.pdf
    python ui/cli.py input.xlsx -o output.md
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import argparse
from facade import ConverterFacade, UnsupportedFormatError


def main():
    parser = argparse.ArgumentParser(description="Convert PDF/DOCX/XLSX/XLS/PPTX to Markdown")
    parser.add_argument("input", help="Path to the input file")
    parser.add_argument("-o", "--output", help="Path to the output .md file (default: print to stdout)")
    args = parser.parse_args()

    facade = ConverterFacade()

    try:
        result = facade.convert(args.input)
    except UnsupportedFormatError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        if result.assets:
            output_dir = os.path.dirname(os.path.abspath(args.output))
            for asset_path, asset_bytes in result.assets.items():
                full = os.path.join(output_dir, asset_path)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "wb") as f:
                    f.write(asset_bytes)
            print(f"Saved to {args.output} (+ {len(result.assets)} image(s))")
        else:
            print(f"Saved to {args.output}")
    else:
        print(result.markdown)


if __name__ == "__main__":
    main()

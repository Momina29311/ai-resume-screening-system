import argparse
from src.parser import extract_text_from_pdf, save_extracted_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True, help="Path to resume PDF")
    args = parser.parse_args()

    text = extract_text_from_pdf(args.resume)
    print("========== Resume Parsed Successfully ==========")
    print(f"Characters Extracted: {len(text)}")
    print(f"Words Extracted: {len(text.split())}")
    print("\nPreview:\n")
    print(text[:1500])

    save_extracted_text(args.resume)

if __name__ == "__main__":
    main()
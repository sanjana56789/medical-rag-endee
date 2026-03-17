# from pypdf import PdfReader

# def process_file(filename, content):
#     text = ""

#     if filename.endswith(".pdf"):
#         reader = PdfReader(content)
#         for page in reader.pages:
#             text += page.extract_text() + "\n"
#     else:
#         text = content.decode("utf-8")

#     # chunking
#     chunks = [text[i:i+300] for i in range(0, len(text), 300)]
#     return chunks





# from pypdf import PdfReader
# import io


# def extract_text(content, filename):
#     """
#     Extract text from PDF or TXT
#     """
#     if filename.endswith(".pdf"):
#         reader = PdfReader(io.BytesIO(content))
#         text = ""

#         for page in reader.pages:
#             extracted = page.extract_text()
#             if extracted:
#                 text += extracted

#         return text

#     else:
#         return content.decode("utf-8")


# def chunk_text(text, chunk_size=300):
#     """
#     Split text into chunks
#     """
#     words = text.split()
#     chunks = []

#     for i in range(0, len(words), chunk_size):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)

#     return chunks



# final working code with OCR for scanned PDFs and images
# from pypdf import PdfReader
# import pytesseract
# from pdf2image import convert_from_bytes
# from PIL import Image
# import io

# # Set Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Set Poppler path
# POPPLER_PATH = r'C:\Users\Sanjana M\Downloads\poppler\poppler-25.12.0\Library\bin'


# def extract_text(content, filename):
#     if filename.lower().endswith(".pdf"):
#         try:
#             reader = PdfReader(io.BytesIO(content))
#             text = ""
#             for page in reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted
#             if text.strip():
#                 print("✅ Text-based PDF detected")
#                 return text
#         except Exception as e:
#             print(f"pypdf failed: {e}")

#         print("🔍 Scanned PDF detected — using OCR...")
#         try:
#             images = convert_from_bytes(content, poppler_path=POPPLER_PATH)
#             text = ""
#             for i, image in enumerate(images):
#                 print(f"   OCR processing page {i+1}...")
#                 page_text = pytesseract.image_to_string(image)
#                 text += page_text + "\n"
#             if text.strip():
#                 print("✅ OCR extraction successful")
#                 return text
#             else:
#                 return None
#         except Exception as e:
#             print(f"OCR failed: {e}")
#             return None

#     elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
#         try:
#             image = Image.open(io.BytesIO(content))
#             text = pytesseract.image_to_string(image)
#             return text
#         except Exception as e:
#             print(f"Image OCR failed: {e}")
#             return None

#     else:
#         return content.decode("utf-8")


# def chunk_text(text, chunk_size=300):
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)
#     return chunks


from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image, ImageFilter, ImageEnhance
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Users\Sanjana M\Downloads\poppler\poppler-25.12.0\Library\bin'


def preprocess_image(image):
    """Enhance image quality for better OCR"""
    # Increase resolution
    w, h = image.size
    image = image.resize((w * 2, h * 2), Image.LANCZOS)

    # Convert to grayscale
    image = image.convert('L')

    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Increase sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)

    # Sharpen filter
    image = image.filter(ImageFilter.SHARPEN)

    return image


def extract_text(content, filename):
    if filename.lower().endswith(".pdf"):
        # Try normal text extraction first
        try:
            reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            if text.strip():
                print("✅ Text-based PDF detected")
                return text
        except Exception as e:
            print(f"pypdf failed: {e}")

        # OCR with preprocessing
        print("🔍 Scanned PDF detected — using OCR with enhancement...")
        try:
            # High DPI for better quality
            images = convert_from_bytes(
                content,
                poppler_path=POPPLER_PATH,
                dpi=300
            )
            text = ""
            for i, image in enumerate(images):
                print(f"   OCR processing page {i+1}...")

                # Try with preprocessing first
                processed = preprocess_image(image)
                page_text = pytesseract.image_to_string(
                    processed,
                    config='--psm 6 --oem 3'
                )

                # If result is too short, try original image
                if len(page_text.strip()) < 50:
                    page_text = pytesseract.image_to_string(
                        image,
                        config='--psm 6 --oem 3'
                    )

                text += page_text + "\n"
                print(f"   Extracted {len(page_text)} characters")

            print("✅ OCR extraction successful")
            print("📄 Preview:", text[:300])  # show what was extracted
            return text if text.strip() else None

        except Exception as e:
            print(f"OCR failed: {e}")
            return None

    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        try:
            image = Image.open(io.BytesIO(content))
            processed = preprocess_image(image)
            text = pytesseract.image_to_string(processed, config='--psm 6 --oem 3')
            return text
        except Exception as e:
            print(f"Image OCR failed: {e}")
            return None

    else:
        return content.decode("utf-8")


def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
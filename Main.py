import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import time
import os

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_image(prompt, output_path="raw_image.png"):
    print("🔮 Sending request to Hugging Face API...")
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        print(f"📡 Status code: {response.status_code}")

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(output_path)
            print(f"✅ Image saved as {output_path}")
            return image
        else:
            print("❌ API Error:", response.text)
            return None

    except Exception as e:
        print("🚨 Network or request error:", e)
        return None

def enhance_image(image, output_path="enhanced_image.png"):
    if image is None:
        print("⚠️ No image to enhance.")
        return
    print("🎨 Enhancing image...")
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = image.filter(ImageFilter.GaussianBlur(radius=1.2))
    image.save(output_path)
    print(f"✨ Enhanced image saved as {output_path}")
    image.show()

def main():
    os.makedirs("outputs", exist_ok=True)

    while True:
        prompt = input("\n💬 Enter a prompt (or type 'exit' to quit): ").strip()
        if prompt.lower() == "exit":
            print("👋 Exiting program.")
            break

        raw_path = "outputs/raw.png"
        enhanced_path = "outputs/enhanced.png"

        image = generate_image(prompt, raw_path)
        enhance_image(image, enhanced_path)

if __name__ == "__main__":
    main()

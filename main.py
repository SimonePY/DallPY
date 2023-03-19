import argparse as ap
import io
import os
from base64 import b64decode as b64

import openai as oa
import tomlkit as tk
from PIL import Image

CONFIG_FILE = "config.toml"
ALLOWED_SIZES = ["256x256", "512x512", "1024x1024"]
ALLOWED_QUANTITIES = list(range(1, 11))

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as configFile:
        configFile.write('api_key = ""\nimage_path = ""')

with open(CONFIG_FILE, "r") as readConfig:
    config = tk.parse(readConfig.read())

api_key = config.get("api_key")
if not api_key:
    print("Error: API key is missing in the configuration file.")
    exit(1)

image_path = os.path.expanduser(config.get("image_path"))
if not image_path:
    print("Error: Image path is missing in the configuration file.")
    exit(1)
os.makedirs(image_path, exist_ok=True)

parser = ap.ArgumentParser(
    description="Generate images using OpenAI GPT-3.",
    formatter_class=ap.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--prompt", type=str, help="the prompt to use for generating images."
)

parser.add_argument(
    "--size",
    type=str,
    choices=ALLOWED_SIZES,
    default="256x256",
    help="the size of the generated image.",
)
parser.add_argument(
    "--quantity",
    type=int,
    choices=ALLOWED_QUANTITIES,
    default=1,
    help="the number of images to generate.",
)
args = parser.parse_args()

if args.prompt is None:
    parser.print_help()
    exit(0)

oa.api_key = api_key
print(
    f"Generating {args.quantity} image(s) with prompt '{args.prompt}' and size {args.size}."
)

for i, _ in enumerate(range(args.quantity)):
    try:
        generation = oa.Image.create(
            prompt=args.prompt, n=args.quantity, size=args.size, response_format="b64_json"
        )
    except Exception as e:
        print(f"Encountered an exception: {e}")
        exit(1)
    if generation["data"]:
        image_data = b64(generation["data"][0]["b64_json"])
        img = Image.open(io.BytesIO(image_data)).convert("RGB")
        image_format = img.format.lower() if img.format else "png"
        file_name = os.path.join(image_path, f"{args.prompt}_image_{i + 1}.{image_format}")
        with open(file_name, "wb") as image_file:
            img.save(image_file, format=image_format.upper())
        print(f"Image created and saved.")
    else:
        print(f"No image was generated.")

# DallPY

Terminal-Line interface for generate images with DALL-E API!

# Usage

You will require **Python** for run this scripts!

Run the command `pip install requirements.txt` for install all libraries.

Run with the command `python main.py` for generate the folder and the config file.

Edit the config file with your openai api key and the name for the image folder.

```
--help = return help menu.
--prompt <str> = Your prompt for generate the image.
--size <int> = The size of the image.
--quantity <int> = How much images you want to generate.
Example : python main.py --prompt "Computer" --size 512x512 --quantity 1
```
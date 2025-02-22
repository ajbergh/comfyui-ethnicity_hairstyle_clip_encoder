import random
import torch
import csv
import os
import time

class CLIPTextEncodeWithExtras:
    @classmethod
    def INPUT_TYPES(s):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        def read_csv_options(filename):
            filepath = os.path.join(script_dir, filename)
            options = []
            try:
                with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        options.append(row[0].strip())
            except FileNotFoundError:
                print(f"Error: CSV file '{filename}' not found in {script_dir}.")
                return ["random"]

            # Remove "random" if it's already in the file to avoid duplicates.
            if "random" in options:
                options.remove("random")
            return ["random"] + sorted(options)

        # CRITICAL: Store the returned lists BEFORE creating INPUT_TYPES
        ethnicity_options = read_csv_options('ethnicity.csv')
        hairstyle_options = read_csv_options('hairstyle.csv')

        return {
            "required": {
                "text_positive": ("STRING", {"multiline": True, "default": ""}),
                "text_negative": ("STRING", {"multiline": True, "default": ""}),
                "clip": ("CLIP", ),
                "ethnicity_toggle": (["on", "off"], {"default": "on"}),
                "hairstyle_toggle": (["on", "off"], {"default": "on"}),
            },
            "optional": {
                # Use the stored lists and their first elements.
                "ethnicity": (ethnicity_options, {"default": ethnicity_options[0]}),
                "hairstyle": (hairstyle_options, {"default": hairstyle_options[0]}),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("positive_conditioning", "negative_conditioning")
    FUNCTION = "encode"
    CATEGORY = "conditioning"

    @classmethod
    def IS_CHANGED(self, text_positive, text_negative, ethnicity, hairstyle, ethnicity_toggle, hairstyle_toggle):
        if ethnicity == "random" or hairstyle == "random":
            return time.time()
        return text_positive + text_negative

    def encode(self, clip, text_positive, text_negative, ethnicity, hairstyle, ethnicity_toggle, hairstyle_toggle):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        def read_csv_options(filename):  # Local read for encode
            filepath = os.path.join(script_dir, filename)
            options = []
            try:
                with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                         options.append(row[0].strip())
            except FileNotFoundError:
                print(f"Error: CSV file '{filename}' not found in {script_dir}.")
                return ["random"] # Consistent default
            return options

        ethnicity_options_for_random = [option for option in read_csv_options('ethnicity.csv') if option != 'random']
        hairstyle_options_for_random = [option for option in read_csv_options('hairstyle.csv') if option != 'random']


        # Ethnicity Handling
        if ethnicity_toggle == "on":
            if ethnicity == "random":
                chosen_ethnicity = random.choice(ethnicity_options_for_random)
            else:
                chosen_ethnicity = ethnicity
            text_positive = f"{chosen_ethnicity} person, {text_positive}"

        # Hairstyle Handling
        if hairstyle_toggle == "on":
            if hairstyle == "random":
                chosen_hairstyle = random.choice(hairstyle_options_for_random)
            else:
                chosen_hairstyle = hairstyle
            text_positive = f"{chosen_hairstyle} hair, {text_positive}"


        tokens_positive = clip.tokenize(text_positive)
        tokens_negative = clip.tokenize(text_negative)
        conditioning_positive, pooled_positive = clip.encode_from_tokens(tokens_positive, return_pooled=True)
        conditioning_negative, pooled_negative = clip.encode_from_tokens(tokens_negative, return_pooled=True)
        return (
            [[conditioning_positive, {"pooled_output": pooled_positive, "tokens": tokens_positive}]],
            [[conditioning_negative, {"pooled_output": pooled_negative, "tokens": tokens_negative}]],
        )

NODE_CLASS_MAPPINGS = {
    "CLIPTextEncodeWithExtras": CLIPTextEncodeWithExtras
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPTextEncodeWithExtras": "CLIP Text Encode (Ethnicity/Hairstyle)"
}
"""
================================================================================
ComfyUI Custom Node: CLIP Text Encode (Ethnicity/Hairstyle)
--------------------------------------------------------------------------------
This module implements a custom ComfyUI node that enhances CLIP text encoding 
by incorporating ethnicity and hairstyle options into the positive prompt text.

Features:
    - Loads "ethnicity" and "hairstyle" options from CSV files (ethnicity.csv 
      and hairstyle.csv) located in the same directory as this file.
    - Provides a dropdown selection with "random" as the first option for both 
      ethnicity and hairstyle.
    - When toggled on, appends the selected ethnicity and/or hairstyle to the 
      positive text, modifying the prompt before encoding.
    - Offers a built-in "random" functionality where a random option is chosen 
      from the CSV files (excluding the "random" entry if present).
    - Wraps the CLIP's tokenize and encode methods to produce both tokenized 
      outputs and pooled outputs for conditioning.
      
Usage within ComfyUI:
    - Define required inputs:
        • text_positive: The primary text prompt (supports multiline input).
        • text_negative: The negative text prompt (supports multiline input).
        • clip: The CLIP model instance for encoding.
        • ethnicity_toggle: ("on"/"off") to enable/disable ethnicity inclusion.
        • hairstyle_toggle: ("on"/"off") to enable/disable hairstyle inclusion.
    - Define optional inputs:
        • ethnicity: Selection from sorted ethnicity options (default is "random").
        • hairstyle: Selection from sorted hairstyle options (default is "random").
      
--------------------------------------------------------------------------------
Author: Adam Bergh ajbergh@gmail.com
Date: 02/22/2025
================================================================================
"""

import random
import torch
import csv
import os
import time

class CLIPTextEncodeWithExtras:
    @classmethod
    def INPUT_TYPES(s):
        # Determine the directory where this script resides.
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Helper function to read CSV file options
        def read_csv_options(filename):
            # Construct the full file path for the CSV file.
            filepath = os.path.join(script_dir, filename)
            options = []
            try:
                # Open the CSV file with UTF-8 encoding.
                with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    # Read each row and add the first column's value after stripping whitespace.
                    for row in reader:
                        options.append(row[0].strip())
            except FileNotFoundError:
                # If the file is not found, log an error and return a default list.
                print(f"Error: CSV file '{filename}' not found in {script_dir}.")
                return ["random"]

            # Remove the "random" entry if it exists, to avoid duplicates.
            if "random" in options:
                options.remove("random")
            # Return a new list with "random" as the first element followed by sorted options.
            return ["random"] + sorted(options)

        # IMPORTANT: Load the CSV options before constructing the INPUT_TYPES dictionary.
        ethnicity_options = read_csv_options('ethnicity.csv')
        hairstyle_options = read_csv_options('hairstyle.csv')

        # Define the input types required by the node.
        return {
            "required": {
                "text_positive": ("STRING", {"multiline": True, "default": ""}),
                "text_negative": ("STRING", {"multiline": True, "default": ""}),
                "clip": ("CLIP", ),
                "ethnicity_toggle": (["on", "off"], {"default": "on"}),
                "hairstyle_toggle": (["on", "off"], {"default": "on"}),
            },
            "optional": {
                # Provide the ethnicity and hairstyle options for selection,
                # with "random" as the default if present.
                "ethnicity": (ethnicity_options, {"default": ethnicity_options[0]}),
                "hairstyle": (hairstyle_options, {"default": hairstyle_options[0]}),
            }
        }

    # Define the types of outputs: two conditioning results (positive and negative).
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    # Names associated with the returned outputs.
    RETURN_NAMES = ("positive_conditioning", "negative_conditioning")
    # Name of the function to execute.
    FUNCTION = "encode"
    # Node category within ComfyUI.
    CATEGORY = "conditioning"

    @classmethod
    def IS_CHANGED(self, text_positive, text_negative, ethnicity, hairstyle, ethnicity_toggle, hairstyle_toggle):
        """
        Determines if the node's inputs have changed.
        If either ethnicity or hairstyle is set to "random", it returns the current time,
        forcing re-encoding. Otherwise, it concatenates the positive and negative texts.
        """
        if ethnicity == "random" or hairstyle == "random":
            return time.time()
        return text_positive + text_negative

    def encode(self, clip, text_positive, text_negative, ethnicity, hairstyle, ethnicity_toggle, hairstyle_toggle):
        # Get the directory of this script to locate the CSV files.
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Local helper function to read CSV options within the encode function context.
        def read_csv_options(filename):
            filepath = os.path.join(script_dir, filename)
            options = []
            try:
                # Open and read the CSV file.
                with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        options.append(row[0].strip())
            except FileNotFoundError:
                # Print error and return a default list containing "random".
                print(f"Error: CSV file '{filename}' not found in {script_dir}.")
                return ["random"]
            return options

        # Read and filter options excluding "random" for selecting random elements.
        ethnicity_options_for_random = [option for option in read_csv_options('ethnicity.csv') if option != 'random']
        hairstyle_options_for_random = [option for option in read_csv_options('hairstyle.csv') if option != 'random']

        # Handle Ethnicity selection: add ethnicity info to the positive text if toggle is on.
        if ethnicity_toggle == "on":
            if ethnicity == "random":
                # Choose a random ethnicity from the available options.
                chosen_ethnicity = random.choice(ethnicity_options_for_random)
            else:
                chosen_ethnicity = ethnicity
            # Prepend the chosen ethnicity with additional description to the text.
            text_positive = f"{chosen_ethnicity} person, {text_positive}"

        # Handle Hairstyle selection: add hairstyle info to the positive text if toggle is on.
        if hairstyle_toggle == "on":
            if hairstyle == "random":
                # Randomly select a hairstyle from the available options.
                chosen_hairstyle = random.choice(hairstyle_options_for_random)
            else:
                chosen_hairstyle = hairstyle
            # Prepend the chosen hairstyle description to the text.
            text_positive = f"{chosen_hairstyle} hair, {text_positive}"

        # Tokenize both positive and negative texts using the provided CLIP model.
        tokens_positive = clip.tokenize(text_positive)
        tokens_negative = clip.tokenize(text_negative)
        # Encode the tokens to produce conditioning data and a pooled output.
        conditioning_positive, pooled_positive = clip.encode_from_tokens(tokens_positive, return_pooled=True)
        conditioning_negative, pooled_negative = clip.encode_from_tokens(tokens_negative, return_pooled=True)

        # Return the conditioning outputs in the expected format.
        return (
            [[conditioning_positive, {"pooled_output": pooled_positive, "tokens": tokens_positive}]],
            [[conditioning_negative, {"pooled_output": pooled_negative, "tokens": tokens_negative}]],
        )

# Mapping from the node class name to its class implementation.
NODE_CLASS_MAPPINGS = {
    "CLIPTextEncodeWithExtras": CLIPTextEncodeWithExtras
}

# Mapping from the node class name to its display name in the ComfyUI interface.
NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPTextEncodeWithExtras": "CLIP Text Encode (Ethnicity/Hairstyle)"
}
# comfyui-ethnicity_hairstyle_clip_encoder

This ComfyUI custom node enhances the standard CLIP text encoding functionality by integrating ethnicity and hairstyle selection into the positive prompt. Designed to work seamlessly with ComfyUI, this node allows you to influence the conditioning process by dynamically appending descriptive modifiers. Users can choose a specific ethnicity or hairstyle, or opt for a "random" selection that picks an option from a predefined CSV list.

## Features

- **Dynamic CSV Loading:**  
  The node reads ethnicity and hairstyle options from CSV files (`ethnicity.csv` and `hairstyle.csv`).  
  - Options are sorted alphabetically.
  - Each option list is prefixed with a default "random" entry, ensuring that the backend’s default is used if no specific selection is made.

- **Random Capability:**  
  If the "random" option is selected, the node picks a random ethnicity or hairstyle (excluding duplicates in the CSV) at runtime, adding variety to the prompt.

- **Toggle Functionality:**  
  Ethnicity and hairstyle modifications can be enabled or disabled independently using toggle inputs (`ethnicity_toggle` and `hairstyle_toggle`).

- **Customized Prompt Modification:**  
  The node preprocesses the positive text prompt by prepending the chosen ethnicity (e.g., "Asian person,") and hairstyle (e.g., "curly hair,") descriptors before encoding. This modification directly influences the conditioning outputs generated by the CLIP model.

- **Backend Integration:**  
  The node wraps CLIP’s tokenize and encode methods:
  - Applies tokenization on both the modified positive prompt and the negative prompt.
  - Produces both tokenized and pooled encoding results for improved conditioning.

## Usage within ComfyUI

1. **Required Inputs:**
   - `text_positive`: Primary prompt text (supports multiline input).
   - `text_negative`: Negative prompt text (supports multiline input).
   - `clip`: The CLIP model instance used for encoding.
   - `ethnicity_toggle`: ("on" or "off") to enable ethnicity inclusion.
   - `hairstyle_toggle`: ("on" or "off") to enable hairstyle inclusion.

2. **Optional Inputs:**
   - `ethnicity`: Dropdown selector populated with sorted ethnicity options; default is "random".
   - `hairstyle`: Dropdown selector populated with sorted hairstyle options; default is "random".

## How It Works

- **CSV Reading Mechanism:**  
  The node defines helper functions to read CSV files from its local directory and extracts options, ensuring that the "random" entry is only added once.

- **Prompt Modification:**  
  When enabled, the node modifies the positive prompt by appending the selected ethnicity and/or hairstyle descriptors. For example, if toggled on and ethnicity is set to "random", a random ethnicity is chosen from the CSV (excluding "random") and prepended to the prompt.

- **Tokenization and Encoding:**  
  The updated prompt is tokenized and encoded using the provided CLIP model, generating conditioning outputs used later in the UI pipeline.

## Extension Integration (JavaScript)

A companion JavaScript extension modifies the UI behavior of this node in ComfyUI:
- It intercepts the node creation process and applies custom widget callbacks.
- The extension ensures that default Python settings are preserved by not overriding widget default values.
- Callbacks update application settings based on user selection for ethnicity and hairstyle.

This comprehensive integration guarantees that prompt modifications are dynamically processed, providing an enhanced and flexible conditioning experience within the ComfyUI framework.

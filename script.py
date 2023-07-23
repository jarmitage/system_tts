import time
import gradio as gr
from pathlib import Path
import subprocess
from modules import shared

params = {
    "display_name": "System TTS",
    "autoplay": True,
    "show_text": True
}

def tts(text, output_file):
    print(f"tts: {text} -> {output_file}")
    subprocess.call(['say', '-o', output_file, '--data-format', 'LEF32@22050', text])

def output_modifier(string, state):
    # Modifies the output string before it is presented in the UI. In chat mode, it is applied to the bot's reply. Otherwise, it is applied to the entire output.
    if string == '':
        string = '*Empty reply, try regenerating*'
    else:
        output_file = Path(f'extensions/system_tts/outputs/{state["character_menu"]}_{int(time.time())}.wav')
        tts(string, output_file)
        autoplay = 'autoplay' if params['autoplay'] else ''
        html_string = f'<audio src="file/{output_file.as_posix()}" controls {autoplay}></audio>'
        if params['show_text']:
            string = f'{html_string}\n\n{string}'
        else:
            string = html_string
    
    shared.processing_message = "*Is typing...*"
    return string

def history_modifier(history):
    # Modifies the chat history before the text generation in chat mode begins.
    
    # Remove autoplay from the last reply
    if len(history['internal']) > 0:
        history['visible'][-1] = [
            history['visible'][-1][0],
            history['visible'][-1][1].replace('controls autoplay>', 'controls>')
        ]

    return history

'''

def ui():
    # Creates custom gradio elements when the UI is launched.
    pass

def custom_css():
    # Returns custom CSS as a string. It is applied whenever the web UI is loaded.
    return ""

def custom_js():
    # Same as above but for javascript.
    return ""

def input_modifier(string, state):
    # Modifies the input string before it enters the model. In chat mode, it is applied to the user message. Otherwise, it is applied to the entire prompt.
    return string

def bot_prefix_modifier(string, state):
    # Applied in chat mode to the prefix for the bot's reply.
    pass

def state_modifier(state):
    # Modifies the dictionary containing the UI input parameters before it is used by the text generation functions.
    return state

def custom_generate_reply():#(...):
    # Overrides the main text generation function.
    pass

def custom_generate_chat_prompt():#(...):
    # Overrides the prompt generator in chat mode.
    pass

def tokenizer_modifier(state, prompt, input_ids, input_embeds):
    # Modifies the input_ids/input_embeds fed to the model. Should return prompt, input_ids, input_embeds. See the multimodal extension for an example.
    pass

def custom_tokenized_length(prompt):
    # Used in conjunction with tokenizer_modifier, returns the length in tokens of prompt. See the multimodal extension for an example.
    pass

'''
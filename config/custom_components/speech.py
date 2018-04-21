import tempfile
import subprocess
import os

DOMAIN = 'speech'

DEFAULT_TEXT = 'test'
DEFAULT_LANGUAGE = 'fr-FR'

def setup(hass, config):
    """Setup is called when Home Assistant is loading our component."""

    def handle_speak(call):
        text = call.data.get('text', DEFAULT_TEXT)
        lang = call.data.get('lang', DEFAULT_LANGUAGE)

        say(text,lang)

    hass.services.register(DOMAIN, 'speak', handle_speak)

    # Return boolean to indicate that initialization was successfully.
    return True

def say(text,lang):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        fname = f.name
    cmd = ['pico2wave', '--wave', fname]
    cmd.extend(['-l', lang])
    cmd.append(text)
    with tempfile.TemporaryFile() as f:
        subprocess.call(cmd, stdout=f, stderr=f)
        f.seek(0)
        output = f.read()
    play(fname)
    os.remove(fname)
    
def play(filename):
    cmd = ['aplay', str(filename)]
    with tempfile.TemporaryFile() as f:
        subprocess.call(cmd, stdout=f, stderr=f)
        f.seek(0)
        output = f.read()

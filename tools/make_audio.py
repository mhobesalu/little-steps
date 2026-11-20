# Makes the spoken clips in audio/ from the card labels and phrases in index.html.
# Voices: English en-US-AvaNeural, Estonian et-EE-AnuNeural (Microsoft neural voices).
# With AZURE_SPEECH_KEY and AZURE_SPEECH_REGION set (licensed, Azure free tier F0 is enough), it uses Azure Speech.
#   python3 tools/make_audio.py --force      (re-records every clip; the GitHub workflow "Make voices" does this)
# Without them it falls back to edge-tts (pip install edge-tts), which is for testing only, not for the store.
import asyncio, os, re, sys, urllib.request
from xml.sax.saxutils import escape
FORCE = '--force' in sys.argv
KEY, REGION = os.environ.get('AZURE_SPEECH_KEY'), os.environ.get('AZURE_SPEECH_REGION')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
cards = re.search(r'const CARDS=\{(.*?)\n\};', html, re.S).group(1)
items = {}
for key, en, et in re.findall(r'(\w+):\{en:"([^"]*)",et:"([^"]*)"\}', cards):
    items[key] = {'en': en, 'et': et}
def strs(lang):
    blk = re.search(r'^' + lang + r':\{(.*)\},?$', re.search(r'const STR=\{(.*?)\n\};', html, re.S).group(1), re.M).group(1)
    return dict(re.findall(r'(\w+):"([^"]*)"', blk))
en, et = strs('en'), strs('et')
for k in ['allDone', 'well0', 'last']:
    items['_' + k] = {'en': en[k], 'et': et[k]}
VOICE = {'en': 'en-US-AvaNeural', 'et': 'et-EE-AnuNeural'}
LOCALE = {'en': 'en-US', 'et': 'et-EE'}
def azure(lang, text, out):
    ssml = (f"<speak version='1.0' xml:lang='{LOCALE[lang]}'><voice name='{VOICE[lang]}'>"
            f"<prosody rate='-8%' pitch='+2%'>{escape(text)}</prosody></voice></speak>")
    req = urllib.request.Request(f'https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1', data=ssml.encode('utf-8'),
        headers={'Ocp-Apim-Subscription-Key': KEY, 'Content-Type': 'application/ssml+xml',
                 'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3', 'User-Agent': 'little-steps-audio'})
    data = urllib.request.urlopen(req, timeout=60).read()
    if not data: raise RuntimeError('empty audio')
    open(out, 'wb').write(data)
async def one(lang, key, text):
    out = os.path.join(ROOT, 'audio', f'{lang}_{key}.mp3')
    if not FORCE and os.path.exists(out) and os.path.getsize(out) > 0: return True
    try:
        if KEY and REGION:
            azure(lang, text, out); return True
        import edge_tts
        await edge_tts.Communicate(text, VOICE[lang], rate='-8%', pitch='+2Hz', proxy=os.environ.get('HTTPS_PROXY')).save(out)
        return os.path.getsize(out) > 0
    except Exception as e:
        if os.path.exists(out): os.remove(out)
        print('fail', lang, key, e); return False
async def main():
    miss = 0
    for key, t in items.items():
        for lang in ('en', 'et'):
            if not await one(lang, key, t[lang]): miss += 1
    print('engine:', 'azure' if KEY and REGION else 'edge-tts', 'clips:', len(items) * 2, 'missing:', miss)
    if miss: sys.exit(1)
asyncio.run(main())

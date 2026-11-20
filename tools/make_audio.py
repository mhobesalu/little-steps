# Makes the spoken clips in audio/ from the card labels and phrases in index.html.
# Voices: English en-US-AvaNeural, Estonian et-EE-AnuNeural (Microsoft neural voices).
# Usage: pip install edge-tts && python3 tools/make_audio.py   (re-run until it says "missing: 0")
# NOTE: before selling, regenerate these with a licensed Azure Speech account (same voice names).
import asyncio, os, re, json, sys
import edge_tts
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
async def one(lang, key, text):
    out = os.path.join(ROOT, 'audio', f'{lang}_{key}.mp3')
    if os.path.exists(out) and os.path.getsize(out) > 0: return True
    try:
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
    print('clips:', len(items) * 2, 'missing:', miss)
asyncio.run(main())

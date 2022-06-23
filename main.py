from flask import Flask, request
import pychromecast
import logging
import os
from gtts import gTTS
#from slugify import slugify
#from pathlib import Path
#from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chromecast_name = os.environ.get('SPEAKERS') 

app = Flask(__name__)
logging.info("Starting up chromecasts")
# chromecasts, _ = pychromecast.get_chromecasts()
#logging.info("Searching for {}".format(chromecast_name))
#cast = next(cc for cc in chromecasts if cc.cast_info.friendly_name == chromecast_name)
services, browser = pychromecast.discovery.discover_chromecasts()
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[chromecast_name])
logging.info(services)
cast = chromecasts[0]

def play_tts(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = "message.mp3"
    tts.save('/app/static/{}'.format(filename))
    mp3_url = "http://{}.ngrok.io/static/message.mp3".format(os.environ.get('NGROK_SLUG'))
    logging.info(mp3_url)
    play_mp3(mp3_url)


def play_mp3(mp3_url):
    print(mp3_url)
    cast.wait()
    mc = cast.media_controller
    mc.play_media(mp3_url, 'audio/mp3')
    mc.block_until_active()


#@app.route('/static/<path:path>')
#def send_static(path):
#        return send_from_directory('static', path)

@app.route('/play/<filename>')
def play(filename):
    urlparts = urlparse(request.url)
    mp3 = Path(os.path.dirname(__file__) + "/static/" + filename)
    if mp3.is_file():
        play_mp3("http://"+urlparts.netloc+"/static/"+filename)
        return filename
    else:
        return "False"

@app.route('/say/')
def say():
    text = request.args.get("text")
    lang = request.args.get("lang")
    if not text:
        return False
    if not lang:
        lang = "en"
    play_tts(text, lang=lang)
    return text

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0', port=9000)

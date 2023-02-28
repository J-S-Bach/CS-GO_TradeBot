import js2py

class SteamApi:
    def __init__(self):
        js2py.translate_file('./JSSteamHandler/SteamHandler.js', "./translatedJS.py")
        try:
            from translatedJS import CsGoHandler
        except ImportError:
            pass

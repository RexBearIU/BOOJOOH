from ..logger import Logger
import tagui as t

class BotInterface(object):
    def __init__(self) -> None:
        self.logger = Logger()

        t.init(chrome_browser=False)
        t.error(True)
        t.debug(True)
import asyncio
from pyppeteer import launch
from datetime import datetime
from ._core import Action,InvalidUrlError
import validators.url as _url
class web_screenshot(Action):
    def __init__(self,url:str) -> None:
        # add window landscape config later.
        invalid = _url(url,public=True)
        if not invalid:
            raise InvalidUrlError('URL invalid, please check your URL carefully.')

        self.url = url

    def _now(self):
        # asyncio.get_event_loop().run_until_complete(web_screenshot._get_screenshot(self.url))
        result = asyncio.run(web_screenshot._get_screenshot(self.url))

    @staticmethod
    async def _get_screenshot(url):
        browser = await launch()
        print('🤖 : Launching browser... Please wait for a while then you will see the result.')
        page = await browser.newPage()
        agent =	'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        view_port = {
            # 'name': 'iPhone 8 Plus',
            'width': 414,
            'height': 736,
            'deviceScaleFactor': 3,
            'isMobile': True,
            'hasTouch': True,
            'isLandscape': False,
        }
        await page.setViewport(view_port)
        await page.setUserAgent(agent)

        # await page.emulate(view_port)

        await page.goto(url,options={'waitUntil':'networkidle2'})
        # time.sleep(1)
        await page.screenshot({'path': f'screenshot{datetime.now().strftime("%m-%d_%H:%M:%S")}.png'})
        await browser.close()


class open(Action):
    def __init__(self) -> None:
        pass

    def _now(self):
        pass


class alert(Action):
    '''
    Shit! It's in the docker. 
    '''

    # @staticmethod
    # def extract_msg(msg:Dict):
    #   t = msg.get('title')
    #   c = msg.get('message')
    #   a = msg.get('audio') 
    #   return t,c,a

    # def __init__(self,msg:Dict) -> None:
    #   self.notify = Notify()
    #   t,c,a = alert.extract_msg(msg)


    # def _now(self):c
    #   pass
    pass

class get_cat(Action):
    '''
    https://thatcopy.pw/catapi/rest/
    '''



class get_random_wallpaper(Action):
    pass

class use_browser(Action):

    def __init__(self,url,code_path) -> None:
        self.url = url
        self.code = self._read_from_path(code_path)


    def _read_from_path(self,code_path):
        return ''

    def _swtich_viewport(self):
        if '':
            pass

        elif '':
            pass
        elif '':
            pass
        return

    @staticmethod
    async def _touch_web(url,code):
        size = {}
        options={"waitUntil": "networkidle2"}
        browser = await launch()
        page = await browser.newPage()
        await page.setViewport(size)
        await page.goto(url,options=options)
        res = await page.evaluate(code)
        return res


    def _now(self):
        asyncio.get_event_loop().run_until_complete(use_browser._touch_web(self.url,self.code))



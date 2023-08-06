from pprint import pprint
from typing import Dict
import httpx
from ._core import Action, InvalidUrlError
from playwright.sync_api import sync_playwright
from pyquery import PyQuery
from datetime import datetime, time
import validators.url as _url
from datetime import datetime
import base64

YOU_API = 'http://127.0.0.1:8000/search/'  # fake api
OCR_API = 'http://127.0.0.1:8000/ocr/'  # fake api


class web_screenshot(Action):
    def __init__(self, url) -> None:
        self.url = url

    def _now(self):
        web_screenshot._web_screenshot(self.url)

    @staticmethod
    def _web_screenshot(url):
        print(
            '🤖 : Launching browser... Please wait for a while then you will see the'
            ' result.'
        )
        with sync_playwright() as p:
            iphone_11 = p.devices["iPhone 11 Pro"]
            browser_type = p.chromium
            browser = browser_type.launch(headless=True)
            context = browser.new_context(**iphone_11)
            page = context.new_page()
            page.set_viewport_size({"width": 375, "height": 635})
            page.goto(url, wait_until="networkidle")
            # page.screenshot(path=f'./example-{browser_type.name}haha.png')
            page.screenshot(
                path=f'screenshot{datetime.now().strftime("%m-%d_%H:%M:%S")}.png'
            )
            browser.close()


class get_now_temp(Action):
    def __init__(self, city: str, lang: str = 'en', ascii_graphs: bool = True) -> None:
        '''
        :param city: 城市的名称，英文/汉语拼音/中文均可
        :param lang: ascii 天气图形中描述天气状况的语言，例：zh-中文; en-英文

        '''
        self.city = city
        self.ascii_graphs = ascii_graphs
        self.lang = lang

    def _now(self):
        # return asyncio.run(get_now_temp.get_weather(self.city,ascii_graphs=self.ascii_graphs))
        return _get_weather(self.city, ascii_graphs=self.ascii_graphs, lang=self.lang)


def _get_weather(city, ascii_graphs, lang):
    res = httpx.get(
        f'http://wttr.in/{city}?lang={lang}{ "&T0" if ascii_graphs else "&format=j1"}'
    )
    if ascii_graphs:
        pq = PyQuery(res.text)
        result = pq.find('pre')
        return result.text(squash_space=False)
    temp = res.json().get('current_condition')
    return temp[0].get('FeelsLikeC')


class get_simple_temp(Action):
    def __init__(self, city) -> None:
        self.city = city

    def _now(self):
        r = _get_weather(self.city, ascii_graphs=False, lang='zh')
        assert isinstance(r, str)
        return float(r)


class translate(Action):
    def __init__(self, q, full=False):
        self.q = q
        self.full = full

    def _now(self):
        result = httpx.get(YOU_API + self.q)
        result = result.json()
        assert isinstance(result, dict)
        result = _clearify(result)
        explains = result.get('explains')
        if explains and not self.full:
            return explains
        if explains and self.full:
            return result
        # if self.full:
        #     return result
        else:
            return result["one_line"][0]


def _clearify(result):
    # pprint(result)
    basic = result.get('basic')
    clean_d = {}
    if basic:
        clean_d['explains'] = basic.get('explains')
        clean_d['web'] = result.get('web')
        clean_d['simple_translation'] = result.get('translation')[0]
        clean_d['web'] = result.get('web')
        clean_d['exam_type'] = basic.get('exam_type')
        clean_d['us-phonetic'] = basic.get('us-phonetic')
        clean_d['uk-phonetic'] = basic.get('uk-phonetic')
        clean_d['wfs'] = basic.get('wfs')
        clean_d['web_dict'] = result.get('webdict').get('url')
    else:
        clean_d["one_line"] = result["translation"]

    # covnert None to an empty string
    for k in clean_d.keys():
        if clean_d[k] == None:
            clean_d[k] = ''
    return clean_d


class simple_translate(Action):
    def __init__(self, q) -> None:
        self.q = q

    def _now(self):
        result = httpx.get(YOU_API + self.q)
        result = result.json()
        assert isinstance(result, dict)
        result = _clearify(result)
        return result.get('simple_translation')


class easy_ocr(Action):
    def __init__(self, path: str):
        with open(path, 'rb') as f:
            q = base64.b64encode(f.read())
            self.q = q.decode('utf-8')

    def _now(self):
        text_list = []
        result = httpx.post(OCR_API, json={'img': self.q, "name": 'image'})
        result = result.json()
        assert isinstance(result, dict)
        items = result["Result"]['regions']
        for item in items:
            # pprint.pprint(item)
            for l in item['lines']:
                # pprint.pprint(l['text'])
                text_list.append(l['text'])

        return text_list

import json
import time

from lxml.html import etree

from config import sec
from tools import Aio, process_video, get_logger


class Twitcasting:
    def __init__(self):
        self.aio = Aio()
        self.logger = get_logger(__name__)

    async def live_info(self, twitcasting_id):
        live_js = json.loads(await self.aio.main(
            f"https://twitcasting.tv/streamserver.php?target={twitcasting_id}&mode=client", 'get'))
        is_live = live_js['movie']['live']
        vid = str(live_js['movie']['id'])
        live_info = {"Is_live": is_live,
                     "Vid": vid}
        return live_info

    async def get_hsl(self, twitcasting_id, live_info):
        html = await self.aio.main(f"https://twitcasting.tv/{twitcasting_id}", "get")
        dom = etree.HTML(html)
        title = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/h2/span[3]/a/text()')[0]
        title += '|' + live_info.get('Vid')
        ref = f"https://twitcasting.tv/{twitcasting_id}/metastream.m3u8"
        target = f"https://twitcasting.tv/{twitcasting_id}"
        date = time.strftime("%Y-%m-%d", time.localtime())
        return {'Title': title,
                'Ref': ref,
                'Target': target,
                'Date': date}

    async def check(self, twitcasting_id):
        live_info = await self.live_info(twitcasting_id)
        if live_info.get('Is_live'):
            result = await self.get_hsl(twitcasting_id, live_info)
            await process_video(result, "Twitcasting")
        else:
            self.logger.info(f'Not found Live, after {sec}s checking')
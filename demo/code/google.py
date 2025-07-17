import asyncio
from typing import Optional, List

from demo.code.config import GOOGLE_COOKIES, IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Google, Network
from PicImageSearch.model import GoogleResponse
from PicImageSearch.sync import Google as GoogleSync

url = f"{IMAGE_BASE_URL}/test01.jpg"
file = get_image_path("test01.jpg")
base_url = "https://www.google.com"

# 收集所有结果
all_results = []


@logger.catch()
async def demo_async() -> None:
    global all_results
    all_results = []  # 重置结果列表

    async with Network(proxies=PROXIES, cookies=GOOGLE_COOKIES) as client:
        google = Google(base_url=base_url, client=client)
        resp = await google.search(file=file)
        collect_results(resp)
        resp2 = await google.next_page(resp)
        collect_results(resp2)
        if resp2:
            resp3 = await google.pre_page(resp2)
            collect_results(resp3)

    # 一次性输出前20个结果
    show_all_results()


def collect_results(resp: Optional[GoogleResponse]) -> None:
    global all_results

    if not resp or not resp.raw:
        return

    all_results.extend(resp.raw)


def show_all_results() -> None:
    global all_results

    # 只显示前20个结果
    results_to_show = all_results[:20]

    for i, result in enumerate(results_to_show, 1):
        logger.info(f"结果 {i}:")
        logger.info(f"标题: {result.title}")
        logger.info(f"URL: {result.url}")
        logger.info("-" * 30)


if __name__ == "__main__":
    asyncio.run(demo_async())

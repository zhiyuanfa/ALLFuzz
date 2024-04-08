import aiohttp
import asyncio
import aiofiles
import string
import random
from datetime import datetime

def generate_random_subdomain(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

async def fetch_status(url, session, semaphore, timeout=5):
    try:
        async with semaphore:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                return url, response.status
    except Exception:
        return url, None

async def check_wildcard_resolution(target, session, semaphore):
    tasks = []
    for _ in range(5):  # 生成并检查5个垃圾域名
        random_subdomain = generate_random_subdomain()
        url = f"http://{random_subdomain}.{target}"
        tasks.append(fetch_status(url, session, semaphore))

    results = await asyncio.gather(*tasks)
    return all(status == 200 for _, status in results if status is not None)

async def brute_force_subdomains(target, session, semaphore):
    subdomains = {}
    async with aiofiles.open('../brute/subdomain.txt', 'r', encoding='utf-8') as file:
        async for sub in file:
            sub = sub.strip()
            url = f"http://{sub}.{target}"
            _, status = await fetch_status(url, session, semaphore)
            if status and not str(status).startswith("40"):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                subdomains[url] = (current_time, status)

    return subdomains

async def subdomain_brute(target, timeout=10):
    semaphore = asyncio.Semaphore(20)

    async with aiohttp.ClientSession() as session:
        wildcard_present = await check_wildcard_resolution(target, session, semaphore)
        if wildcard_present:
            print(f"{target}存在泛解析")
            return {}

        subdomains = await brute_force_subdomains(target, session, semaphore)
        return subdomains
import asyncio

from injector import async_launch_persistent_context
from playwright.async_api import async_playwright
from ultis import create_fingerprint, load_fingerprint


class HcmAutomation:
    def __init__(self):
            pass

    async def launch(self,playwright, profile, proxy):

        fingerprint_data = load_fingerprint(profile)
        # print(fingerprint_data)
        browser = await async_launch_persistent_context(playwright,
                                                        profile=profile,
                                                        proxy=proxy,
                                                        fingerprint=fingerprint_data,
                                                        )

        return browser

    async def close(self, browser):
        await browser.close()

    async def create_profile(self, profile, proxy=None, os='windows'):
        async with async_playwright() as playwright:
            fingerprint_data = create_fingerprint(profile, os)
            browser = await async_launch_persistent_context(playwright,
                                                            profile=profile,
                                                            proxy=proxy,
                                                            fingerprint=fingerprint_data,
                                                            )
            await browser.close()
            return


async def main():
    async with async_playwright() as playwright:
        hcm = HcmAutomation()
        # await hcm.create_profile('iso_test', 'http://3.83.216.202:1558','ios')
        browser = await hcm.launch(playwright, 'iso_test','http://3.83.216.202:1558')
                                                        
        page = await browser.new_page()
        await page.goto("https://www.facebook.com/")
        await asyncio.sleep(200)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())

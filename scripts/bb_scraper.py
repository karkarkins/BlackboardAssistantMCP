"""
Future Extensions:
Integrate with context_builder.py to store assignment context in json format.
"""

import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

load_dotenv()

BB_USERNAME = os.getenv("BB_USERNAME")
BB_PASSWORD = os.getenv("BB_PASSWORD")
BB_LOGIN_URL = os.getenv("BB_LOGIN_URL")

async def scrape_blackboard():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("Navigating to Blackboard login page...")
        await page.goto(BB_LOGIN_URL)

        print("Clicking HERE link to go to student login...")
        await page.click("text=HERE")

        await page.wait_for_selector('input[name="loginfmt"]')

        await page.fill('input[name="loginfmt"]', BB_USERNAME)
        await page.click('#idSIButton9')
        await page.fill('input[name="passwd"]', BB_PASSWORD)
        await page.click('#idSIButton9')

        await page.wait_for_load_state('networkidle')

        print("Logged in successfully. Navigating to courses page...")

        await page.wait_for_selector('a[href="https://ncat.blackboard.com/ultra/course"]')

        await page.click('a[href="https://ncat.blackboard.com/ultra/course"]')
        await page.wait_for_load_state('networkidle')

        # Wait for course tiles to appear
        await page.wait_for_selector('a.course-title')
        
        # focus the main scrollable list
        await page.click("label:has-text('View Course List')")

        # then scroll with keyboard
        for _ in range(5):   # adjust how many times
            await page.keyboard.press("PageDown")
            await asyncio.sleep(0.5)
                

        course_links = await page.query_selector_all('a.course-title')

        results = []

        CURRENT_TERM = "202610"

        filtered_links = []
        for link in course_links:
            course_title = await link.inner_text()
            if CURRENT_TERM in course_title:
                filtered_links.append(link)

        print(f"Found {len(filtered_links)} courses:")
        for course_link in filtered_links:
            course_title = await course_link.inner_text()
            print(f"Scraping course: {course_title}")

            await course_link.click()
            await asyncio.sleep(2)
            await page.wait_for_load_state('networkidle')

            course_data = {
                "course_name": course_title,
                "course_url": page.url,
                "contents": [],
                "discussions": []
            }
            
            print(course_data)
            print("---------------------------------------------")


            # Scrape course content here
            try:
                print(" Accessing Course Content...")

                # Find the classic course iframe
                frame = page.frame(name="classic-learn-iframe")

                # Verify we found it
                if frame:
                    element = await frame.query_selector("span[title='Course Content']")
                    if element:
                        await element.click()
                        print("Clicked Course Content")
                    else:
                        print("Course Content not found inside iframe.")
                else:
                    print("classic-learn-iframe not found.")
                
                """
                for frame in page.frames:
                    print("Frame name:", frame.name, "URL:", frame.url)

                elements = await page.query_selector_all("span")
                print(f" Found {len(elements)} elements with titles:")
                for el in elements:
                    text = await el.inner_text()
                    print("SPAN:", text)
                """

                if await page.query_selector("li a:has(span[title='Course Content'])"):
                    print("Found Course Content link, clicking...")
                    await page.click("a[title='Course Content']")
                    await page.wait_for_load_state('networkidle')

                    content_items = await page.query_selector_all("div.content-list")
                    for item in content_items:
                        text = await item.inner_text()
                        print(f"  Found content item: {text}")
                        if text:
                            course_data["contents"].append({"title": text})
                    await page.click('button.bb-close')
            except Exception as e:
                print(f" No Course Content found for {course_title}: {e}")

            results.append(course_data)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_blackboard())

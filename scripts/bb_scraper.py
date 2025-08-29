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
        course_links = await page.query_selector_all('a.course-title')

        print(f"Found {len(course_links)} courses:")
        for link in course_links:
            course_title = await link.inner_text()
            print("-", course_title.strip())

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_blackboard())

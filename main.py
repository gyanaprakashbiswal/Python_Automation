import argparse
import sys
from selenium.webdriver.common.by import By

from config import DEFAULT_SCRAPE_URL, TARGET_LOGIN_URL, TEST_USERNAME, TEST_PASSWORD
from modules.logger import setup_logger
from modules.scraper import WebScraper
from modules.browser_bot import BrowserBot
from modules.utils import save_json, save_csv

logger = setup_logger(__name__)

def run_scraper(url: str):
    print(f"\n--- Running Web Scraper on {url} ---")
    scraper = WebScraper()
    data = scraper.run(url)
    
    if data:
        print("\n[Scraper Summary]")
        print(f"Title: {data.get('title')}")
        print(f"Headings Found: {len(data.get('headings', []))}")
        print(f"Links Found: {len(data.get('links', []))}")
        print(f"Paragraphs Found: {len(data.get('paragraphs', []))}")
        
        # Save results by default
        save_json(data, "scraper_results.json")
        
        # Flatten for CSV
        csv_data = [
            {"Type": "Title", "Content": data.get("title")},
            {"Type": "Total Headings", "Content": len(data.get("headings", []))},
            {"Type": "Total Links", "Content": len(data.get("links", []))}
        ]
        save_csv(csv_data, "scraper_summary.csv")
        print("\nResults saved to data directory.")
    else:
        print("\nScraping failed or returned no data. Check logs.")

def run_selenium():
    print("\n--- Running Selenium Automation ---")
    bot = BrowserBot(headless=False) # Set to True to run invisibly
    
    try:
        bot.start_browser()
        
        # Example 1: Visit a page and take screenshot
        bot.visit("https://example.com")
        bot.capture_screenshot("example_home.png")
        
        # Example 2: Login automation (Using a public test site)
        print(f"\nAttempting login at {TARGET_LOGIN_URL}")
        # Locators for the-internet.herokuapp.com/login
        user_loc = (By.ID, "username")
        pass_loc = (By.ID, "password")
        submit_loc = (By.CSS_SELECTOR, "button[type='submit']")
        
        bot.login(TARGET_LOGIN_URL, user_loc, pass_loc, submit_loc, TEST_USERNAME, TEST_PASSWORD)
        bot.capture_screenshot("after_login.png")
        
        # Extract flash message text to verify login status
        flash_loc = (By.ID, "flash")
        text = bot.extract_text(flash_loc)
        print(f"\nExtracted UI Text (Flash Message): {text.strip()}")
        
        # Save extracted text
        save_json({"login_status_message": text}, "selenium_extracted.json")

    except Exception as e:
        logger.error(f"Selenium automation encountered an error: {e}")
        print(f"\nError: {e}")
    finally:
        bot.close_browser()
        print("\nSelenium sequence finished.")

def interactive_menu():
    while True:
        print("\n" + "="*50)
        print("    PYTHON AUTOMATION TOOLKIT CLI    ")
        print("="*50)
        print("1. Run Web Scraper")
        print("2. Run Selenium Automation")
        print("3. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            url = input(f"Enter URL to scrape (default: {DEFAULT_SCRAPE_URL}): ")
            url = url.strip() or DEFAULT_SCRAPE_URL
            run_scraper(url)
        elif choice == '2':
            run_selenium()
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="Python Automation Toolkit")
    parser.add_argument("--scraper", action="store_true", help="Run the Web Scraper module")
    parser.add_argument("--selenium", action="store_true", help="Run the Selenium Automation module")
    parser.add_argument("--url", type=str, default=DEFAULT_SCRAPE_URL, help="Target URL for scraping")
    
    args = parser.parse_args()

    # If CLI arguments are provided, run the specific module
    if args.scraper:
        run_scraper(args.url)
    elif args.selenium:
        run_selenium()
    else:
        # Otherwise, launch the interactive CLI menu
        try:
            interactive_menu()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()

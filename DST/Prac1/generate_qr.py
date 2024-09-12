from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
import time


def get_QR(text):
    # Set up Chrome options (or use Firefox options if you prefer)
    chrome_options = webdriver.ChromeOptions()

    # TODO: FIX THIS, arguments to disable browser choice pop-ups or similar not working
    chrome_options.add_experimental_option(
        "excludeSwitches",
        [
            "disable-hang-monitor",
            "disable-prompt-on-repost",
            "disable-background-networking",
            "disable-sync",
            "disable-translate",
            "disable-web-resources",
            "disable-client-side-phishing-detection",
            "disable-component-update",
            "disable-default-apps",
            "disable-zero-browsers-open-for-tests",
        ],
    )

    # Create the WebDriver instance (for Chrome)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    # Path to your WebDriver (adjust to where you downloaded the ChromeDriver)
    # webdriver_service = Service("/Applications/chromedriver-mac-arm64/chromedriver")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

    try:
        # Step 1: Navigate to the QR code generator website
        driver.get("https://the-qrcode-generator.com")

        # Step 2: Locate the "Plain Text" button by its class name and click on it
        plain_text_button = driver.find_element(
            By.XPATH, '//*[@id="campaign-list"]/div[5]'
        )
        plain_text_button.click()

        main_window_handle = driver.current_window_handle

        print("Successfully clicked on the 'Plain Text' button!")

        text_input = driver.find_element(
            By.XPATH, '//*[@id="widget_input_tab_content"]/div/textarea'
        )
        text_input.send_keys(text)  # Replace with your desired text

        # Step 4: Locate and click the first "Download" button using XPATH
        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="downloadBtn"]'))
        )
        download_button.click()

        print("First download button clicked successfully!")

        # Get all window handles
        # Wait for the new window/tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Get all window handles
        all_window_handles = driver.window_handles

        # Switch to the new window/tab
        for handle in all_window_handles:
            if handle != main_window_handle:
                driver.switch_to.window(handle)
                break

        modal = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/section[5]/div/div[4]/button[2]")
            )
        )
        # TODO: fix this last click, not working
        time.sleep(20)  # Wait for 5 seconds to download the file

        if modal.is_displayed():
            final_download_button = modal.find_element(
                (By.XPATH, '//*[@id="downloadBtn"]')
            )

            final_download_button.click()

        print("Download initiated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

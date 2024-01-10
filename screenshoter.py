from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_autoinstaller import install
from tqdm import tqdm
import time
import os

def take_screenshot(url, output_path):
    options = Options()
    options.headless = True

    # Use the installed Chromedriver
    install()

    # Specify the path to Chromedriver
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Adjust this based on your Chrome installation path

    # Set the window size for fullscreen
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    try:
        driver.get(url)

        # Take screenshot of the first page
        driver.save_screenshot(output_path)
        print(f"Screenshot saved for {url} at {output_path}")

    except Exception as e:
        print(f"Error taking screenshot for {url}: {e}")

    finally:
        driver.quit()

def main():
    subdomains_file = input("Enter the path to the subdomains file: ")

    if not os.path.isfile(subdomains_file):
        print(f"Error: File '{subdomains_file}' not found.")
        return

    output_directory = input("Enter the path to save the screenshots: ")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(subdomains_file, "r") as file:
        subdomains = file.read().splitlines()

    for subdomain in tqdm(subdomains, desc="Progress", unit="subdomain"):
        url = f"http://{subdomain}"
        output_path = os.path.join(output_directory, f"{subdomain.replace('.', '_')}_screenshot.png")
        take_screenshot(url, output_path)

if __name__ == "__main__":
    main()

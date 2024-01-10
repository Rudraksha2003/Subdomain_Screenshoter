import asyncio
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import csv
import os
from webdriver_manager.firefox import GeckoDriverManager

async def capture_screenshot(subdomain, output_path=None):
    options = Options()
    options.add_argument('-headless')  # Run Firefox in headless mode
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

    try:
        driver.get(subdomain)

        domain_name = subdomain.replace('http://', '').replace('https://', '').replace('.', '_')
        screenshot_filename = f"{domain_name}.png"

        if output_path:
            screenshot_filename = os.path.join(output_path, screenshot_filename)

        title = driver.title
        screenshot = driver.get_screenshot_as_png()

        with open(screenshot_filename, "wb") as f:
            f.write(screenshot)

        return subdomain, title, screenshot_filename

    except Exception as e:
        return subdomain, str(e), None

    finally:
        driver.quit()

async def capture_screenshots(subdomain_list, output_path=None, num_threads=5):
    results = []

    with tqdm(total=len(subdomain_list), desc="Capturing Screenshots") as pbar:
        async def capture(subdomain):
            nonlocal results
            result = await capture_screenshot(subdomain, output_path)
            results.append(result)
            pbar.update(1)

        await asyncio.gather(*[capture(subdomain) for subdomain in subdomain_list])

    return results

def save_results_to_csv(results, csv_filename='screenshot_results.csv'):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Subdomain', 'Title', 'Screenshot Filename']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({'Subdomain': result[0], 'Title': result[1], 'Screenshot Filename': result[2]})

def create_requirements_txt():
    with open('requirements.txt', 'w') as req_file:
        req_file.write("selenium==3.141.0\n")
        req_file.write("tqdm==4.62.3\n")
        req_file.write("webdriver-manager==3.5.0\n")

if __name__ == "__main__":
    try:
        print("""
             Welcome to Subdomain Screenshot Capture Tool
             Press 1 for capturing screenshots of a list of subdomains
             Press 2 to exit
        """)

        option = int(input("[+] Enter the option: "))

        if option == 1:
            subdomain_list_path = input("[+] Enter the file path containing subdomains: ")
            subdomains = open(subdomain_list_path, "r").read().splitlines()
            output_path = input("[+] Enter the path to save the screenshots: ")
            num_threads = int(input("[+] Enter the number of threads (default is 5): ") or 5)

            loop = asyncio.get_event_loop()
            screenshot_results = loop.run_until_complete(capture_screenshots(subdomains, output_path=output_path, num_threads=num_threads))
            save_results_to_csv(screenshot_results)
            create_requirements_txt()

            print(f"\nScreenshots saved for {len(screenshot_results)} subdomains.")
            print(f"Results saved to {os.path.abspath('screenshot_results.csv')}")
            print("Requirements file 'requirements.txt' created.")

        elif option == 2:
            print("Exiting the tool.")

        else:
            print("Invalid option. Please choose either 1 or 2.")

    except KeyboardInterrupt:
        print("\nScript interrupted. Thank you for using the tool.")

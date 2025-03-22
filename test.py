import os
import csv
import signal
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import functools
import psutil

# Force immediate flushing of print statements
print = functools.partial(print, flush=True)

# Global variable to track the last processed pin
last_processed_pin = 0

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print("\nCtrl+C detected! Saving progress and exiting gracefully...")
    with open("progress.txt", "w") as f:
        f.write(str(last_processed_pin))
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Load progress if the file exists
if os.path.exists("progress.txt"):
    with open("progress.txt", "r") as f:
        last_processed_pin = int(f.read().strip())
    print(f"Resuming from pin {last_processed_pin + 1}")
else:
    last_processed_pin = 0

# Configure Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.binary_location = "/usr/bin/google-chrome-stable"
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Initialize Chrome driver with Service
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Rest of your script...

try:
    # Start virtual display (required for headless on Linux)
    print("Starting virtual display...")
    os.system("Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &")
    os.environ['DISPLAY'] = ':99'

    for folder_name, folder_data in xpaths["parent_folders"].items():
        print(f"\n=== Processing parent folder: {folder_name} ===")
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        print(f"Attempting to click parent folder: {folder_name}")
        if safe_click(closed_folder):
            print(f"Successfully opened parent folder: {folder_name}")
        time.sleep(1)

        for subfolder_name, subfolder_data in folder_data["subfolders"].items():
            try:
                print(f"\n--- Processing subfolder: {subfolder_name} ---")
                subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
                print(f"Attempting to click subfolder: {subfolder_name}")
                if safe_click(subfolder):
                    print(f"Successfully opened subfolder: {subfolder_name}")
                time.sleep(1)

                pins = []
                for index in range(last_processed_pin + 1, subfolder_data['pins'] + 1):
                    try:
                        global_status['current_pin'] = f"{index}/{subfolder_data['pins']}"
                        global_status['current_folder'] = f"{folder_name} > {subfolder_name}"
                        print_status()

                        # Clear the console before printing the "Processing pin" message
                        os.system('clear')
                        print(f"\nProcessing pin {index} of {subfolder_data['pins']}")

                        # Update the last processed pin
                        last_processed_pin = index

                        location_xpath = f'{subfolder_data["location_base"]}[{index}]'
                        
                        # Add retry logic for element location
                        for attempt in range(3):
                            try:
                                location = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
                                break
                            except:
                                print(f"Element not found, retrying ({attempt + 1}/3)")
                                driver.execute_script("window.scrollBy(0, 100);")
                                time.sleep(1)
                        else:
                            print(f"Skipping pin {index} - not found after 3 attempts")
                            continue

                        print(f"Clicking pin #{index}")
                        if not safe_click(location):
                            continue

                        time.sleep(1)
                        name = driver.find_element(By.XPATH, xpaths["name"]).text
                        description = driver.find_element(By.XPATH, xpaths["description"]).text
                        print(f"Retrieved name: {name}")

                        nav_button = driver.find_element(By.XPATH, xpaths["navigation_button"])
                        print("Clicking navigation button")
                        safe_click(nav_button)

                        if switch_to_new_tab():
                            current_url = driver.current_url
                            print(f"New tab URL: {current_url}")
                            lat, lon = extract_coordinates(current_url)
                            print(f"Coordinates for pin {index}: Lat {lat}, Lon {lon}")
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            print("Returned to main tab")
                        else:
                            lat, lon = None, None
                            print("Failed to switch to new tab")

                        pins.append({
                            "Name": name,
                            "Description": description,
                            "Type": subfolder_name,
                            "Latitude": lat,
                            "Longitude": lon,
                            "Index": index
                        })

                        back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
                        print("Clicking back button")
                        safe_click(back_button)
                        time.sleep(1)

                        global_status['total_pins_processed'] += 1
                        global_status['success_rate'] = global_status['total_pins_processed'] / index

                    except Exception as e:
                        print(f"Error processing pin {index}: {str(e)}")
                        driver.save_screenshot(f"error_{index}.png")

                filename = generate_filename(folder_name, subfolder_name)
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Name", "Description", "Type", "Latitude", "Longitude", "Index"])
                    writer.writeheader()
                    writer.writerows(pins)
                print(f"Successfully saved {len(pins)} entries to {filename}")

            except Exception as e:
                print(f"Subfolder error: {str(e)}")

except Exception as e:
    print(f"Main error: {str(e)}")
finally:
    driver.quit()
    print("Browser closed")
    os.system("pkill Xvfb")  # Clean up virtual display

    # Clean up progress file on completion
    if os.path.exists("progress.txt"):
        os.remove("progress.txt")

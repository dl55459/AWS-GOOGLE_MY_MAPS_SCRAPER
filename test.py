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

# Open the Google My Maps link
url = "https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1"
print("Navigating to URL...")
driver.get(url)

# Wait for the map to load
wait = WebDriverWait(driver, 20)

# Define all XPaths at the beginning for better visibility
xpaths = {
    # Parent folders and their subfolders
    "parent_folders": {
        "Ghost Towns": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "Archaeological Site": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div',
                    'pins': 95
                },
                "Dammed": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[4]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div',
                    'pins': 60
                },
                "Abandoned Due to Disaster": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div',
                    'pins': 29
                },
                "Unbuilt Developments": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[6]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[6]/div[2]/div',
                    'pins': 16
                },
                "Ghost Towns": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[7]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[7]/div[2]/div',
                    'pins': 1196
                }
            }
        },
        "Abandoned/Historic Places": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "Abandoned Buildings": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[2]/div',
                    'pins': 88
                },
                "Abandoned Military Property": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[4]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[4]/div[2]/div',
                    'pins': 75
                },
                "Historical Marker": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[5]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[5]/div[2]/div',
                    'pins': 64
                },
                "Abandoned Mine": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[6]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[6]/div[2]/div',
                    'pins': 54
                },
                "Abandoned Place": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[7]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[7]/div[2]/div',
                    'pins': 50
                },
                "Theme Park": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[8]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[8]/div[2]/div',
                    'pins': 41
                },
                "Abandoned Industrial Plant": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[9]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[9]/div[2]/div',
                    'pins': 35
                },
                "Memorial": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[10]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[10]/div[2]/div',
                    'pins': 28
                },
                "Abandoned Bridge": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[11]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[11]/div[2]/div',
                    'pins': 22
                },
                "Historical Site": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[12]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[12]/div[2]/div',
                    'pins': 17
                },
                "Abandoned Power Plant": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[13]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[13]/div[2]/div',
                    'pins': 11
                },
                "Abandoned Mine2": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[14]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[14]/div[2]/div',
                    'pins': 2
                },
                "Abandoned Bridge (Demolished)": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[15]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[15]/div[2]/div',
                    'pins': 1
                }
            }
        }
    },
    # Navigation button in the details panel
    "navigation_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[3]/div',

    # Back button to return to the main side panel
    "back_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div'
}

# Global status tracking
global_status = {
    'total_pins_processed': 0,
    'current_pin': None,
    'current_folder': None,
    'start_time': time.time(),
    'success_rate': 0
}

def print_status():
    elapsed = time.time() - global_status['start_time']
    print(f"\n――――――――――――――――――――――――――――――――――――――――――――")
    print(f"Current Folder: {global_status['current_folder']}")
    print(f"Processing Pin: {global_status['current_pin']}")
    print(f"Elapsed Time: {elapsed:.2f}s")
    print(f"Success Rate: {global_status['success_rate']:.1%}")
    print(f"Memory Usage: {psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.2f} MB")
    print(f"――――――――――――――――――――――――――――――――――――――――――――\n")

def switch_to_new_tab(timeout=10):
    print("Attempting to switch to new tab...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            print("Successfully switched to new tab")
            return True
        time.sleep(0.5)
    print("Failed to switch to new tab")
    return False

def ensure_element_visible(element):
    try:
        driver.execute_script("arguments[0].style.zIndex = '99999';", element)
        driver.execute_script("arguments[0].style.position = 'relative';", element)
    except Exception as e:
        print(f"Visibility adjustment failed: {str(e)}")

def safe_click(element, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            ensure_element_visible(element)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", element)
            print(f"Successfully clicked element after {attempt + 1} attempts")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error clicking element - {str(e)}")
            time.sleep(2)
    print("Max retries reached. Skipping this element.")
    return False

def extract_coordinates(url):
    try:
        if "dir//" in url:
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
            print(f"Extracted coordinates - Lat: {lat}, Lon: {lon}")
            return float(lat), float(lon)
        print("No coordinates found in URL")
        return None, None
    except Exception as e:
        print(f"Coordinate extraction error: {str(e)}")
        return None, None

def generate_filename(parent_folder, child_folder):
    # Create OUTPUT directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "OUTPUT")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    parent = parent_folder.replace(" ", "_").replace("/", "_").lower()
    child = child_folder.replace(" ", "_").replace("/", "_").lower()
    return os.path.join(output_dir, f"{parent}_{child}.csv")

def find_name_and_description_xpaths(driver):
    try:
        divs = driver.find_elements(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div')
        name = "N/A"
        description = "N/A"

        for div in divs:
            try:
                label = div.find_element(By.XPATH, './div[1]').text.lower()
                value_element = div.find_element(By.XPATH, './div[2]')
                
                if value_element:
                    value = value_element.text.strip() if value_element.text.strip() else value_element.get_attribute('href') or "N/A"
                else:
                    value = "N/A"
                
                if "name" in label:
                    name = value
                elif "description" in label:
                    description = value
            except Exception as e:
                print(f"Skipping div due to error: {str(e)}")
                continue  
        
        return name, description
    except Exception as e:
        print(f"Error finding name and description: {str(e)}")
        return "N/A", "N/A"

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
                        
                        # Dynamically find name and description XPaths
                        name_xpath, description_xpath = find_name_and_description_xpaths(driver)
                        
                        name = "N/A"
                        description = "N/A"
                        
                        if name_xpath:
                            name = driver.find_element(By.XPATH, name_xpath).text
                        if description_xpath:
                            description = driver.find_element(By.XPATH, description_xpath).text
                        
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

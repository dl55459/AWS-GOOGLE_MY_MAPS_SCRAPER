from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import psutil  # For memory usage
import datetime  # For execution time

# Configuration
output_folder = "output_ghost_csv"  # Folder to store CSV files (change as needed)
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage

# Set the path to ChromeDriver (installed in /usr/local/bin/chromedriver)
driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Google My Maps link
url = "https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1"
driver.get(url)

# Wait for the map to load
wait = WebDriverWait(driver, 20)  # Increased timeout for slow loading

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

    # Base XPath for the details panel
    "details_panel": '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div',
    # Navigation button in the details panel
    "navigation_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[3]/div',
    # Back button to return to the main side panel
    "back_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div'
}

# some folder structure:
# 1)
# "Ghost Towns": {
#     "closed": "//xpath/to/closed/folder",
#     "location_base": "//xpath/to/locations",
#     "pins": 100
# }
# 2)
# "Abandoned Places": {
#     "closed": "//xpath/to/parent/folder",
#     "subfolders": {
#         "Factories": {
#             "xpath": "//xpath/to/subfolder",
#             "location_base": "//xpath/to/locations",
#             "pins": 50
#         }
#     }
# }

# Define possible strings for name and description labels
possible_name_labels = ["name"]
possible_description_labels = ["description"]

# Function to log messages
def log_message(message):
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [Memory: {memory_usage:.2f} MB] {message}"
    print(log_entry)
    with open("log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

def safe_click(element, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
            element.click()
            return True
        except Exception as e:
            log_message(f"Attempt {attempt + 1}: Error clicking element - {str(e)}")
            time.sleep(2)
    log_message("Max retries reached. Skipping this element.")
    return False

# Function to extract coordinates from the URL
def extract_coordinates(url):
    try:
        if "dir//" in url:
            # Extract the part of the URL between "dir//" and "&"
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
            return float(lat), float(lon)
        else:
            return None, None
    except Exception as e:
        log_message(f"Error extracting coordinates from URL: {str(e)}")
        return None, None

# Function to extract name and description dynamically
def extract_name_and_description():
    name = "N/A"
    description = "N/A"
    try:
        # Find all div elements at any level within the details panel
        details_divs = driver.find_elements(By.XPATH, xpaths["details_panel"] + "//div")
        log_message("Searching for name and description in details panel...")
        for div in details_divs:
            text = div.text
            # Check for name labels
            for label in possible_name_labels:
                if label in text:
                    log_message(f"Found '{label}' label.")
                    name = div.find_element(By.XPATH, "./following-sibling::div[1]").text
                    log_message(f"Extracted name: {name}")
                    break
            # Check for description labels
            for label in possible_description_labels:
                if label in text:
                    log_message(f"Found '{label}' label.")
                    description = div.find_element(By.XPATH, "./following-sibling::div[1]").text
                    log_message(f"Extracted description: {description}")
                    break
    except Exception as e:
        log_message(f"Error extracting name or description: {str(e)}")
    return name, description

def process_folder(folder_name, folder_data):
    """Process a parent folder with optional subfolders"""
    try:
        log_message(f"═════════ PROCESSING PARENT FOLDER: {folder_name.upper()} ═════════")
        if not expand_folder(folder_name, folder_data):
            return

        if "subfolders" in folder_data and folder_data["subfolders"]:
            process_subfolders(folder_name, folder_data["subfolders"])
        else:
            process_direct_locations(folder_name, folder_data)

    except Exception as e:
        log_message(f"⚠️ Critical error processing folder {folder_name}: {str(e)}")


def expand_folder(folder_name, folder_data):
    """Expand the parent folder"""
    try:
        log_message(f"Looking for folder element using XPath: {folder_data['closed']}")
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        log_message("Found parent folder element. Attempting to expand...")
        if not safe_click(closed_folder):
            log_message(f"⚠️ Failed to expand parent folder: {folder_name}")
            return False
        log_message(f"✔ Successfully expanded parent folder: {folder_name}")
        time.sleep(1)
        return True
    except Exception as e:
        log_message(f"⚠️ Error expanding folder {folder_name}: {str(e)}")
        return False


def process_subfolders(folder_name, subfolders):
    """Process all subfolders within a parent folder"""
    log_message(f"Found {len(subfolders)} subfolders in {folder_name}")
    for subfolder_name, subfolder_data in subfolders.items():
        try:
            log_message(f"\n├── PROCESSING SUBFOLDER: {subfolder_name}")
            if not expand_subfolder(subfolder_name, subfolder_data):
                continue
            process_locations(subfolder_name, subfolder_data, folder_name)
        except Exception as e:
            log_message(f"│   ⚠️ Error processing subfolder {subfolder_name}: {str(e)}")


def expand_subfolder(subfolder_name, subfolder_data):
    """Expand a subfolder"""
    try:
        log_message(f"│   Looking for subfolder element using XPath: {subfolder_data['xpath']}")
        subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
        if not safe_click(subfolder):
            log_message(f"│   ⚠️ Failed to open subfolder: {subfolder_name}")
            return False
        log_message(f"│   ✔ Successfully opened subfolder: {subfolder_name}")
        time.sleep(1)
        return True
    except Exception as e:
        log_message(f"│   ⚠️ Error expanding subfolder {subfolder_name}: {str(e)}")
        return False


def process_direct_locations(folder_name, folder_data):
    """Process locations directly in a parent folder"""
    log_message(f"No subfolders found in {folder_name}, checking for direct locations...")
    if 'location_base' in folder_data:
        log_message(f"Found direct locations in parent folder. Processing {folder_data['pins']} locations...")
        for i in range(1, folder_data['pins'] + 1):
            log_message(f"└── Processing location {i}/{folder_data['pins']} in parent folder")
            process_location(folder_data['location_base'], i, folder_name)
    else:
        log_message(f"⚠️ No locations found in parent folder {folder_name}")


def process_locations(subfolder_name, subfolder_data, folder_name):
    """Process all locations within a subfolder"""
    log_message(f"│   Preparing to process {subfolder_data['pins']} locations...")
    for i in range(1, subfolder_data['pins'] + 1):
        log_message(f"│   └── Processing location {i}/{subfolder_data['pins']}")
        process_location(subfolder_data['location_base'], i, f"{folder_name}/{subfolder_name}")

def process_location(location_base, index, folder_path=""):
    try:
        log_message(f"\n{'='*50}")
        log_message(f"PROCESSING LOCATION {index} (XPath: {location_base}[{index}])")
        log_message(f"{'='*50}")

        # CLICK LOCATION
        location = wait.until(EC.element_to_be_clickable((By.XPATH, f'{location_base}[{index}]')))
        log_message("Location element found, attempting click...")

        if not safe_click(location):
            log_message("❌ Failed to click location")
            return False

        log_message("✅ Location clicked successfully")
        time.sleep(1)  # Wait for animation

        # WAIT FOR DETAILS PANEL
        try:
            wait.until(lambda d: d.find_element(By.XPATH, xpaths["details_panel"]).is_displayed())
            log_message("✅ Details panel appeared")
        except Exception as e:
            log_message(f"❌ Details panel failed to appear: {str(e)}")
            return False

        # EXTRACT DATA
        name, description = extract_name_and_description()

        # GET COORDINATES
        log_message("Attempting to get coordinates...")
        try:
            nav_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["navigation_button"])))
            safe_click(nav_button)
            log_message("✅ Navigation button clicked")

            # Switch to new tab
            driver.switch_to.window(driver.window_handles[1])
            log_message(f"New tab opened, current URL: {driver.current_url[:100]}...")

            # Get coordinates
            current_url = driver.current_url
            lat, lon = extract_coordinates(current_url)
            log_message(f"✅ Extracted coordinates: {lat}, {lon}")

            # Close tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            log_message("Returned to main tab")
        except Exception as e:
            log_message(f"❌ Error getting coordinates: {str(e)}")
            lat, lon = None, None
            try:
                driver.switch_to.window(driver.window_handles[0])
            except Exception:
                pass

        # SAVE DATA
        log_message("Saving location data...")
        save_location_data(folder_path, name, description, lat, lon, index)
        log_message("✅ Data saved successfully")

        # RETURN TO LIST
        try:
            back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
            safe_click(back_button)
            log_message("✅ Returned to location list")
            time.sleep(0.5)  # Wait for list to reload
        except Exception as e:
            log_message(f"❌ Error returning to list: {str(e)}")
            return False

        return True

    except Exception as e:
        log_message(f"❌ CRITICAL ERROR in process_location: {str(e)}")
        # Attempt recovery
        try:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
            safe_click(back_button)
        except Exception:
            log_message("Could not recover from error")
        return False

def save_location_data(folder_path, name, description, lat, lon, index):
    """Save location data to CSV"""
    clean_path = folder_path.replace(" ", "_").replace("/", "_").lower()
    filename = f"{clean_path}.csv" if clean_path else "locations.csv"
    filepath = os.path.join(output_folder, filename)

    data = {
        "Name": name,
        "Description": description,
        "Latitude": lat,
        "Longitude": lon,
        "Index": index
    }

    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def process_folder(folder_name, folder_data):
    """Process a parent folder with optional subfolders"""
    try:
        expand_parent_folder(folder_name, folder_data)
        if has_subfolders(folder_data):
            process_all_subfolders(folder_name, folder_data["subfolders"])
        else:
            process_direct_locations_in_folder(folder_name, folder_data)
    except Exception as e:
        log_message(f"Error processing folder {folder_name}: {str(e)}")


def expand_parent_folder(folder_name, folder_data):
    """Expand the parent folder"""
    closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
    safe_click(closed_folder)
    log_message(f"Processing folder: {folder_name}")
    time.sleep(1)


def has_subfolders(folder_data):
    """Check if the folder has subfolders"""
    return "subfolders" in folder_data and folder_data["subfolders"]


def process_all_subfolders(folder_name, subfolders):
    """Process all subfolders within a parent folder"""
    for subfolder_name, subfolder_data in subfolders.items():
        try:
            process_single_subfolder(folder_name, subfolder_name, subfolder_data)
        except Exception as e:
            log_message(f"Error processing subfolder {subfolder_name}: {str(e)}")


def process_single_subfolder(folder_name, subfolder_name, subfolder_data):
    """Process a single subfolder"""
    subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
    safe_click(subfolder)
    log_message(f"Processing subfolder: {subfolder_name}")
    time.sleep(1)
    process_locations_in_subfolder(folder_name, subfolder_name, subfolder_data)


def process_locations_in_subfolder(folder_name, subfolder_name, subfolder_data):
    """Process locations within a subfolder"""
    for i in range(1, subfolder_data['pins'] + 1):
        process_location(subfolder_data['location_base'], i, f"{folder_name}/{subfolder_name}")


def process_direct_locations_in_folder(folder_name, folder_data):
    """Process locations directly in a parent folder"""
    if 'location_base' in folder_data:  # Check if parent has direct locations
        for i in range(1, folder_data['pins'] + 1):
            process_location(folder_data['location_base'], i, folder_name)

# Main execution
try:
    start_time = time.time()
    log_message("\n" + "="*60)
    log_message("STARTING SCRIPT EXECUTION".center(60))
    log_message("="*60 + "\n")

    # Process each parent folder
    for folder_name, folder_data in xpaths["parent_folders"].items():
        process_folder(folder_name, folder_data)

except Exception as e:
    log_message("\n" + "!"*60)
    log_message(f"CRITICAL ERROR: {str(e)}".center(60))
    log_message("!"*60)
finally:
    driver.quit()
    execution_time = time.time() - start_time
    log_message("\n" + "="*60)
    log_message("SCRIPT COMPLETED".center(60))
    log_message(f"Total execution time: {execution_time:.2f} seconds".center(60))
    log_message("="*60)

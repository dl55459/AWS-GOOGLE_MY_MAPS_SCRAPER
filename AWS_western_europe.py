import os
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
output_folder = "output_airports_csv"  # Folder to store CSV files (change as needed)
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
url = "https://www.google.com/maps/d/viewer?mid=1fmO--HHRTuMMOgyRoXvK7prcGkpeiRE&hl=en&femb=1&ll=43.68706338340388%2C10.128599688444908&z=4"
driver.get(url)

# Wait for the map to load
wait = WebDriverWait(driver, 20)

# Define all XPaths at the beginning for better visibility
xpaths = {
    # Parent folders and their subfolders
    "parent_folders": {
        "Italy": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div',
            'pins': 297+3
        },
        "France": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div',
            'pins': 377+3
        },
        "Spain": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div',
            'pins': 157+3
        },
        "Portugal": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div',
            'pins': 130+3
        },
        "Belgium": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div',
            'pins': 95+3
        },
        "Germany": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div',
            'pins': 71+3
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
        log_message(f"Looking for folder element using XPath: {folder_data['closed']}")
        
        # Open parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        log_message("Found parent folder element. Attempting to expand...")
        
        if not safe_click(closed_folder):
            log_message(f"⚠️ Failed to expand parent folder: {folder_name}")
            return
            
        log_message(f"✔ Successfully expanded parent folder: {folder_name}")
        time.sleep(1)
        
        # Check if there are subfolders
        if "subfolders" in folder_data and folder_data["subfolders"]:
            log_message(f"Found {len(folder_data['subfolders'])} subfolders in {folder_name}")
            
            for subfolder_name, subfolder_data in folder_data["subfolders"].items():
                try:
                    log_message(f"\n├── PROCESSING SUBFOLDER: {subfolder_name}")
                    log_message(f"│   Looking for subfolder element using XPath: {subfolder_data['xpath']}")
                    
                    # Open subfolder
                    subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
                    if not safe_click(subfolder):
                        log_message(f"│   ⚠️ Failed to open subfolder: {subfolder_name}")
                        continue
                        
                    log_message(f"│   ✔ Successfully opened subfolder: {subfolder_name}")
                    time.sleep(1)
                    
                    # Process locations in subfolder
                    log_message(f"│   Preparing to process {subfolder_data['pins']} locations...")
                    for i in range(1, subfolder_data['pins'] + 1):
                        log_message(f"│   └── Processing location {i}/{subfolder_data['pins']}")
                        process_location(subfolder_data['xpath'], subfolder_data['location_base'], i, 
                                       f"{folder_name}/{subfolder_name}")
                
                except Exception as e:
                    log_message(f"│   ⚠️ Error processing subfolder {subfolder_name}: {str(e)}")
        else:
            log_message(f"No subfolders found in {folder_name}, checking for direct locations...")
            if 'location_base' in folder_data:
                log_message(f"Found direct locations in parent folder. Processing {folder_data['pins']} locations...")
                for i in range(1, folder_data['pins'] + 1):
                    log_message(f"└── Processing location {i}/{folder_data['pins']} in parent folder")
                    process_location(folder_data['closed'], folder_data['location_base'], i, folder_name)
            else:
                log_message(f"⚠️ No locations found in parent folder {folder_name}")
                    
    except Exception as e:
        log_message(f"⚠️ Critical error processing folder {folder_name}: {str(e)}")

def process_location(parent_folder_data, child_folder_data=None, index=1, folder_path=""):
    """
    Processes locations in either:
    - Parent folder's direct locations (when child_folder_data=None)
    - Child folder's locations (when child_folder_data provided)
    
    Args:
        parent_folder_data: Dict containing parent folder info with 'closed' and optionally 'location_base'
        child_folder_data: Dict containing child folder info with 'xpath' and 'location_base'
        index: Starting index for location elements
        folder_path: Output path for CSV files
    Returns:
        bool: True if successful, False if failed
    """
    try:
        log_message(f"\n{'='*50}")
        log_message(f"🚀 PROCESSING LOCATION INDEX {index}")
        
        # Get parent folder name
        parent_name = folder_path.split('/')[0] if folder_path else "Unknown"
        log_message(f"Parent: {parent_name}")
        
        if child_folder_data:
            # Get child folder name
            child_name = folder_path.split('/')[1] if '/' in folder_path else "Unknown"
            log_message(f"Child: {child_name}")
            
        log_message(f"{'='*50}")
        
        # ================= FOLDER HANDLING =================
        # Open parent folder
        try:
            parent_element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, parent_folder_data['closed'])))
            safe_click(parent_element)
            log_message("✅ Parent folder opened")
            time.sleep(1.5)
        except Exception as e:
            log_message(f"❌ Failed to open parent folder: {str(e)}")
            return False

        # Open child folder if provided
        if child_folder_data:
            try:
                child_element = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, child_folder_data['xpath'])))
                safe_click(child_element)
                log_message("✅ Child folder opened")
                time.sleep(1.5)
            except Exception as e:
                log_message(f"❌ Failed to open child folder: {str(e)}")
                try:
                    safe_click(parent_element)
                    log_message("↩️ Closed parent folder after child failure")
                except:
                    pass
                return False

        # ================= LOCATION PROCESSING =================
        location_base = child_folder_data['location_base'] if child_folder_data else parent_folder_data.get('location_base')
        
        if not location_base:
            log_message("❌ No location_base found in folder structure")
            return False

        max_attempts = 5  # Try div[1] through div[5]
        location_element = None
        found_index = index
        
        for div_offset in range(0, max_attempts):
            current_div = index + div_offset
            location_xpath = f"{location_base}/div[{current_div}]"
            
            try:
                log_message(f"🔍 Attempting location at div[{current_div}]")
                location_element = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, location_xpath)))
                found_index = current_div
                log_message(f"✅ Found location at div[{found_index}]")
                break
            except Exception as e:
                log_message(f"⚠️ Not found at div[{current_div}]: {str(e)}")
                continue

        if not location_element:
            log_message(f"❌ Failed to find location after {max_attempts} attempts")
            return False

        # ================= CLICK LOCATION =================
        if not safe_click(location_element):
            log_message("❌ Failed to click location element")
            return False
        log_message("🖱️ Location clicked successfully")
        time.sleep(1.5)  # Wait for details panel to load

        # ================= DATA EXTRACTION =================
        name, description = extract_name_and_description()
        log_message(f"📋 Extracted: Name='{name[:50]}...' | Desc={len(description)} chars")

        # ================= COORDINATES EXTRACTION =================
        lat, lon = None, None
        try:
            nav_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, xpaths["navigation_button"])))
            safe_click(nav_button)
            log_message("🌍 Opened navigation tab")
            
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2.5)  # Increased wait for maps to load
            current_url = driver.current_url
            lat, lon = extract_coordinates(current_url)
            log_message(f"📍 Coordinates: {lat}, {lon}")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            log_message(f"⚠️ Coordinate extraction failed: {str(e)}")
            try:
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            except:
                log_message("⚠️ Failed to recover window state")

        # ================= SAVE DATA =================
        try:
            save_location_data(folder_path, name, description, lat, lon, found_index)
            log_message("💾 Data saved successfully")
        except Exception as e:
            log_message(f"❌ Failed to save data: {str(e)}")
            return False

        # ================= CLEANUP =================
        try:
            back_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, xpaths["back_button"])))
            safe_click(back_button)
            log_message("↩️ Returned to list view")
            time.sleep(1)
        except Exception as e:
            log_message(f"⚠️ Failed to return to list: {str(e)}")
            return False

        return True

    except Exception as e:
        log_message(f"💥 CRITICAL ERROR: {str(e)}")
        # Final recovery attempt
        try:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            back_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, xpaths["back_button"])))
            safe_click(back_button)
            log_message("🆘 Recovered from critical error")
        except:
            log_message("🆘 FAILED to recover from critical error")
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
        # Open parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        safe_click(closed_folder)
        log_message(f"Processing folder: {folder_name}")
        time.sleep(1)
        
        # Check if there are subfolders
        if "subfolders" in folder_data and folder_data["subfolders"]:
            for subfolder_name, subfolder_data in folder_data["subfolders"].items():
                try:
                    # Open subfolder
                    subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
                    safe_click(subfolder)
                    log_message(f"Processing subfolder: {subfolder_name}")
                    time.sleep(1)
                    
                    # Process locations in subfolder
                    for i in range(1, subfolder_data['pins'] + 1):
                        process_location(
                            parent_folder_data=folder_data,
                            child_folder_data=subfolder_data,
                            index=i,
                            folder_path=f"{folder_name}/{subfolder_name}"
                        )
                
                except Exception as e:
                    log_message(f"Error processing subfolder {subfolder_name}: {str(e)}")
        else:
            # Process locations directly in parent folder if no subfolders
            if 'location_base' in folder_data:
                for i in range(1, folder_data['pins'] + 1):
                    process_location(
                        parent_folder_data=folder_data,
                        index=i,
                        folder_path=folder_name
                    )
                    
    except Exception as e:
        log_message(f"Error processing folder {folder_name}: {str(e)}")

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

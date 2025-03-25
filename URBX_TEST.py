import os
import time
import csv
import gc
import psutil
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuration
output_folder = "output_urbx_csv"
os.makedirs(output_folder, exist_ok=True)

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Set the path to ChromeDriver
driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Google My Maps link
url = "https://www.google.com/maps/d/viewer?mid=1fuQBYYfSXBobyFtPknOOc9utCArEExk&g_ep=CAISEjI1LjExLjMuNzM1NDg4OTYwMBgAIN1iKnUsOTQyNTk1NTEsOTQyNDI1NTYsOTQyMjQ4MjUsOTQyMjcyNDcsOTQyMjcyNDgsOTQyMzExODgsNDcwNzE3MDQsNDcwNjk1MDgsOTQyMTg2NDEsOTQyMDMwMTksNDcwODQzMDQsOTQyMDg0NTgsOTQyMDg0NDdCAlNL&g_st=ic&ll=37.116651%2C-111.915733&z=8"
driver.get(url)

# Wait for the map to load
wait = WebDriverWait(driver, 20)

# XPaths configuration
xpaths = {
    "parent_folders": {
        "Military Properties": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div',
                    'pins': 79
                },
            }
        },
        "Archaeological Sites": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[2]/div',
                    'pins': 92
                },
            }
        },
        "Abandoned Theme Parks": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/div',
                    'pins': 40
                },
            }
        },
        "abandoned power plants/ abandoned bridges": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div[3]/div[2]/div',
                    'pins': 23
                },
            }
        },
        "Abandoned locations1": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div[3]/div[2]/div',
                    'pins': 2254
                },
            }
        },
        "Abandoned Locations2": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div[3]/div[2]/div',
                    'pins': 2102
                },
            }
        },
        "More Abandoned Buildings": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[7]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[7]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[7]/div/div[3]/div[3]/div[2]/div',
                    'pins': 95
                },
            }
        },
        "Ghost Towns": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[8]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[8]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[8]/div/div[3]/div[3]/div[2]/div',
                    'pins': 195
                },
            }
        },
        "Abandoned Locations3": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[9]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "All": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[9]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[9]/div/div[3]/div[3]/div[2]/div',
                    'pins': 230
                },
            }
        },
    },
    "details_panel": '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div',
    "navigation_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[3]/div',
    "back_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div'
}

# Logging function
def log_message(message):
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [Memory: {memory_usage:.2f} MB] {message}"
    print(log_entry)
    with open("log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

def cleanup_memory():
    gc.collect()
    log_message(f"Memory cleaned. Current usage: {psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.2f} MB")

def safe_click(element, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                log_message(f"Final attempt failed to click element: {str(e)}")
                return False
            time.sleep(1)
            log_message(f"Retrying click ({attempt + 1}/{max_retries})")

def extract_coordinates(url):
    try:
        if "!3d" in url and "!4d" in url:
            parts = url.split("!3d")[1].split("!4d")
            lat = parts[0]
            lon = parts[1].split("!")[0]
        elif "dir//" in url:
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
        else:
            return None, None
            
        return float(lat), float(lon)
    except Exception as e:
        log_message(f"Error extracting coordinates: {str(e)}")
        return None, None

def extract_name_and_description():
    name = "N/A"
    description = "N/A"
    try:
        # Try to find name in the first few divs
        details_divs = driver.find_elements(By.XPATH, xpaths["details_panel"] + "//div")
        
        # Look for name in likely elements
        for div in details_divs[:10]:
            text = div.text.strip()
            if text and len(text) < 100:
                name = text
                break
                
        # Description is often in a larger text block
        description_div = driver.find_element(By.XPATH, xpaths["details_panel"])
        description = description_div.text.replace(name, "").strip()
        
        return name, description
        
    except Exception as e:
        log_message(f"Error extracting name/description: {str(e)}")
        return name, description

def save_location_data(folder_path, name, description, lat, lon, index):
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

def process_location(location_xpath, location_base, index, folder_path=""):
    try:
        log_message(f"\n{'='*50}")
        log_message(f"PROCESSING LOCATION {index} (XPath: {location_base}[{index}])")
        
        # CLICK LOCATION
        location = wait.until(EC.element_to_be_clickable((By.XPATH, f'{location_base}[{index}]')))
        if not safe_click(location):
            log_message("❌ Failed to click location")
            return False
        
        log_message("✅ Location clicked successfully")
        time.sleep(1)
        
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
            except:
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
            time.sleep(0.5)
        except Exception as e:
            log_message(f"❌ Error returning to list: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        log_message(f"❌ CRITICAL ERROR in process_location: {str(e)}")
        try:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
            safe_click(back_button)
        except:
            log_message("Could not recover from error")
        return False

def process_folder(folder_name, folder_data):
    """Process a parent folder with optional subfolders"""
    try:
        log_message(f"\n═════════ PROCESSING PARENT FOLDER: {folder_name.upper()} ═════════")
        
        # Open parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
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
                        process_location(subfolder_data['xpath'], subfolder_data['location_base'], i, 
                                       f"{folder_name}/{subfolder_name}")
                        if i % 10 == 0:
                            cleanup_memory()
                
                except Exception as e:
                    log_message(f"│   ⚠️ Error processing subfolder {subfolder_name}: {str(e)}")
        else:
            log_message(f"No subfolders found in {folder_name}, checking for direct locations...")
            if 'location_base' in folder_data:
                log_message(f"Found direct locations in parent folder. Processing {folder_data['pins']} locations...")
                for i in range(1, folder_data['pins'] + 1):
                    log_message(f"└── Processing location {i}/{folder_data['pins']} in parent folder")
                    process_location(folder_data['closed'], folder_data['location_base'], i, folder_name)
                    if i % 10 == 0:
                        cleanup_memory()
            else:
                log_message(f"⚠️ No locations found in parent folder {folder_name}")
                    
    except Exception as e:
        log_message(f"⚠️ Critical error processing folder {folder_name}: {str(e)}")

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

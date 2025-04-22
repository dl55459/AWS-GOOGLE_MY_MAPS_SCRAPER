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
output_folder = "output_eu_csv"  # Folder to store CSV files (change as needed)
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
            'pins': 297
        },
        "France": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div',
            'pins': 377
        },
        "Spain": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div',
            'pins': 157
        },
        "Portugal": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[4]/div/div[3]/div',
            'pins': 130
        },
        "Belgium": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[5]/div/div[3]/div',
            'pins': 95
        },
        "Germany": {
            'closed': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div[2]/div/div',
            'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[6]/div/div[3]/div',
            'pins': 71
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
possible_name_labels = ["name", "nom"]
possible_description_labels = ["description", "le description"]

# Function to log messages
def log_message(message):
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [Memory: {memory_usage:.2f} MB] {message}"
    print(log_entry)
    try:
        with open("log.txt", "a", encoding="utf-8") as log_file:  # Added encoding
            log_file.write(log_entry + "\n")
    except UnicodeEncodeError:
        # If UTF-8 fails, try to encode problematic characters
        with open("log.txt", "a", encoding="utf-8", errors="replace") as log_file:
            log_file.write(log_entry.encode('utf-8', errors='replace').decode('utf-8') + "\n")


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

def extract_coordinates(url):
    try:
        if "dir//" in url:
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
            return float(lat), float(lon)
        else:
            return None, None
    except Exception as e:
        log_message(f"Error extracting coordinates from URL: {str(e)}")
        return None, None

def extract_name_and_description():
    name = "N/A"
    description = "N/A"
    try:
        # First try to find labeled fields
        details_divs = driver.find_elements(By.XPATH, xpaths["details_panel"] + "//div")
        
        # Check for name labels
        for div in details_divs:
            text = div.text.lower()
            for label in possible_name_labels:
                if label in text:
                    try:
                        name = div.find_element(By.XPATH, "./following-sibling::div[1]").text
                        break
                    except:
                        name = div.text.replace(label, "").strip()
                        break
            if name != "N/A":
                break
        
        # Check for description labels
        for div in details_divs:
            text = div.text.lower()
            for label in possible_description_labels:
                if label in text:
                    try:
                        description = div.find_element(By.XPATH, "./following-sibling::div[1]").text
                        break
                    except:
                        description = div.text.replace(label, "").strip()
                        break
            if description != "N/A":
                break
        
        # Fallback if no labels found
        if name == "N/A" and details_divs:
            name = details_divs[0].text.split('\n')[0] if details_divs[0].text else "N/A"
        if description == "N/A" and details_divs:
            description = '\n'.join(details_divs[0].text.split('\n')[1:]) if details_divs[0].text else "N/A"
            
    except Exception as e:
        log_message(f"Error extracting name or description: {str(e)}")
    return name, description

def process_folder(folder_name, folder_data):
    """Process a parent folder with direct locations (no subfolders)"""
    try:
        log_message(f"═════════ PROCESSING FOLDER: {folder_name.upper()} ═════════")
        log_message(f"Looking for folder element using XPath: {folder_data['closed']}")
        
        # Open parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        log_message("Found folder element. Attempting to expand...")
        
        if not safe_click(closed_folder):
            log_message(f"⚠️ Failed to expand folder: {folder_name}")
            return
            
        log_message(f"✔ Successfully expanded folder: {folder_name}")
        time.sleep(1)
        
        # Process locations directly in the folder
        log_message(f"Preparing to process {folder_data['pins']} locations...")
        
        # Note: First location starts with div[3], then increments by 1
        for i in range(3, folder_data['pins'] + 3):
            log_message(f"└── Processing location {i-2}/{folder_data['pins']}")
            process_location(folder_data['closed'], folder_data['location_base'], i, folder_name)
            
    except Exception as e:
        log_message(f"⚠️ Critical error processing folder {folder_name}: {str(e)}")

def process_location(location_xpath, location_base, index, folder_path=""):
    try:
        log_message(f"\n{'='*50}")
        log_message(f"PROCESSING LOCATION {index-2} (XPath: {location_base}[{index}])")
        
        # CLICK LOCATION - note the adjusted XPath for direct locations
        location = wait.until(EC.element_to_be_clickable((By.XPATH, f'{location_base}[{index}]')))
        log_message("Location element found, attempting click...")
        
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
        save_location_data(folder_path, name, description, lat, lon, index-2)  # Adjust index for 1-based counting
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

def save_location_data(folder_path, name, description, lat, lon, index):
    """Save location data to CSV with proper UTF-8 handling"""
    clean_path = folder_path.replace(" ", "_").lower()
    filename = f"{clean_path}.csv"
    filepath = os.path.join(output_folder, filename)
    
    # Clean the data by encoding/decoding to handle special characters
    def clean_text(text):
        if text is None:
            return ""
        if isinstance(text, str):
            return text.encode('utf-8', errors='replace').decode('utf-8')
        return str(text)
    
    data = {
        "Name": clean_text(name),
        "Description": clean_text(description),
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

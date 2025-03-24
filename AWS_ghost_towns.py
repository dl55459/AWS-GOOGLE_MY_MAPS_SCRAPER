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

# Function to safely click an element
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

# Function to extract coordinates
def extract_coordinates(url):
    try:
        if "dir//" in url:
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
            return float(lat), float(lon)
        return None, None
    except Exception as e:
        log_message(f"Error extracting coordinates: {str(e)}")
        return None, None

# Function to extract name and description
def extract_name_and_description():
    name = "N/A"
    description = "N/A"
    try:
        details_divs = driver.find_elements(By.XPATH, xpaths["details_panel"] + "//div")
        for div in details_divs:
            text = div.text.lower()
            for label in possible_name_labels:
                if label in text:
                    name = div.find_element(By.XPATH, "./following-sibling::div[1]").text
                    break
            for label in possible_description_labels:
                if label in text:
                    description = div.find_element(By.XPATH, "./following-sibling::div[1]").text
                    break
    except Exception as e:
        log_message(f"Error extracting name/description: {str(e)}")
    return name, description

def process_folder(folder_element, current_path=""):
    """Recursively process a folder and its contents"""
    try:
        # Click to expand the folder
        folder_header = folder_element.find_element(By.XPATH, ".//div[contains(@class, 'section-folder-header')]")
        safe_click(folder_header)
        time.sleep(1)
        
        folder_name = folder_header.text
        full_path = f"{current_path}/{folder_name}" if current_path else folder_name
        log_message(f"Processing folder: {full_path}")
        
        # Get all items in current folder
        items = folder_element.find_elements(By.XPATH, "./following-sibling::div[contains(@class, 'section-content')]//div[contains(@class, 'section-item')]")
        
        for item in items:
            try:
                item_class = item.get_attribute("class")
                if "section-folder" in item_class:
                    process_folder(item, full_path)
                elif "section-location" in item_class:
                    process_location(item, full_path)
            except Exception as e:
                log_message(f"Error processing item: {str(e)}")
                
    except Exception as e:
        log_message(f"Error processing folder: {str(e)}")

def process_location(location_element, folder_path):
    """Process a single location"""
    try:
        safe_click(location_element)
        time.sleep(1)
        
        name, description = extract_name_and_description()
        
        # Get coordinates
        nav_button = driver.find_element(By.XPATH, xpaths["navigation_button"])
        safe_click(nav_button)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        current_url = driver.current_url
        lat, lon = extract_coordinates(current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        # Save data
        save_location_data(folder_path, name, description, lat, lon)
        
        # Go back
        back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
        safe_click(back_button)
        time.sleep(1)
        
    except Exception as e:
        log_message(f"Error processing location: {str(e)}")

def save_location_data(folder_path, name, description, lat, lon):
    """Save location data to CSV"""
    # Clean path for filename
    clean_path = folder_path.replace(" ", "_").replace("/", "_").lower()
    filename = f"{clean_path}.csv" if clean_path else "locations.csv"
    filepath = os.path.join(output_folder, filename)
    
    data = {
        "Name": name,
        "Description": description,
        "Latitude": lat,
        "Longitude": lon,
        "Folder Path": folder_path
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
    log_message("Script execution started.")
    
    # Find all root elements
    root_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'section-item')]")
    
    for item in root_items:
        try:
            item_class = item.get_attribute("class")
            if "section-folder" in item_class:
                process_folder(item)
            elif "section-location" in item_class:
                process_location(item, "")
        except Exception as e:
            log_message(f"Error processing root item: {str(e)}")
            
except Exception as e:
    log_message(f"Error in main execution: {str(e)}")
finally:
    driver.quit()
    execution_time = time.time() - start_time
    log_message(f"Script completed in {execution_time:.2f} seconds.")

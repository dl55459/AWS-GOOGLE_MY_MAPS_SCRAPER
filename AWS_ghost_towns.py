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

# Function to log messages to both console and log.txt
def log_message(message):
    # Get current memory usage
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # In MB
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format the log message
    log_entry = f"[{timestamp}] [Memory: {memory_usage:.2f} MB] {message}"
    print(log_entry)  # Print to console
    with open("log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")  # Write to log file

# Function to safely click an element with retries
def safe_click(element, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)  # Wait for the element to be in view
            element.click()
            return True
        except Exception as e:
            log_message(f"Attempt {attempt + 1}: Error clicking element - {str(e)}")
            time.sleep(2)  # Wait before retrying
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

# Function to generate a valid filename
def generate_filename(parent_folder, child_folder):
    # Replace spaces and special characters with underscores
    parent_folder = parent_folder.replace(" ", "_").replace("/", "_").lower()
    child_folder = child_folder.replace(" ", "_").replace("/", "_").lower()
    return os.path.join(output_folder, f"{parent_folder}_{child_folder}.csv")

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

# Extract data from all parent folders and their subfolders
try:
    start_time = time.time()  # Start timer for execution time
    log_message("Script execution started.")

    # Loop through each parent folder
    for folder_name, folder_data in xpaths["parent_folders"].items():
        log_message(f"Processing parent folder: {folder_name}")

        # Locate and expand the parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        safe_click(closed_folder)
        log_message(f"Expanded parent folder: {folder_name}")
        time.sleep(1)  # Wait for the folder to expand

        # Loop through each subfolder in the parent folder
        for subfolder_name, subfolder_data in folder_data["subfolders"].items():
            try:
                log_message(f"Processing subfolder: {subfolder_name}")

                # Locate and click the subfolder
                subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
                safe_click(subfolder)
                log_message(f"Clicked subfolder: {subfolder_name}")
                time.sleep(1)  # Wait for the subfolder to load

                # Initialize a list to store pins for this subfolder
                pins = []

                # Loop through all location elements in the subfolder
                for index in range(1, subfolder_data['pins'] + 1):  # Loop from 1 to number of pins
                    try:
                        # Generate the XPath for the current location element
                        location_xpath = f'{subfolder_data["location_base"]}[{index}]'
                        log_message(f"Processing location {index} with XPath: {location_xpath}")

                        # Locate the location element
                        location = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
                        if not safe_click(location):
                            log_message(f"Skipping location {index} due to click failure")
                            continue
                        log_message(f"Clicked location {index}")
                        time.sleep(1)  # Wait for the details panel to load

                        # Extract name and description dynamically
                        name, description = extract_name_and_description()

                        # Click the navigation button to get coordinates
                        nav_button = driver.find_element(By.XPATH, xpaths["navigation_button"])
                        safe_click(nav_button)
                        log_message("Clicked navigation button")

                        # Switch to the new tab
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(2)  # Wait for the tab to load

                        # Extract coordinates from the URL
                        current_url = driver.current_url
                        lat, lon = extract_coordinates(current_url)
                        log_message(f"Extracted coordinates: {lat}, {lon}")

                        # Save the data
                        pins.append({
                            "Name": name,
                            "Description": description,
                            "Latitude": lat,
                            "Longitude": lon,
                            "Index": index
                        })

                        # Close the new tab and switch back to the main tab
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)

                        # Click the back button to return to the main side panel
                        back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
                        safe_click(back_button)
                        log_message("Clicked back button")
                        time.sleep(1)  # Wait for the side panel to reload
                    except Exception as e:
                        log_message(f"Error extracting location data in {subfolder_name} (index {index}): {str(e)}")

                # Save the data for this subfolder to a CSV file
                filename = generate_filename(folder_name, subfolder_name)
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Name", "Description", "Latitude", "Longitude", "Index"])
                    writer.writeheader()
                    writer.writerows(pins)

                log_message(f"Data saved to {filename}")
            except Exception as e:
                log_message(f"Error accessing subfolder {subfolder_name}: {str(e)}")
except Exception as e:
    log_message(f"Error accessing parent folder or subfolder: {str(e)}")
finally:
    # Close the browser
    driver.quit()
    log_message("Browser closed.")

    # Log total execution time
    execution_time = time.time() - start_time
    log_message(f"Script execution completed in {execution_time:.2f} seconds.")

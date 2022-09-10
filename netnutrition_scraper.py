from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import string

import pandas as pd

# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")

path = 'C:\\Users\\isaac\\Desktop\\netnutrition_scraper\\chromedriver.exe'
url = 'https://nutrition.info.dining.ucsb.edu/NetNutrition/1'

driver = webdriver.Chrome(executable_path=path)
wait = WebDriverWait(driver, 30)
driver.get(url)

# Navigate to Ortega's daily menu
ortega_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Take Out at Ortega Commons')))
ortega_button.click()

ortega_daily_menu_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Ortega\'s Daily Menu')))
ortega_daily_menu_button.click()

ortega_daily_menu_table = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'table')))

# Click on first Ortega menu item
# driver.execute_script("document.getElementsByClassName('cbo_nn_itemPrimaryRow')[0].getElementsByClassName('cbo_nn_itemHover')[0].click()")

# Scrape Ortega menu items and serving sizes
ortega_items = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemPrimaryRow')
ortega_items_alt = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemAlternateRow')

ortega_items_list = []

for ortega_item in ortega_items:
    item_button = ortega_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = ortega_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    ortega_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    ortega_items_list.append(ortega_food)
    
for ortega_item in ortega_items_alt:
    item_button = ortega_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = ortega_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    ortega_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    ortega_items_list.append(ortega_food)

df1 = pd.DataFrame(ortega_items_list)
df1.to_csv('ortega.csv', index=False)

# Navigate back to page showing all dining units
back_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_Back*Menu Details')))
back_button.click()

back_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_Back*Child Units')))
back_button.click()

# Navigate to DLG's breakfast menu
dlg_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'De La Guerra Dining Commons')))
dlg_button.click()

dlg_daily_menu_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'De La Guerra\'s Daily Menu')))
dlg_daily_menu_button.click()

dlg_breakfast_button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cbo_nn_menuLink')))
dlg_breakfast_button[0].click()

dlg_breakfast_table = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'table')))

# Scrape DLG breakfast menu items and serving sizes
dlg_items = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemPrimaryRow')
dlg_items_alt = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemAlternateRow')

dlg_items_list = []

for dlg_item in dlg_items:
    item_button = dlg_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = dlg_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    dlg_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    dlg_items_list.append(dlg_food)
    
for dlg_item in dlg_items_alt:
    item_button = dlg_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = dlg_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    dlg_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    dlg_items_list.append(dlg_food)

df2 = pd.DataFrame(dlg_items_list)
df2.to_csv('dlg_breakfast.csv', index=False)

# Navigate back to page showing DLG daily menus
back_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_Back*Menu Details')))
back_button.click()

# Navigate to DLG's lunch menu
dlg_lunch_button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cbo_nn_menuLink')))
dlg_lunch_button[1].click()

dlg_lunch_table = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'table')))

# Scrape DLG lunch menu items and serving sizes
dlg_items = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemPrimaryRow')
dlg_items_alt = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemAlternateRow')

dlg_items_list = []

for dlg_item in dlg_items:
    item_button = dlg_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = dlg_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    dlg_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    dlg_items_list.append(dlg_food)
    
for dlg_item in dlg_items_alt:
    item_button = dlg_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = dlg_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    dlg_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    dlg_items_list.append(dlg_food)

df3 = pd.DataFrame(dlg_items_list)
df3.to_csv('dlg_lunch.csv', index=False)

# Navigate back to page showing DLG daily menus
back_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_Back*Menu Details')))
back_button.click()

# Navigate to DLG's dinner menu
dlg_dinner_button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cbo_nn_menuLink')))
dlg_dinner_button[2].click()

dlg_dinner_table = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'table')))

# Scrape DLG dinner menu items and serving sizes
dlg_items = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemPrimaryRow')
dlg_items_alt = driver.find_elements(By.CLASS_NAME, 'cbo_nn_itemAlternateRow')

dlg_items_list = []

for dlg_item in dlg_items:
    item_button = dlg_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = dlg_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    dlg_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    dlg_items_list.append(dlg_food)
    
for dlg_item in dlg_items_alt:
    item_button = dlg_item.find_element(By.XPATH, './/*[@class="cbo_nn_itemHover"]')    
    item_name = item_button.text
    serving_size = dlg_item.find_element(By.XPATH, './/*[@class="align-middle"][3]').text
    
    # Scrape data on macronutrients
    item_button.click()
    nutrition_table = wait.until(EC.visibility_of_element_located((By.ID, 'nutritionLabel')))
    nutrition_row_calories = nutrition_table.find_element(By.CLASS_NAME, "cbo_nn_LabelSubHeader")
    nutrition_row_fat = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[0]
    nutrition_row_carbs = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[5]
    nutrition_row_protein = nutrition_table.find_elements(By.CLASS_NAME, "cbo_nn_LabelBorderedSubHeader")[9]
    
    calories_amount = nutrition_row_calories.find_element(By.CLASS_NAME, 'inline-div-right').text
    fat_amount = nutrition_row_fat.find_element(By.XPATH, './/div[1]/span[2]').text
    carbs_amount = nutrition_row_carbs.find_element(By.XPATH, './/div[1]/span[2]').text
    protein_amount = nutrition_row_protein.find_element(By.XPATH, './/div[1]/span[2]').text
    
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close")))
    close_button.click()
    
    dlg_food = {
        'name': item_name,
        'serving size': serving_size,
        'calories': float(calories_amount.strip(' <g')), 
        'fat': float(fat_amount.strip(' <g')),
        'carbohydrates': float(carbs_amount.strip(' <g')),
        'protein': float(protein_amount.strip(' <g'))
    }
    dlg_items_list.append(dlg_food)

df4 = pd.DataFrame(dlg_items_list)
df4.to_csv('dlg_dinner.csv', index=False)
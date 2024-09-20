# pylint: disable=missing-function-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=broad-exception-caught
# pylint: disable=inconsistent-return-statements
import os
import datetime
import re
import time
import string
import random
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from yaml import safe_load


def delete_files(folder_path):
    """this method delete the files"""
    # folder = '/path/to/folder'
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def rename_file(path, filename):
    """this method rename the files"""
    try:
        new_file_name = os.path.join(path, filename + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.png')
        os.rename(os.path.join(path, filename + '.png'), new_file_name)
    except WindowsError:
        print('image not found to rename:' + new_file_name)


def get_data(variable):
    """this method return the value"""
    variable = variable.replace('_empty_', '')
    if variable.find("randomemail_") != -1:
        variable_name = variable.replace('_space_', ' ')
        random_email = variable_name.split('_')
        random_number = random.randint(0, 99999)
        email_list = random_email[1].split('@')
        if len(email_list) > 1:
            email_id = email_list[0] + str(random_number) + '@' + email_list[1]
        else:
            email_id = email_list[0] + str(random_number) + '@gmail.com'
        return email_id
    elif variable.find("randomnumber_") != -1:
        random_number = random.randint(0, 9999999999)
        return random_number
    elif variable.find("randomtext_") != -1:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(7))
    else:
        return variable


def getymlvalue(data, key):
    """this method fetch the data of the key"""
    try:
        data = safe_load(data)
        value = data.get(key)
        if value is None:
            return key
        return value
    except Exception as e:
        print(e)
        return key


# method for fetching only key from xpath
def get_yml_object_repository_value(data, node, key, context):
    """this method fetch the data of the key"""
    try:
        data = safe_load(data)
        if node == "":
            value = data[key]
        else:
            value = data[node][key]
        if value is None:
            value = key
    except Exception as e:
        print(e)
        value = key
    context.xpath = value
    context.XPathKey = node + "." + key
    return value


# method for fetching only key from xpath
def get_object_repository_value(data, key):
    """this method fetch the element and return the fetching element"""
    try:
        data = safe_load(data)
        value = data[key]
        if value is None:
            return key
        return value
    except Exception as e:
        print(e)
        return key


def getframes(context, xpath):
    try:
        context.driver.switch_to.default_content()
    except:
        pass
    try:
        if "||" in xpath:
            split_xpath = xpath.split("||")
            frame_element = context.driver.find_element(MobileBy.XPATH, split_xpath[1])
            context.driver.switch_to.frame(frame_element)
            return split_xpath[0]
        else:
            return xpath
    except Exception as e:
        raise Exception(f"Failed to switch frames: {e}")


def findElement(context, identificationtype, xpath):
    """this method fetch the element and return the fetching element"""
    element = None
    if identificationtype.upper() == "xpath".upper():
        element = context.driver.find_element("xpath", xpath)
    elif identificationtype.upper() == "id".upper():
        element = context.driver.find_element_by_id(xpath)
    return element


def findElements(context, identificationtype, xpath):
    """this method fetch the elements and return the fetching elements"""
    element = None
    if identificationtype.upper() == "xpath".upper():
        element = context.driver.find_elements("xpath", xpath)
    elif identificationtype.upper() == "id".upper():
        element = context.driver.find_elements_by_id(xpath)
    return element


def button_selected(context, identificationtype, xpath):
    """this action click on the element label type is button"""
    main_xpath = getframes(context, xpath)
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            try:
                element.click()
                break
            except:
                context.driver.execute_script("arguments[0].click()", element)
                break
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception("Unable to click on element")


def selected_dropdown_on_link(context, texttobeentered, identificationtype):
    """this action click the element in the dropdown label"""
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            try:
                xpath = "//*[contains(@text,'" + str(texttobeentered) + "')]"
                element = findElement(context, identificationtype, xpath)
                element.clear()
                break
            except:
                context.driver.execute_script("arguments[0].click()", xpath)
                break
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception("Unable to select dropdown option")


def selected_file_upload(context, identificationtype, xpath):
    """this action file upload in the required position"""
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath)
            element.clear()
            break
        except Exception:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception


def label_verify_text(context, identificationtype, xpath):
    """this action verify the text on the element"""
    main_xpath = getframes(context, xpath)
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            if element.is_displayed():
                try:
                    eleText = element.text
                    context.eachStepMessage.append("Visible text : ", eleText)
                except:
                    pass
                return True
            return False
        except:
            context.driver.swipe(x, (window_height * 0.70), x, (window_height * 0.50), 400)
            i += 1
        if i >= int(context.WhileLoopCount):
            return False


def verify_date_format(context, identificationtype, xpath, param):
    """this action verify the text on the element"""
    param = str(getymlvalue(context.yamldata, get_data(param)))
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath)
            if element.is_displayed():
                eleText = element.text
                current_date = datetime.now()
                # Monday, Mar 28 ---> param should be like this : %A, %b %d 
                formatted_date = current_date.strftime(param)
                context.eachStepMessage.append(
                    "Actual Date : " + str(eleText) + ", Expected Date : " + str(formatted_date))
                if str(eleText) == str(formatted_date):
                    return True
                else:
                    return False
        except:
            context.driver.swipe(x, (window_height * 0.70), x, (window_height * 0.50), 400)
            i += 1
        if i >= int(context.WhileLoopCount):
            return False


def testbox_verify_content(context, texttobeenter, identificationtype, xpath):
    """this method verify the content of the text box"""
    main_xpath = getframes(context, xpath)
    texttobeenter = str(getymlvalue(context.yamldata, get_data(texttobeenter)))
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath).text
            if element.find(texttobeenter) != -1:
                return True
            return False
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def butn_lnk_click_if_visible(context, identificationtype, xpath):
    """this method check the button is visible or not"""
    main_xpath = getframes(context, xpath)
    if str(identificationtype).lower() == 'xpath':
        element_locator = (By.XPATH, main_xpath)
    else:
        element_locator = (By.ID, main_xpath)
    flag = True
    while flag:
        try:
            element = WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located(element_locator))
            element.click()
            break
        except:
            flag = False


def label_verify_content(context, valuetobeentered, identificationtype):
    """this method verify the content of the label"""
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            if "NA" in valuetobeentered:
                return True
            xpath = "//*[contains(@text, '" + valuetobeentered + "')]"
            element = findElement(context, identificationtype, xpath)
            if element.is_displayed():
                return True
        except Exception as e:
            print('Element not found with text', e)
        time.sleep(context.WaitTimeIntervalInSeconds)
        i += 1
    return False


def textbox_verify_text_not_present(context, valuetobeentered, identificationtype, xpath):
    """this method verify the text not present in the element """
    main_xpath = getframes(context, xpath)
    valuetobeentered = str(getymlvalue(context.yamldata, get_data(valuetobeentered)))
    try:
        element = findElement(context, identificationtype, main_xpath).text
        if element.find(valuetobeentered) != -1:
            return False
        return True
    except Exception:
        return True


def butn_scroll_and_click(context, identificationtype, xpath):
    """this method will scroll and click the element"""
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath)
            element.click()
            break
        except:
            context.driver.swipe(x, (window_height * 0.8), x, (window_height * 0.20), 400)
        if i >= int(context.WhileLoopCount):
            raise Exception("Error: element not found")


def clear_and_enter_text(context, texttobeentered, identificationtype, xpath):
    """this method first clear the text and enter the text in the textbox"""
    main_xpath = getframes(context, xpath)
    texttobeentered = str(getymlvalue(context.yamldata, get_data(texttobeentered)))
    try:
        element = findElement(context, identificationtype, main_xpath)
        element.clear()
        time.sleep(1)
        element.send_keys(texttobeentered)
    except Exception as e:
        raise Exception("Unable to Enter Text in TextBox", e)


def btn_click_by_index(context, texttobeentered, identificationtype, objxpath):
    """this method click the element according to the index"""
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElements(context, identificationtype, objxpath)
            element = element[int(texttobeentered) - 1]
            try:
                print("Clicked on link no " + texttobeentered + " (" + element.text + ")")
                element.click()
                break
            except:
                context.driver.execute_script("arguments[0].click()", element)
                break
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception("Unable to click on element")


def lnk_verify_records_displayed(context, identificationtype, xpath):
    """this method verify the link records displayed or not"""
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        context.driver.swipe(x, (window_height * 0.70), x, (window_height * 0.50), 400)
        try:
            elements = findElements(context, identificationtype, xpath)
            if len(elements) > 0:
                return True
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def label_verify_text_not_present(context, valuetobeentered, identificationtype):
    """this method verify the text not present in the element """
    valuetobeentered = str(getymlvalue(context.yamldata, get_data(valuetobeentered)))
    try:
        xpath = "//*[contains(text(),'" + valuetobeentered + "')]"
        element = findElement(context, identificationtype, xpath)
        if element.is_displayed():
            return False
        return True
    except:
        return True


def label_dropdown_copied_number(context, identificationtype, xpath):
    """this method copied the text of the dropdown element"""
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath)
            context.LabelNumber = element.text
            if context.LabelNumber.find("₹") != -1:
                context.LabelNumber = context.LabelNumber.replace("₹", "")
            break
        except:
            context.driver.swipe(x, (window_height * 0.70), x, (window_height * 0.20), 400)


def label_verify_copied_number(context, identificationtype, xpath):
    """this method copied the text of the element"""
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath)
            if element is None :
                element = context.driver.find_element(By.XPATH,xpath)
            variable = element.text
            if variable.find(".") != -1:
                split_prices = variable.split('.')
                price = split_prices[0]
                price = re.sub('[^0-9]', '', price)
            else:
                price = variable
                price = re.sub('[^0-9]', '', price)
            if context.LabelNumber.find(".") != -1:
                split_copied = context.LabelNumber.split('.')
                copied_value = split_copied[0]
                copied_value = re.sub('[^0-9]', '', copied_value)
            else:
                copied_value = context.LabelNumber
                copied_value = re.sub('[^0-9]', '', copied_value)
            if copied_value == price:
                return True
        except Exception:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def label_copied_text(context, identificationtype, xpath):
    """this method copied the text of the element"""
    main_xpath = getframes(context, xpath)
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            context.LabelText = element.text
            break
        except Exception as e:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
            i += 1
            if i >= int(context.WhileLoopCount):
                raise Exception(e)


def label_dropdown_verify_copied_text(context, identificationtype, xpath):
    """this method copied the text of the dropdown element"""
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath).text
            if element.find(context.LabelText) != -1:
                return True
        except Exception:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def set_textbox_area_entered(context, valuetobeenter, identificationtype, xpath):
    """this method entered the text in the text box"""
    main_xpath = getframes(context, xpath)
    valuetobeenter = str(getymlvalue(context.yamldata, get_data(valuetobeenter)))
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            element.send_keys(valuetobeenter)
            break
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception("Unable to enter in Text Box")


def label_displayed(context, valuetobeenter, identificationtype):
    """this method check element is displayed or not"""
    i = 0
    valuetobeenter = str(getymlvalue(context.yamldata, get_data(valuetobeenter)))
    while i < int(context.WhileLoopCount):
        try:
            if "NA" in valuetobeenter:
                return True
            xpath = "//*[contains(text(), '" + valuetobeenter + "')]"
            listofelements = findElements(context, identificationtype, xpath)
            for element in listofelements:
                if element.is_displayed():
                    return True
        except Exception as e:
            print('Element not found with text' + str(e))
        time.sleep(context.WaitTimeIntervalInSeconds)
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def page_displayed(context, valuetobeenter, identificationtype):
    """this method check element is displayed or not"""
    valuetobeenter = str(getymlvalue(context.yamldata, get_data(valuetobeenter)))
    if 'app' in str(context.mobileAutomationType).lower():
        return True
    else:
        i = 0
        while i < int(context.WhileLoopCount):
            try:
                if "NA" in valuetobeenter:
                    return True
                xpath = "//*[contains(text(),'" + valuetobeenter + "')]"
                listofelements = findElements(context, identificationtype, xpath)
                for element in listofelements:
                    if element.is_displayed():
                        return True
            except Exception as e:
                print('Element not found with text' + str(e))
            time.sleep(context.WaitTimeIntervalInSeconds)
            i += 1
            if i >= int(context.WhileLoopCount):
                return False


def scroll_and_entertext(context, valuetobeenter, identificationtype, xpath):
    """this method scroll to the element enter txt in textfield"""
    main_xpath = getframes(context, xpath)
    valuetobeenter = str(getymlvalue(context.yamldata, get_data(valuetobeenter)))
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            if element.is_displayed():
                element.send_keys(valuetobeenter)
                break
        except:
            context.driver.swipe(x, (window_height * 0.75), x, (window_height * 0.20), 400)
        i += 1
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        if i >= int(context.WhileLoopCount):
            raise Exception(f"Unable to enter {valuetobeenter} in Text Box")


def scroll_and_clear_entertext(context, valuetobeenter, identificationtype, xpath):
    """this method scroll to the element clear the text after enter txt in textfield"""
    main_xpath = getframes(context, xpath)
    valuetobeenter = str(getymlvalue(context.yamldata, get_data(valuetobeenter)))
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    x = window_width / 2
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            if element.is_displayed():
                element.click()
                element.clear()
                time.sleep(1)
                element.send_keys(valuetobeenter)
                break
        except:
            context.driver.swipe(x, (window_height * 0.70), x, (window_height * 0.20), 400)
        i += 1
    time.sleep(int(context.TimeIntervalInMilliSeconds))
    if i >= int(context.WhileLoopCount):
        raise Exception(f"Unable to enter {valuetobeenter} in Text Box")


def scroll_down(context, scroll):
    """this method scroll to the down based on parameter"""
    scroll = int(str(getymlvalue(context.yamldata, get_data(scroll))))
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    i = 0
    x = window_width / 2
    while i < scroll:
        context.driver.swipe(x, (window_height * 0.80), x, (window_height * 0.20), 400)
        i += 1


def scroll_vertical(context, vertical):
    """this method scroll vertical  based on parameter"""
    scroll = str(getymlvalue(context.yamldata, get_data(vertical)))
    window_size = context.driver.get_window_size()
    window_width = window_size.pop('width')
    window_height = window_size.pop('height')
    i = 0
    x = window_width / 2
    if '-' in scroll:
        scroll = int(scroll.replace('-', ''))
        start_y = window_height * 0.2
        end_y = window_height * 0.75
        while i < scroll:
            context.driver.swipe(x, start_y, x, end_y, 400)
            i += 1
    else:
        scroll = int(scroll.replace('-', ''))
        start_y = window_height * 0.8
        end_y = window_height * 0.2
        while i < scroll:
            context.driver.swipe(x, start_y, x, end_y, 400)
            i += 1


def click_until_not_visible(context, identificationtype, xpath):
    """this method click until the element is visible"""
    main_xpath = getframes(context, xpath)
    if str(identificationtype).lower() == 'xpath':
        element_locator = (By.XPATH, main_xpath)
    else:
        element_locator = (By.ID, main_xpath)
    flag = True
    while flag:
        try:
            element = WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located(element_locator))
            element.click()
            break
        except:
            flag = False


def verify_enabled(context, identificationtype, xpath):
    main_xpath = getframes(context, xpath)
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            if element.is_enabled():
                return True
            return False
        except Exception:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def verify_disabled(context, identificationtype, xpath):
    main_xpath = getframes(context, xpath)
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            if element.is_enabled():
                return False
            return True
        except Exception:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            return False


def click_multiple_times(context, valuetobeenter, identificationtype, xpath):
    main_xpath = getframes(context, xpath)
    value = str(getymlvalue(context.yamldata, get_data(valuetobeenter)))
    i = 0
    j = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, main_xpath)
            while j < int(value):
                element.click()
                j += 1
            break
        except:
            time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception("Unable to locate the element")


def tap_element(context, identificationtype, xpath):
    try:
        context.driver.press_keycode(66)
    except:
        pass
    i = 0
    while i < int(context.WhileLoopCount):
        try:
            element = findElement(context, identificationtype, xpath)
            try:
                touch_actions = TouchAction(context.driver)
                touch_actions.tap(element).perform()
                break
            except:
                context.driver.execute_script("arguments[0].click()", element)
                break
        except Exception as e:
            print(e)
        time.sleep(int(context.TimeIntervalInMilliSeconds))
        i += 1
        if i >= int(context.WhileLoopCount):
            raise Exception("Unable to click on element")

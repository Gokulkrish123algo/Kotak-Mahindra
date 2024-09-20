# pylint:disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-wildcard-import
# pylint: disable=unused-import
import time
import re
import random
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import common
import imagecompareutil
import requestutil
from appium.webdriver.common.touch_action import TouchAction


def attach_page(context,pagename):
    if "browser" in str(context.mobileAutomationType).lower():
        try:
            pagename = int(pagename.replace('Page', ''))-1
            all_window_handles= context.driver.window_handles
            if pagename is not None:
                context.driver.switch_to.window(all_window_handles[pagename])
                return
            for handle in all_window_handles:
                context.driver.switch_to_window(handle)
                page_title = context.driver.title
                if pagename in page_title:
                    break
        except:
            pass

        
def textboxnameentered(context,var_name):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","NameTextBoxXPATH",context))
    common.set_textbox_area_entered(context, var_name, "XPATH", xpath)
          
def textboxmobilenoentered(context,var_mobileNo):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","MobileNoTextBoxXPATH",context))
    common.set_textbox_area_entered(context, var_mobileNo, "XPATH", xpath)
          
def textboxpincodeentered(context,var_pinCode):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","PINCODETextBoxXPATH",context))
    common.set_textbox_area_entered(context, var_pinCode, "XPATH", xpath)
          
def textboxaddressentered(context,var_address):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","AddressTextBoxXPATH",context))
    common.set_textbox_area_entered(context, var_address, "XPATH", xpath)
          
def buttonworkscrollandclick(context):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","WorkButtonXPATH",context))
    common.butn_scroll_and_click(context,"XPATH",xpath)
    
def buttonaddnewaddressselected(context):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","AddnewaddressButtonXPATH",context))
    common.button_selected(context,"XPATH",xpath)
    
def buttondeleteselected(context):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","DeleteButtonXPATH",context))
    common.button_selected(context,"XPATH",xpath)
    
def buttonyesselected(context):
    try:
        attach_page(context,'My address')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yamldataobject,"My address","yesButtonXPATH",context))
    common.button_selected(context,"XPATH",xpath)
    
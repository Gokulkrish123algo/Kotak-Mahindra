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

        
def pageloginpageaccesstopage(context):
    pass
    
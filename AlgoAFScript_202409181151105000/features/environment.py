# pylint: disable=missing-function-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long
import os
import shutil
import subprocess
import platform
import time
from typing import Dict, Any
from _datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.common import AppiumOptions
import xmltodict
from yaml import safe_load


def before_all(context):
    def getymldata(path):
        data = safe_load(path)
        return data

    starttime = datetime.now()
    plat = platform.system()
    release = platform.release()
    os_version = plat + " " + release
    user = os.getlogin()
    print("before all method")
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'TestData.yml'))
        context.yamldata = str(getymldata(open(path)))
    except Exception:
        context.yamldata = None
    objectpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ObjectRepository.yml'))
    context.yamldataobject = str(getymldata(open(objectpath, encoding="utf8")))
    xmlpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ApplicationSettings.xml'))
    xml_data = ''
    with open(xmlpath) as fd:
        xml_data = xmltodict.parse(fd.read())
    context.softAssertion = xml_data['ApplicationSettings']['SoftAssertion']
    context.platformName = xml_data['ApplicationSettings']['platformName']
    context.platformVersion = xml_data['ApplicationSettings']['platformVersion']
    context.deviceName = xml_data['ApplicationSettings']['deviceName']
    context.udid = xml_data['ApplicationSettings']['udid']
    context.autName = xml_data['ApplicationSettings']['URL']
    context.autType = xml_data['ApplicationSettings']['autType']
    context.RemoteUrl = xml_data['ApplicationSettings']['RemoteUrl']
    context.browserName = xml_data['ApplicationSettings']['browserName']
    context.appPackage = xml_data['ApplicationSettings']['appPackage']
    context.appActivity = xml_data['ApplicationSettings']['appActivity']
    context.mobileAutomationType = xml_data['ApplicationSettings']['mobileAutomationType']
    context.automationName = xml_data['ApplicationSettings']['automationName']
    context.driver = ''
    # context.driver=webdriver.Remote(command_executor='http://127.0.0.1:4723/wd/hub',desired_capabilities={'platformName':context.platformName,'platformVersion':context.platformVersion,'deviceName':context.deviceName,'udid':context.udid,'fullReset':False,'noReset':True,'nativeWebScreenshot' : 'true','appPackage':context.appPackage, 'appActivity':context.appActivity,'newCommandTimeout':'5000'})
    context.compareImage = xml_data['ApplicationSettings']['EnableCompareImage']
    time.sleep(3)
    context.TimeIntervalInMilliSeconds = 1
    context.WaitTimeIntervalInSeconds = 1
    context.WhileLoopCount = 5
    context.MaximumTimeInSecondsToWaitForControl = xml_data['ApplicationSettings'][
        'MaximumTimeInSecondsToWaitForControl']
    context.MaximumTimeInSecondsToWaitForScroll = xml_data['ApplicationSettings'][
        'MaximumTimeInMilliSecondsToWaitForPage']
    context.FailureScreenshot = xml_data['ApplicationSettings']['EnableScrenshotForFailure']
    context.PassedScreenshot = xml_data['ApplicationSettings']['EnableScrenshotForSucess']
    context.AllStepsScreenshot = xml_data['ApplicationSettings']['EnableScrenshotForAllSteps']
    context.ParallelExecution = xml_data['ApplicationSettings']['ParallelExecution']
    context.SeparateFailureReport = xml_data['ApplicationSettings']['EnableSeprateFailureReport']
    context.ReportFolder = xml_data['ApplicationSettings']['ReportFolder']
    context.KobitonApp = xml_data['ApplicationSettings']['KobitonApp']
    context.IsRealMobile = xml_data['ApplicationSettings']['isRealMobile']
    context.appKey = xml_data['ApplicationSettings']['lambdaTestAppKey']
    context.TestEnvironment = xml_data['ApplicationSettings']['testEnvironment']
    context.UserName = xml_data['ApplicationSettings']['LT_USERNAME']
    context.AccessKey = xml_data['ApplicationSettings']['LT_ACCESS_KEY']
    context.xcodeOrgId = xml_data['ApplicationSettings']['xcodeOrgId']
    context.xcodeSigningId = xml_data['ApplicationSettings']['xcodeSigningId']
    context.bundleId = xml_data['ApplicationSettings']['bundleId']
    context.eachStepMessage = []
    context.CopiedList = []
    context.dict_api_response = {}
    tempreport = os.getcwd() + "//" + context.ReportFolder + "//"
    tempscreenshot = os.getcwd() + "//" + context.ReportFolder + "//screenshots"
    if not os.path.exists(tempscreenshot):
        os.makedirs(tempscreenshot)
    filename = "Report.txt"
    context.LogFile = os.path.join(tempreport, filename)
    f = open(context.LogFile, "w+")
    f.write("Start_Time= " + str(starttime))
    f.write("\nOS=" + str(os_version))
    f.write("\nUser=" + str(user))
    f.write("\nautName=" + str(context.autName))
    f.write("\nautType=" + str(context.autType))
    f.write("\nmobileOSVersion=" + str(context.platformVersion))
    f.write("\nFailureScreenshot=" + context.FailureScreenshot)
    f.write("\nSuccessScreenshot=" + context.PassedScreenshot)
    f.write("\nAllStepScreenshot=" + context.AllStepsScreenshot)
    f.write("\nseparateFailReport=" + context.SeparateFailureReport)
    f.close()
    context.list_tags = []
    context.URL = xml_data['ApplicationSettings']['URL']
    context.status = ''
    context.scenarioName = ''
    context.softFailurelist = []


def after_scenario(context, scenario):
    context.driver.quit()


def before_scenario(context, scenario):
    if context.TestEnvironment == 'lambdatest':
        options = UiAutomator2Options().load_capabilities({
            'lt:options': {
                'w3c': True,
                'platformName': context.platformName,
                'deviceName': context.deviceName,
                'platformVersion': context.platformVersion,
                'isRealMobile': True,
                'app': context.appKey
            }
        })
        url = "https://" + context.UserName + ":" + context.AccessKey + "@mobile-hub.lambdatest.com/wd/hub"
        context.driver = webdriver.Remote(url, options=options)
    elif context.TestEnvironment == 'browserstack':
        url = "http://" + context.UserName + ":" + context.AccessKey + "@hub-cloud.browserstack.com/wd/hub"
        option = {'os_version': context.platformVersion,
                  'device': context.deviceName,
                  'real_mobile': context.IsRealMobile,
                  'browserName': context.browserName,
                  'browserVersion': context.browserversion}
        context.driver = webdriver.Remote(command_executor=url, desired_capabilities=option)
    else:
        if str(context.mobileAutomationType).lower().replace(" ", "") == "androidapp":
            cap: Dict[str, Any] = {
                'platformName': context.platformName,
                'automationName': context.automationName,
                'deviceName': context.deviceName,
                'appPackage': context.appPackage,
                'appActivity': context.appActivity,
                'newCommandTimeout': '5000'
            }
            url = context.RemoteUrl
            context.driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))
        elif str(context.mobileAutomationType).lower().replace(" ", "") == "iosapp":
            cap: Dict[str, Any] = {
                'platformName': context.platformName,
                'automationName': context.automationName,
                'deviceName': context.deviceName,
                'xcodeOrgId': context.xcodeOrgId,
                'xcodeSigningId': context.xcodeSigningId,
                'udid': context.udid,
                'platformVersion': context.platformVersion,
                'bundleId': context.bundleId,
                'newCommandTimeout': '5000'
            }
            url = context.RemoteUrl
            context.driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))
        else:
            cap: Dict[str, Any] = {
                'platformName': context.platformName,
                'automationName': context.automationName,
                'deviceName': context.deviceName,
                'udid': context.udid,
                'browserName': context.browserName,
                'newCommandTimeout': '10000'
            }
            url = context.RemoteUrl
            context.driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))
            context.driver.get(context.autName)
    context.driver.update_settings({"waitForIdleTimeout": 100})
    context.eachStepMessage = []
    context.StepNumber = 0
    context.eachStepMessage = []
    context.list_tags = scenario.tags
    context.scenarioName = scenario.name
    context.list_tag = ""
    for i in context.list_tags:
        if "test" in i:
            context.list_tag = i


def after_step(context, step):
    context.StepNumber = context.StepNumber + 1
    f = open(context.LogFile, "a+" , encoding='utf-8')
    f.write("\n" + str(context.list_tags))
    f.write("\n" + str(context.scenarioName))
    f.write("\n" + str(step) + "StepNumber|" + str(context.StepNumber) + "|StepNumber")
    if context.AllStepsScreenshot == "True":
        date = str(datetime.now()).replace(' ', '')
        date = date.replace('-', '')
        date = date.replace(':', '')
        date = date.replace('.', '')
        img = context.list_tag + '_' + date
        directory = '%s/' % os.getcwd()
        tempimage = '/' + context.ReportFolder + '/screenshots/' + img + '.png'
        context.driver.save_screenshot(directory + tempimage)
        f.write("\nscreenshot|" + img + ".png|screenshot")
    else:
        if context.FailureScreenshot == "True":
            if step.status == 'failed':
                context.status == 'failed'
                date = str(datetime.now()).replace(' ', '')
                date = date.replace('-', '')
                date = date.replace(':', '')
                date = date.replace('.', '')
                img = context.list_tag + '_' + date
                directory = '%s/' % os.getcwd()
                tempimage = '/' + context.ReportFolder + '/screenshots/' + img + '.png'
                context.driver.save_screenshot(directory + tempimage)
                f.write("\nscreenshot|" + img + ".png|screenshot")
        if context.PassedScreenshot == "True":
            if str(step).find("then") != -1:
                if step.status == 'passed':
                    date = str(datetime.now()).replace(' ', '')
                    date = date.replace('-', '')
                    date = date.replace(':', '')
                    date = date.replace('.', '')
                    img = context.list_tag + '_' + date
                    directory = '%s/' % os.getcwd()
                    tempimage = '/' + context.ReportFolder + '/screenshots/' + img + '.png'
                    context.driver.save_screenshot(directory + tempimage)
                    f.write("\nscreenshot|" + img + ".png|screenshot")
        messagelength = len(context.eachStepMessage)
        for i in range(messagelength):
            f.write("\nMessage|" + context.eachStepMessage[i] + "|Message")
        f.close()
        context.eachStepMessage = []


def after_all(context):
    endtime = datetime.now()
    f = open(context.LogFile, "a+", encoding='utf-8')
    f.write("\nEnd_Time=" + str(endtime))
    f.close()
    try:
        if str(context.mobileAutomationType).lower().replace(" ", "").__contains__("ios"):
            reportfolder = os.getcwd() + "/TestReports"
            if not os.path.exists(reportfolder):
                os.makedirs(reportfolder)
            finalreportfile = reportfolder + "/TestReport_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            if not os.path.exists(finalreportfile):
                os.makedirs(finalreportfile)
            oldapth = os.getcwd() + "/Temp"
            file_names = os.listdir(oldapth)
            for file_name in file_names:
                shutil.move(os.path.join(oldapth, file_name), finalreportfile)
            os.rmdir(oldapth)
            reportpath = finalreportfile + "/report.html"
            cmd_command = "mono algoReport.exe behave \"" + finalreportfile + "\" \"" + reportpath + "\""
            target_directory = os.getcwd()
            os.chdir(target_directory)
            subprocess.run(cmd_command, shell=True)
        else:
            reportfolder = os.getcwd() + "\\TestReports"
            if not os.path.exists(reportfolder):
                os.makedirs(reportfolder)
            finalreportfile = reportfolder + "\\TestReport_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            if not os.path.exists(finalreportfile):
                os.makedirs(finalreportfile)
            oldapth = os.getcwd() + "\\Temp"
            file_names = os.listdir(oldapth)
            for file_name in file_names:
                shutil.move(os.path.join(oldapth, file_name), finalreportfile)
            os.rmdir(oldapth)
            reportpath = finalreportfile + "\\report.html"
            cmd_command = "algoReport.exe behave \"" + finalreportfile + "\" \"" + reportpath + "\""
            target_directory = os.getcwd()
            os.chdir(target_directory)
            subprocess.run(cmd_command, shell=True)
    except Exception as e:
        print("Exception------------ " + e)

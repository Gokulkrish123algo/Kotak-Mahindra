# pylint:disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-wildcard-import
# pylint: disable=undefined-variable
# pylint: disable=function-redefined
import os
import sys
from behave import *
import myaddressworkflow
import assertion

currentDir = os.getcwd()
previousDir = os.path.dirname(currentDir) + '/' + 'shared' + '/' + 'steps'
sys.path.append(previousDir)


def parse_string(text):
	return text.strip()


register_type(Name=parse_string)
use_step_matcher("cfparse")

        
@when("I entered Name in my address as '{var_name:Name?}'")
def step(context,var_name):
     myaddressworkflow.textboxnameentered(context,var_name)
    
@when("I entered Mobile No in my address as '{var_mobileNo:Name?}'")
def step(context,var_mobileNo):
     myaddressworkflow.textboxmobilenoentered(context,var_mobileNo)
    
@when("I entered PIN CODE in my address as '{var_pinCode:Name?}'")
def step(context,var_pinCode):
     myaddressworkflow.textboxpincodeentered(context,var_pinCode)
    
@when("I entered Address in my address as '{var_address:Name?}'")
def step(context,var_address):
     myaddressworkflow.textboxaddressentered(context,var_address)
    
@when("I scroll and click Work in my address")
def step(context):
     myaddressworkflow.buttonworkscrollandclick(context)
    
@when("I selected Add new address in my address")
def step(context):
     myaddressworkflow.buttonaddnewaddressselected(context)
    
@when("I selected Delete in my address")
def step(context):
     myaddressworkflow.buttondeleteselected(context)
    
@when("I selected yes in my address")
def step(context):
     myaddressworkflow.buttonyesselected(context)
    
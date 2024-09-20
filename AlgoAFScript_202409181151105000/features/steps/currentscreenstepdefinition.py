# pylint:disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-wildcard-import
# pylint: disable=undefined-variable
# pylint: disable=function-redefined
import os
import sys
from behave import *
import currentscreenworkflow
import assertion

currentDir = os.getcwd()
previousDir = os.path.dirname(currentDir) + '/' + 'shared' + '/' + 'steps'
sys.path.append(previousDir)


def parse_string(text):
	return text.strip()


register_type(Name=parse_string)
use_step_matcher("cfparse")

        
@when("I selected Account Menu in home page catagories")
def step(context):
     currentscreenworkflow.buttonaccountmenuselected(context)
    
@when("I selected My profile in my account")
def step(context):
     currentscreenworkflow.buttonmyprofileselected(context)
    
@then("'{var_page:Name?}' is displayed with '{var_content:Name?}'")
def step(context,var_page,var_content):
    assertion.assert_true(context,currentscreenworkflow.pagedefaultpagedisplayed(context,var_page))
    assertion.assert_true(context, currentscreenworkflow.labelmessagedisplayed(context,var_content))
    if str(context.softAssertion).lower() == 'true':
          assertion.assert_all(context)
    else:
          pass
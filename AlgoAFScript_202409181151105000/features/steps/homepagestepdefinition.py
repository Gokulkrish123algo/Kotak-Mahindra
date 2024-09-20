# pylint:disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-wildcard-import
# pylint: disable=undefined-variable
# pylint: disable=function-redefined
import os
import sys
from behave import *
import homepageworkflow
import assertion

currentDir = os.getcwd()
previousDir = os.path.dirname(currentDir) + '/' + 'shared' + '/' + 'steps'
sys.path.append(previousDir)


def parse_string(text):
	return text.strip()


register_type(Name=parse_string)
use_step_matcher("cfparse")

        
@given("I have access to application")
def step(context):
     homepageworkflow.pageloginpageaccesstopage(context)
    
Feature: SSB project1
#Regression Type
#Correct Values = true
#Incorrect Values = false
#Illegal Values = false
#Invalid Values = false
#Boundary Values = false
#Edge Cases Values = false

@Add_addresss
@uid895621424
@set21
@test001
Scenario Outline: User able to add the address
Given I have access to application
When I selected Account Menu in home page catagories
And I selected My profile in my account
And I selected Add address in my address
And I entered Name in my address as '<Name>'
And I entered Mobile No in my address as '<Mobile No>'
And I entered PIN CODE in my address as '<PIN CODE>'
And I entered Address in my address as '<Address>'
And I scroll and click Work in my address
And I selected Add new address in my address
And I selected Delete in my address
And I selected yes in my address
And I selected Account Menu in home page catagories
Then '<page>' is displayed with '<content>'

Examples:
|SlNo.|Name|Mobile No|PIN CODE|Address|page|content|
|1|gokul R|6385250471|560102|3rd street ,HSR |Current Screen|NA|


#Total No. of Test Cases : 1


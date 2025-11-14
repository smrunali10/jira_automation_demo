#*** Settings ***
#Resource    ../resources/ApiKeywords.robot
#Library     ../Library/JiraUI.py
#
#*** Variables ***
#${EMAIL}       smrunali46@gmail.com
#${PASSWORD}    Sonawane
#
#*** Test Cases ***
#Create And Validate Epic
#    ${epic_key}=    Create Jira Epic    ${EMAIL}    ${API_TOKEN}
#    Log To Console   Epic created via API: ${epic_key}
#
#    Start Browser Session
#    Login To Jira    ${EMAIL}    ${PASSWORD}
#    Open Jira Project Board    ${PROJECT_KEY}
#    Validate Epic Visible By Key    ${epic_key}
#    Close Browser Session



#*** Settings ***
#Library    ../Library/JiraDoppler.py
#Library    ../Library/JiraUI.py
#Resource   ../resources/ApiKeywords.robot
#
#Suite Setup    INITIALIZE SECRETS
#
#*** Test Cases ***
#Create And Validate Epic
#    ${epic_key}=    Create Jira Epic    ${EMAIL}    ${API_TOKEN}
#    Log To Console   Epic created via API: ${epic_key}
#
#    Start Browser Session
#    Login To Jira   ${EMAIL}     ${PASSWORD}
#    Open Jira Project Board    ${PROJECT_KEY}
#    Validate Epic Visible By Key    ${epic_key}
#    Close Browser Session

*** Settings ***
Resource    ../resources/ApiKeywords.robot
Library     ../Library/JiraUI.py
Library     ../Library/JiraDoppler.py
Suite Setup    INITIALIZE SECRETS

*** Test Cases ***
Create And Validate Epic
    [Tags]    API   UI
    ${epic_key}=    Create Jira Epic    ${EMAIL}    ${API_TOKEN}
    Log To Console   Epic created via API: ${epic_key}
    Set Suite Variable    ${epic_key}

    Start Browser Session
    Login To Jira   ${EMAIL}     ${PASSWORD}
    Open Jira Project Board    ${PROJECT_KEY}
    Validate Epic Visible By Key    ${epic_key}
    Close Browser Session

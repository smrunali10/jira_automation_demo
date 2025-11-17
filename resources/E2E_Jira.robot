*** Settings ***
Resource    ../resources/ApiKeywords.robot
Library     ../Library/JiraUI.py

*** Variables ***
${EMAIL}       smrunali46@gmail.com
${PASSWORD}    Sonawane

*** Test Cases ***
Create And Validate Epic
    [Tags]    Create    Validate
    ${epic_key}=    Create Jira Epic    ${EMAIL}    ${API_TOKEN}
    Log To Console   Epic created via API: ${epic_key}

    Start Browser Session
    #Login To Jira    ${EMAIL}    ${PASSWORD}
    Login With Cookies Or Fallback
    Open Jira Project Board    ${PROJECT_KEY}
    Validate Epic Visible By Key    ${epic_key}
    Close Browser Session
#------------------------------------------------------------------------------------------------

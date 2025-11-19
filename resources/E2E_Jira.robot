*** Settings ***
Resource    ../resources/ApiKeywords.robot
Library     ../Library/JiraUI.py
Library     ../Library/JiraDoppler.py

Suite Setup   INITIALIZE SECRETS

*** Test Cases ***
Create Epic Via Api And Validate Via Ui

    [Tags]    Create-Api    Validate-Ui
    ${epic_key}=    Create Jira Epic    ${EMAIL}    ${API_TOKEN}
    Log To Console   Epic created via API: ${epic_key}
    Start Browser Session
    Login With Cookies Or Fallback
    Open Jira Project Board    ${PROJECT_KEY}
    Validate Epic Visible By Key    ${epic_key}
    Close Browser Session
    Delete Jira Epic    ${epic_key}    ${EMAIL}    ${API_TOKEN}

Create Epic With Invalid Project Key
    [Tags]    Negative-Api
    Create Epic With Invalid Project Key    ${EMAIL}    ${API_TOKEN}

Delete Nonexistent Epic
    [Tags]    Negative-Api
    ${fake_epic_key}=    Set Variable    EPIC-99999
    Run Keyword And Expect Error    *Status code verification failed*
    ...    Delete Jira Epic    ${fake_epic_key}    ${EMAIL}    ${API_TOKEN}
    Log To Console    Negative test passed: Deletion of non-existent Epic failed as expected
#*** Settings ***
#Library    RESTLibrary
#Library    Collections
#Resource   JiraVariables.robot
#
#*** Keywords ***
#Create Jira Headers
#    [Arguments]    ${content_type}=application/json
#    ${headers}=    Create Dictionary
#    ...    Content-Type=${content_type}
#    ...    Accept=application/json
#    RETURN    ${headers}
#
#Create Jira Epic
#    [Arguments]    ${email}    ${token}
#    ${request_id}=    Set Variable    create_epic_${TEST NAME}
#    ${HEADERS}=       Create Jira Headers
#    ${project}=       Create Dictionary    key=${PROJECT_KEY}
#    ${issuetype}=     Create Dictionary    name=Epic
#    ${fields}=        Create Dictionary
#    ...    project=${project}
#    ...    summary=Created Epic using API
#    ...    description=Created Epic using API
#    ...    issuetype=${issuetype}
#    ${payload}=       Create Dictionary    fields=${fields}
#
#    Make HTTP Request
#    ...    ${request_id}
#    ...    ${BASE_URL}/rest/api/2/issue
#    ...    method=POST
#    ...    requestHeaders=${HEADERS}
#    ...    requestBody=${payload}
#    ...    expectedStatusCode=201
#    ...    authType=Basic
#    ...    username=${email}
#    ...    password=${token}
#
#    ${epic_key}=    Extract From Response    ${request_id}    $.key
#    Log    Epic created: ${epic_key}
#    RETURN    ${epic_key}
#
#Extract From Response
#    [Arguments]    ${request_id}    ${json_path}
#    ${value}=    Execute RC    <<<rc, ${request_id}, body, ${json_path}>>>
#    RETURN    ${value}
#
#Validate Epic Description
#    [Arguments]    ${epic_key}    ${expected_description}    ${email}    ${token}
#    ${request_id}=    Set Variable    validate_epic_${TEST NAME}
#    ${HEADERS}=       Create Jira Headers
#
#    Make HTTP Request
#    ...    ${request_id}
#    ...    ${BASE_URL}/rest/api/2/issue/${epic_key}
#    ...    method=GET
#    ...    requestHeaders=${HEADERS}
#    ...    expectedStatusCode=200
#    ...    authType=Basic
#    ...    username=${email}
#    ...    password=${token}
#
#    ${actual_description}=    Extract From Response    ${request_id}    $.fields.description
#    Log    Actual description: ${actual_description}
#    Should Be Equal    ${actual_description}    ${expected_description}

*** Settings ***
Library    RESTLibrary
Library    Collections
Resource   JiraVariables.robot

*** Keywords ***
Create Jira Headers
    [Arguments]    ${content_type}=application/json
    ${headers}=    Create Dictionary
    ...    Content-Type=${content_type}
    ...    Accept=application/json
    RETURN    ${headers}

Create Jira Epic
    [Arguments]    ${email}    ${token}
    ${request_id}=    Set Variable    create_epic_${TEST NAME}
    ${HEADERS}=       Create Jira Headers
    ${project}=       Create Dictionary    key=${PROJECT_KEY}
    ${issuetype}=     Create Dictionary    name=Epic
    ${fields}=        Create Dictionary
    ...    project=${project}
    ...    summary=Created Epic using API
    ...    description=Created Epic using API
    ...    issuetype=${issuetype}
    ${payload}=       Create Dictionary    fields=${fields}

    Make HTTP Request
    ...    ${request_id}
    ...    ${BASE_URL}/rest/api/2/issue
    ...    method=POST
    ...    requestHeaders=${HEADERS}
    ...    requestBody=${payload}
    ...    expectedStatusCode=201
    ...    authType=Basic
    ...    username=${email}
    ...    password=${token}

    ${epic_key}=    Extract From Response    ${request_id}    $.key
    Log    Epic created: ${epic_key}
    RETURN    ${epic_key}

Extract From Response
    [Arguments]    ${request_id}    ${json_path}
    ${value}=    Execute RC    <<<rc, ${request_id}, body, ${json_path}>>>
    RETURN    ${value}

Validate Epic Description
    [Arguments]    ${epic_key}    ${expected_description}    ${email}    ${token}
    ${request_id}=    Set Variable    validate_epic_${TEST NAME}
    ${HEADERS}=       Create Jira Headers

    Make HTTP Request
    ...    ${request_id}
    ...    ${BASE_URL}/rest/api/2/issue/${epic_key}
    ...    method=GET
    ...    requestHeaders=${HEADERS}
    ...    expectedStatusCode=200
    ...    authType=Basic
    ...    username=${email}
    ...    password=${token}

    ${actual_description}=    Extract From Response    ${request_id}    $.fields.description
    Log    Actual description: ${actual_description}
    Should Be Equal    ${actual_description}    ${expected_description}

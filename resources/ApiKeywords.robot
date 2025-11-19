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

Delete Jira Epic
    [Arguments]    ${epic_key}    ${email}    ${token}
    ${request_id}=    Set Variable    delete_${epic_key}
    ${HEADERS}=       Create Jira Headers
    Make HTTP Request
    ...    ${request_id}
    ...    ${BASE_URL}/rest/api/2/issue/${epic_key}
    ...    method=DELETE
    ...    requestHeaders=${HEADERS}
    ...    expectedStatusCode=204
    ...    authType=Basic
    ...    username=${email}
    ...    password=${token}

    Log To Console    Deleted Epic: ${epic_key}

Create Epic With Invalid Project Key
    [Arguments]    ${email}    ${token}
    ${invalid_project}=    Create Dictionary    key=FAKE123
    ${issuetype}=          Create Dictionary    name=Epic
    ${fields}=             Create Dictionary
    ...    project=${invalid_project}
    ...    summary=Invalid Epic
    ...    description=This should fail
    ...    issuetype=${issuetype}
    ${payload}=            Create Dictionary    fields=${fields}

    ${request_id}=    Set Variable    invalid_epic_${TEST NAME}
    ${HEADERS}=       Create Jira Headers
    Make HTTP Request
    ...    ${request_id}
    ...    ${BASE_URL}/rest/api/2/issue
    ...    method=POST
    ...    requestHeaders=${HEADERS}
    ...    requestBody=${payload}
    ...    expectedStatusCode=400
    ...    authType=Basic
    ...    username=${email}
    ...    password=${token}

    Log To Console    Negative test passed: Epic creation failed as expected
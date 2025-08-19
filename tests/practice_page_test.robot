*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Practice Page Automation
    Open Browser    https://rahulshettyacademy.com/AutomationPractice/    edge
    Maximize Browser Window
    
    # Select Radio3
    Select Radio Button    radioButton    radio3
    
    # Verify suggestion class textbox
    Page Should Contain Textfield    xpath://input[@placeholder='Type to Select Countries']
    
    # Type and select India
    Input Text    id:autocomplete    Ind
    Wait Until Element Is Visible    xpath://ul[@id='ui-id-1']//div[text()='India']
    Click Element    xpath://ul[@id='ui-id-1']//div[text()='India']
    
    # Select Option2 from dropdown
    Select From List By Value    id:dropdown-class-example    option2
    
    # Select checkboxes
    Select Checkbox    id:checkBoxOption1
    Select Checkbox    id:checkBoxOption3
    
    # Handle new tab
    Click Element    id:opentab
    Switch Window    NEW
    Close Window
    Switch Window    MAIN
    
    # Handle Alert
    Input Text    id:name    Mrinmoy
    Click Element    id:confirmbtn
    Alert Should Be Present    Hello Mrinmoy, Are you sure you want to confirm?    ACCEPT
    
    # Close browser
    Close Browser

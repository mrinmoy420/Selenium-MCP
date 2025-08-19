*** Settings ***
Library    SeleniumLibrary
Library    Process
Library    OperatingSystem

*** Keywords ***
Setup ChromeDriver
    ${result}=    Run Process    python    -c    from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())
    Set Environment Variable    PATH    ${result.stdout}

*** Test Cases ***
Radio Button Test
    Setup ChromeDriver
    Open Browser    https://rahulshettyacademy.com/AutomationPractice/    chrome
    Click Element    css:input[value='radio3']
    Sleep    2s    # Adding a small delay to ensure the element is clicked
    Close Browser

cd .\Tests\ 
pytest -v -s --alluredir="./target/allure-reports"
@REM to check the Allure logs navigate to target folder and run  "allure serve .\allure-reports\"
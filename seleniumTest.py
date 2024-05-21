from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from termcolor import colored
from tqdm import tqdm
import itertools

# Create a new Firefox profile
profile = webdriver.FirefoxProfile()

# Set up the WebDriver with the new profile
service = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=service)

# Open the URL
driver.get("https://cirillom.github.io/cadastro-usuario/")

input_name_element = driver.find_element(By.ID, "inputName")
input_name_help_element = driver.find_element(By.ID, "inputNameHelp")

input_year_element = driver.find_element(By.ID, "inputYear")
input_year_help_element = driver.find_element(By.ID, "inputYearHelp")

input_email_element = driver.find_element(By.ID, "inputEmail")
input_email_help_element = driver.find_element(By.ID, "inputEmailHelp")

input_password_element = driver.find_element(By.ID, "inputPassword")
input_password_help_element = driver.find_element(By.ID, "inputPasswordHelp")
input_password_strength_element = driver.find_element(By.ID, "passStrengthMeter")

input_button_element = driver.find_element(By.ID, "submitButton")
input_result_element = driver.find_element(By.ID, "inputResult")

# input (name, expected name result)
nameTests = [
    ("Carlos", "Formato de nome inválido"),
    ("Fernanda", ""),
    ("Ana123", "Formato de nome inválido"),
    ("Jose@123", "Formato de nome inválido"),
    ("Maria Clara", "Formato de nome inválido"),
    ("", "Formato de nome inválido"),
    ("Joaquina", ""),
    ("JoaoPa", "Formato de nome inválido"),
    ("Maria", "Formato de nome inválido"),
    ("Ana", "Formato de nome inválido"),
    ("Beatriz", "")
]

# input (year, expected year result)
yearTests = [
    ("aa20", "Formato de ano inválido"),
    ("matheus", "Formato de ano inválido"),
    ("1900", ""),
    ("2022", ""),
    ("2023", "Ano inválido. O ano não pode ser maior que ${maxYear}."),
    ("1800", "Ano inválido. O ano não pode ser menor que 1900."),
    ("2021", "")
]

# input (email, expected email result)
emailTests = [
    ("usuario@dominio.com", ""),
    ("usuario123@dominio.org", ""),
    ("usuario@dominio.br", ""),
    ("usuario@dominio.net", ""),
    ("usuario@dominio.com.br", "Formato de email inválido"),
    ("usuario@dominio", "Formato de email inválido"),
    ("usuario@.com", "Formato de email inválido"),
    ("@dominio.com", "Formato de email inválido"),
    ("usuario@dominio.c", "Formato de email inválido"),
    ("usuario@dominio.comm", "Formato de email inválido"),
    ("usuario@dominio.con", "Formato de email inválido"),
    ("usuário@domínio.com", "Formato de email inválido"),
    ("user@domain.co.uk", "Formato de email inválido"),
    ("user.name@domain.com", "Formato de email inválido"),
    ("username@domain.net.org", "Formato de email inválido")
]

# input (password, expected password result, expected password strength)
passwordTests = [
    ("Pass@123", "moderada", 20),
    ("pass@123", "fraca", 10),
    ("P@ss1234", "moderada", 20),
    ("P@ssw0rd123", "moderada", 20),
    ("P@ssw0rd123456", "forte", 30),
    ("P@ssw0rd1234!6", "forte", 30),
    ("senha@123", "moderada", 20),
    ("senha@1234567890", "forte", 30),
    ("user@2021", "Senha inválida", 0),
    ("Senha@123", "Senha inválida", 0),
    ("P@ss!", "Senha inválida", 0),
    ("123456", "Senha inválida", 0),
    ("Aa@1", "Senha inválida", 0)
]

tests = {}
testCount = 0
total_iterations = len(nameTests) * len(yearTests) * len(emailTests) * len(passwordTests)

#open file to write tests
f = open("tests.csv", "w")
f.write("Test,Name,ExpectedNameResult,Year,ExpectedYearResult,Email,ExpectedEmailResult,Password,ExpectedPasswordResult,ExpectedPasswordStrength,ExpectedResult\n")

# Use itertools.product to create a Cartesian product of the tests
for (name, x_name_result), (year, x_year_result), (email, x_email_result), (password, x_password_result, x_strength_result) in tqdm(itertools.product(nameTests, yearTests, emailTests, passwordTests), total=total_iterations):
                testCount += 1

                tests[testCount] = {}

                x_result = "Formulário inválido!"
                if x_name_result == "" and x_year_result == "" and x_email_result == "" and "Senha inválida." not in x_password_result:
                    x_result = "Dados registrados com sucesso!"

                # Write the test to the file
                f.write(f"{testCount},{name},{x_name_result},{year},{x_year_result},{email},{x_email_result},{password},{x_password_result},{x_strength_result},{x_result}\n")

                input_name_element.clear()
                input_name_element.send_keys(name)

                input_year_element.clear()
                input_year_element.send_keys(year)

                input_email_element.clear()
                input_email_element.send_keys(email)

                input_password_element.clear()
                input_password_element.send_keys(password)

                input_button_element.click()
                input_button_element.click()

                tests[testCount]["name"] = (input_name_help_element.text, x_name_result, (input_name_help_element.text == x_name_result))
                tests[testCount]["year"] = (input_year_help_element.text, x_year_result, (input_year_help_element.text == x_year_result))
                tests[testCount]["email"] = (input_email_help_element.text, x_email_result, (input_email_help_element.text == x_email_result))
                tests[testCount]["password"] = (input_password_help_element.text, x_password_result, (x_password_result in input_password_help_element.text))
                tests[testCount]["strength"] = (input_password_strength_element.text, x_strength_result, (input_password_strength_element.get_attribute("value") == x_strength_result))
                tests[testCount]["submit"] = (input_result_element.text, x_result, (input_result_element.text == x_result))

                if all(value[2] == True for value in tests[testCount].values()):
                    tests[testCount]["result"] = True
                else:
                    tests[testCount]["result"] = False
f.close()
#count sucessfull tests
successfullTests = 0
for key, value in tests.items():
    if value["result"] == True:
        successfullTests += 1

print(colored(f"Total of {successfullTests} / {testCount}", "blue"))
for key, value in tests.items():
    if value["result"] == True:
        print(colored(f"Test {key}: Successful", "green"))
    else:
        print(colored(f"Test {key}: Failed on: ", "red"))
        for k, v in value.items():
            if k != "result":
                if v[2] == False:
                    print(colored(f"\t{k}: got \"{v[0]}\" ", "red"))

# Close the browser
driver.quit()

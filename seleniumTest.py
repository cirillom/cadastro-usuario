from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from termcolor import colored
from tqdm import tqdm
import itertools

# Set up the WebDriver with the new profile
service = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=service)

#driver = webdriver.Chrome() #use chrome if not on ubuntu

# Open the URL
driver.get("https://guscarenci.github.io/desafioWebDev/")

input_name_element = driver.find_element(By.ID, "inputName")
input_name_help_element = driver.find_element(By.ID, "inputNameHelp")

input_year_element = driver.find_element(By.ID, "inputYear")
input_year_help_element = driver.find_element(By.ID, "inputYearHelp")

input_email_element = driver.find_element(By.ID, "inputEmail")
input_email_help_element = driver.find_element(By.ID, "inputEmailHelp")

input_password_element = driver.find_element(By.ID, "inputPassword")
input_password_help_element = driver.find_element(By.ID, "inputPasswordHelp")
input_password_strength_element = driver.find_element(By.ID, "passStrengthMeter")

input_button_element = driver.find_element(By.CSS_SELECTOR, ".btn")
input_result_element = driver.find_element(By.ID, "formMessage")

def make_test(tests, testCount, name, x_name_result, year, x_year_result, email, x_email_result, password, x_password_result, x_strength_result):
    tests[testCount] = {}

    x_result = "Seus dados não foram registrados!"
    if x_name_result == "" and x_year_result == "" and x_email_result == "" and "inválida" not in x_password_result:
        x_result = "Seus dados foram registrados!"

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

    tests[testCount]["name"] = (input_name_help_element.text, x_name_result, (x_name_result in input_name_help_element.text))
    tests[testCount]["year"] = (input_year_help_element.text, x_year_result, (x_year_result in input_year_help_element.text))
    tests[testCount]["email"] = (input_email_help_element.text, x_email_result, (x_email_result in input_email_help_element.text))
    tests[testCount]["password"] = (input_password_help_element.text, x_password_result, (x_password_result in input_password_help_element.text))
    tests[testCount]["strength"] = (input_password_strength_element.text, x_strength_result, (input_password_strength_element.get_attribute("value") == x_strength_result))
    tests[testCount]["submit"] = (input_result_element.text, x_result, (x_result in input_result_element.text))

    if all(value[2] == True for value in tests[testCount].values()):
        tests[testCount]["result"] = True
    else:
        tests[testCount]["result"] = False

# input (name, expected name result)
nameTests = [
    ("Matheus", ""), #Caso com apenas letras
    ("m4theus", "inválido"), #Caso com letras e número
    ("matheus cirillo", "inválido"), #Caso com letras e número
    ("m@theus", "inválido"), #Caso com letras e caracteres
    ("mat", "inválido") #Caso com menos de 6 letras
]

# input (year, expected year result)
yearTests = [
    ("2003", ""), #caso válido
    ("1900", ""), #caso de borda válido
    ("2022", ""), #caso de borda válido
    ("2023", "inválido"), #caso onde é maior que 2022
    ("1899", "inválido"), #caso onde é menor que 1900
    ("matheus", "inválido") #caso com letras
]

# input (email, expected email result)
emailTests = [
    ("usuario@dominio.net", ""),
    ("usu4rio@dominio.com", ""),
    ("matheus@usp.br", ""),
    ("123456789@dominio.org", ""),
    ("usu!rio@dominio.com", "inválido"),  # letras, números e símbolos antes do @
    ("@dominio.com", "inválido"),  # nada antes do @
    ("usuario@dom!nio.com", "inválido"),  # letras, números e símbolos entre @ e .
    ("usuario@.com", "inválido"),  # nada entre @ e .
    ("usuario@dominio.usp", "inválido")  # final usp depois do .
]

# input (password, expected password result, expected password strength)
passwordTests = [
    ("a1!b", "inválida", "0"), #senha com menos de 6 caracteres
    ("a1!b2c3d4@@f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0", "inválida", "0"), #senha com mais de 20 caracteres
    ("abcdefgh123", "inválida", "0"), #senha sem caracter especial
    ("abcdefgh!", "inválida", "0"), #senha sem número
    ("12345678!", "inválida", "0"), #senha sem letra
    ("abcde1!", "fraca", "10"), #senha fraca
    ("Abcde1!fgh", "moderada", "20"), #senha moderada
    ("ABcd123!@fgHI", "forte", "30") #senha forte
]

tests = {}
testCount = 0
total_iterations = len(nameTests) * len(yearTests) * len(emailTests) * len(passwordTests)

#open file to write tests
f = open("tests.csv", "w")
f.write("Test,Name,ExpectedNameResult,Year,ExpectedYearResult,Email,ExpectedEmailResult,Password,ExpectedPasswordResult,ExpectedPasswordStrength,ExpectedResult\n")

all_tests = itertools.product(nameTests, yearTests, emailTests, passwordTests)

#hardcoded tests to check password handling name and year
year_in_pass = (("Matheus", ""), ("2003", ""), ("123456789@dominio.org", ""), ("pabx!@#2003", "inválida", "0"))
name_in_pass = (("Matheus", ""), ("2003", ""), ("123456789@dominio.org", ""), ("matheus123@", "inválida", "0"))
all_tests = list(all_tests)
all_tests.append(year_in_pass)
all_tests.append(name_in_pass)

# Use itertools.product to create a Cartesian product of the tests
for (name, x_name_result), (year, x_year_result), (email, x_email_result), (password, x_password_result, x_strength_result) in tqdm(itertools.product(nameTests, yearTests, emailTests, passwordTests), total=total_iterations):
    testCount += 1
    make_test(tests, testCount, name, x_name_result, year, x_year_result, email, x_email_result, password, x_password_result, x_strength_result)


f.close()
#count sucessfull tests
successfullTests = 0
for key, value in tests.items():
    if value["result"] == True:
        successfullTests += 1

f = open("results.csv", "w")

print(colored(f"Total of {successfullTests} / {testCount}", "blue"))
f.write(f"Total of {successfullTests} / {testCount}")
for key, value in tests.items():
    if value["result"] == True:
        print(colored(f"Test {key}: Successful", "green"))
        f.write(f"Test {key}: Successful\n")
    else:
        print(colored(f"Test {key}: Failed on: ", "red"))
        f.write(f"Test {key}: Failed on: ")
        for k, v in value.items():
            if k != "result":
                if v[2] == False:
                    print(colored(f"\t{k}: got \"{v[0]}\" ", "red"))
                    f.write(f"\t{k}: got \"{v[0]}\"\n")

# Close the browser
driver.quit()

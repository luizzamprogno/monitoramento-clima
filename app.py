from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
from time import sleep
import smtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule

def iniciar_driver():
    chromedriver_path = "C:\\Meus documentos\\Desafios semanais\\Semana 1\\chromedriver-win64\\chromedriver.exe"
    chrome_options = Options()

    arguments = [
    '--lang=pt-BR',
    '--window-size=1200,800',
    '--incognito',
    '--disable-infobars'
    '--force-device-scale-factor=0.8'
    ]

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    
    wait = WebDriverWait(
        driver=driver,
        timeout=0,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )

    return driver, wait

def open_url(url):

    driver, wait = iniciar_driver()
    driver.get(url)

    return driver, wait

def find_city(wait, city):

    city_name = wait.until(expected_conditions.visibility_of_all_elements_located((By.ID, 'search_pc')))
    city_name[0].send_keys(city)
    city_name[0].send_keys(Keys.ENTER)
    sleep(5)

def get_day_temperature(driver, wait, xpath):
    day_temperature = wait.until(expected_conditions.visibility_of_all_elements_located((By.XPATH, xpath)))
    return day_temperature[0]

def get_day_condition(driver, wait, xpath):
    day_condition = wait.until(expected_conditions.visibility_of_all_elements_located((By.XPATH, xpath)))
    return day_condition[0]

def get_3_day_prediction(driver, day_xpath, max_xpath, min_xpath):

    prediction_day = driver.find_element(By.XPATH, day_xpath)
    prediction_max = driver.find_element(By.XPATH, max_xpath)
    prediction_min = driver.find_element(By.XPATH, min_xpath)

    return prediction_day, prediction_max, prediction_min

def write_content(day_temperature, day_condition, predictions):

    conteudo = f"""
    Temperatura de agora: {day_temperature}
    Condições climáticas do dia: {day_condition}

    Previsão para os próximos 3 dias:
    """
    for day, max_temp, min_temp in predictions:
        conteudo += f"""
    Dia: {day}
    Temperatura máxima: {max_temp}
    Temperatura mínima: {min_temp}
    """
    return conteudo

def send_email(smtp_server, smtp_port, smtp_user, smtp_password, from_email, to_email, subject, body):
    
    # Cria o e-mail
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adiciona o corpo do e-mail
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Envia o e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia a conexão TLS
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')
    finally:
        server.quit()

def schedule_email(duration):
    schedule.every(duration).seconds.do(main)

    while True:
        schedule.run_pending()
        sleep(1)

def main():
    
    url = 'https://www.tempo.com/'
    city = 'Oriente'
    temperature_xpath = "//span[@class='dato-temperatura changeUnitT']"
    condition_xpath = "//span[@class='descripcion']"

    # Configurações do servidor e credenciais
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'lpzampronio@gmail.com'
    smtp_password = 'epyx hyjd wtlc yzbv' # senha de app do Google

    # Informações do e-mail
    from_email = 'lpzampronio@gmail.com'
    to_email = 'lpzamprogno@gmail.com'
    subject = 'Previsão do tempo'

    driver, wait = open_url(url)
    find_city(wait, city)
    day_temperature = get_day_temperature(driver, wait, temperature_xpath)
    day_condition = get_day_condition(driver, wait, condition_xpath)

    predictions = []
    for day in range(2, 5): # d2, d3, d4
        day_xpath = f"//li[@class='grid-item dia d{day}']/span[@class='col day_col']/span[@class='text-0']"
        max_xpath = f"//li[@class='grid-item dia d{day}']/span[@class='col day_col']/span[@class='temp']/span[@class='max changeUnitT']"
        min_xpath = f"//li[@class='grid-item dia d{day}']/span[@class='col day_col']/span[@class='temp']/span[@class='min changeUnitT']"
    
        prediction_day, prediction_max, prediction_min = get_3_day_prediction(driver, day_xpath, max_xpath, min_xpath)
        predictions.append((prediction_day.text, prediction_max.text, prediction_min.text))
        
    body = write_content(day_temperature.text, day_condition.text, predictions)

    send_email(smtp_server, smtp_port, smtp_user, smtp_password, from_email, to_email, subject, body)

    driver.close()

if __name__ == '__main__':
    schedule_email(30)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep

# 1. Запускаем Firefox
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

try:
    # 2. Открываем главную страницу
    driver.get("https://itcareerhub.de/ru")
    print("Сайт открыт")

    # Ждём, пока страница загрузится
    sleep(3)

    # 3. Находим и кликаем по ссылке "Способы оплаты"
    link = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    link.click()
    print("Переход на 'Способы оплаты и рассрочка'")

    # 4. Ждём, пока загрузится новая страница с заголовком
    sleep(5)  # даём 4 секунды — этого достаточно для itcareerhub.de

    # 5. Делаем скриншот ВСЕГО окна — уже с нужной секцией
    driver.save_screenshot("payment_methods_section.png")
    print("Скриншот сохранён!")

finally:
    driver.quit()

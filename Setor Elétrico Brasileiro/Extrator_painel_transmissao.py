import time
import json
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

'''
    Extrai informações relevantes do Painel da Transmissão da Aneel
'''


class ExtractData:
    def __init__(self):
        options = FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.vars = {}

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        self.vars["window_handles"] = self.driver.window_handles
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def set_situacao(self):
        self.driver.find_element(
            By.ID, "ReportViewer1_ctl04_ctl03_ddDropDownButton").click()
        self.driver.find_element(
            By.CSS_SELECTOR, "tr:nth-child(1) > td > span > label").click()
        self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(4)").click()
        self.driver.find_element(
            By.ID, "ReportViewer1_ctl04_ctl05_ddValue").click()

    def itens_in_select(self):
        self.driver.find_element(
            By.ID, "ReportViewer1_ctl04_ctl05_ddValue").click()
        dropdown = self.driver.find_element(
            By.ID, "ReportViewer1_ctl04_ctl05_ddValue")
        select = Select(dropdown)
        return select, len(select.options)

    def set_select_option(self, value):
        self.driver.find_element(
            By.ID, "ReportViewer1_ctl04_ctl05_ddValue").click()
        dropdown = self.driver.find_element(
            By.ID, "ReportViewer1_ctl04_ctl05_ddValue")
        select = Select(dropdown)
        select.select_by_value(value)

        select = Select(dropdown)
        selected_option = select.first_selected_option
        option_value = selected_option.get_attribute("value")
        print("Opção selecionada:", selected_option.text)
        print("ID da opção selecionada:", selected_option.get_attribute("value"))
        return selected_option.text

    def searching(self):
        self.driver.find_element(
            By.CSS_SELECTOR, "option:nth-child(1)").click()
        self.driver.find_element(By.ID, "ReportViewer1_ctl04_ctl00").click()

    def exporting(self):
        # Abrindo opções de export
        wait = WebDriverWait(self.driver, 10)
        time.sleep(5)
        element = wait.until(EC.presence_of_element_located(
            (By.ID, "ReportViewer1_ToggleParam")))
        # exportando
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(15)
        self.driver.find_element(
            By.ID, "ReportViewer1_ctl06_ctl04_ctl00_ButtonImg").click()
        try:
            self.driver.find_element(
                By.LINK_TEXT, "Arquivo XML com dados de relatórios").click()
        except:
            time.sleep(3)
            self.driver.find_element(
                By.ID, "ReportViewer1_ctl06_ctl04_ctl00_ButtonImg").click()
            self.driver.find_element(
                By.LINK_TEXT, "Arquivo XML com dados de relatórios").click()

    def time(self):
        atual = datetime.datetime.now()
        formato = "%Y-%m-%d %H:%M:%S"
        return atual.strftime(formato)

    def run(self):
        logs = []
        self.driver.get(
            "https://www2.aneel.gov.br/relatoriosrig/(S(eafvzeo33i0t01uiu2ilaz2h))/relatorio.aspx?folder=sfe/Monitoramento/Transmissao&report=EmpreendimentoIndiv")
        self.driver.maximize_window()
        self.set_situacao()
        select, itens = self.itens_in_select()
        log = ["start", True, self.time()]
        print(log)
        logs.append(log)
        for option_number in range(1, itens + 1):
            try:
                print(option_number)
                selected = self.set_select_option(str(option_number))
                self.searching()
                self.exporting()
                log = [selected, True, self.time()]
                print(log)
                logs.append(log)
            except:
                log = [option_number, False, self.time()]
                print(log)
                logs.append(log)
        self.driver.quit()
        log = ["end", True, self.time()]
        print(log)
        logs.append(log)
        return logs


if __name__ == "__main__":
    extractor = ExtractData()
    logs = extractor.run()
    path = r""
    with open(path, "w") as file:
        json.dump(logs, file, indent=4)

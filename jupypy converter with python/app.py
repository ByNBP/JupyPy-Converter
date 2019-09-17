import sys
import os
import subprocess
import time
from selenium import webdriver
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

global filename, driver


class UserInterface(QDialog):
    def __init__(self):
        super(UserInterface, self).__init__()
        loadUi('userInterface.ui', self)
        self.setWindowTitle("Jupypy Converter")
        self.openJNButton.clicked.connect(self.openJupyter)
        self.saveCodeButton.clicked.connect(self.saveCode)
        self.exitButton.clicked.connect(self.exitApp)
        self.runCodeButton.clicked.connect(self.runCode)

    def runCode(self):
        RunSavedCode()

    def openJupyter(self):
        openJN()
        self.close()
        loginUI.show()

    def saveCode(self):
        GetCellValues()

    def exitApp(self):
        veri = os.popen("tasklist").read()
        if veri.find("chromedriver.exe") != -1:
            subprocess.Popen('taskkill /F /IM chromedriver.exe', stdout=subprocess.PIPE)
        if veri.find("jupyter.exe") != -1:
            subprocess.Popen('taskkill /F /IM jupyter.exe', stdout=subprocess.PIPE)
        if veri.find("jupyter-notebook.exe") != -1:
            subprocess.Popen('taskkill /F /IM jupyter-notebook.exe', stdout=subprocess.PIPE)
        if veri.find("jupyter-notebook.exe") != -1:
            subprocess.Popen('taskkill /F /IM chrome.exe', stdout=subprocess.PIPE)
        self.close()


class LoginInterface(QDialog):
    def __init__(self):
        super(LoginInterface, self).__init__()
        loadUi('loginUI.ui', self)
        self.setWindowTitle("Jupyter Notebook Login")
        self.loginButton.clicked.connect(self.login)

    def login(self):
        password = self.passwordText.toPlainText()
        print(password)
        LoginToJupyter(password)
        self.close()
        ui.show()


def openJN():
    global driver
    subprocess.Popen('jupyter notebook --no-browser', stdout=subprocess.PIPE)
    p = subprocess.Popen('jupyter notebook list', stdout=subprocess.PIPE)
    out, err = p.communicate()
    text = str(out)
    text = text.split("::")
    print(text)
    link = text[len(text) - 2]
    link = link[link.find("http://localhost:"):len(link)]
    print("yunus emre karakaya "+link)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(link)
    time.sleep(5)
    ui.infoText.setText("Info: Jupyter Notebook opened")


def LoginToJupyter(password):
    password_input = driver.find_element_by_id("password_input")
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(3)
    driver.find_element_by_id("login_submit").click()
    ui.infoText.setText("Info: Login Successful")


def GetCellValues():
    global filename, driver
    handlers = driver.window_handles
    driver.switch_to.window(handlers[1])
    title = driver.find_element_by_id("notebook_name").text
    cells = driver.find_elements_by_class_name("CodeMirror-lines")
    filename = title + ".py"
    file = open(filename, "w")
    code = ""
    for cell in cells:
        code += cell.text + "\n"
    file.write(code)
    file.close()
    ui.infoText.setText("Info: Code saved successfully")


def RunSavedCode():
    os.system("python " + filename)
    ui.infoText.setText("Info: Code Run Successfully")




app = QApplication(sys.argv)
ui = UserInterface()
ui.setWindowFlags(Qt.WindowCloseButtonHint)

loginUI = LoginInterface()
ui.show()

sys.exit(app.exec_())

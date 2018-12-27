import unittest
import xmlrunner
from selenium import webdriver
import PageObjects as PO
import names


class LoginTestCase(unittest.TestCase):

    # setUp se ejecuta antes de cada test method

    def setUp(self):
        self.driver = webdriver.Chrome('/Users/cizquierdo/PycharmProjects/POExample/chromedriver')

    def test_login(self):
        self.driver.get('http://192.168.64.2/')
        base_logout_po = PO.BaseLogoutPO(self.driver)
        login_po = base_logout_po.goto_login()
        login_po.login('user', 'bitnami1')
        base_login_po = PO.BaseLoginPO(self.driver)
        self.assertEqual('user', base_login_po.get_username())

    def test_create_new_project_without_modules(self):
        project_name = names.get_full_name()
        self.driver.get('http://192.168.64.2/')
        base_logout_po = PO.BaseLogoutPO(self.driver)
        login_po = base_logout_po.goto_login()
        login_po.login('user', 'bitnami1')
        base_login_po = PO.BaseLoginPO(self.driver)
        projects_po = base_login_po.goto_projects()
        new_project_po = projects_po.goto_new_project()
        new_project_po.create_new_project_without_modules(project_name)
        project_setting_po = PO.ProjectSettingsPO(self.driver)
        self.assertEqual('Successful creation.', project_setting_po.get_flash_notice_text())

    def tearDown(self):
        self.driver.close()

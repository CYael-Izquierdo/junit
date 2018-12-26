from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePO:

    driver = None
    wait = WebDriverWait(driver, 10, 0.5)

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver=driver, timeout=10, poll_frequency=0.5)

    def find_page_element(self, loc):
        return self.driver.find_element(loc[0], loc[1])

    def select_option_ddm(self, ddm_loc, option):
        ddm = self.find_page_element(ddm_loc)
        return ddm.find_element(By.LINK_TEXT, option)


class BaseLogoutPO(BasePO):

    btn_home_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[1]/a')
    btn_projects_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[2]/a')
    btn_help_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[3]/a')
    btn_login_tmenu_loc = (By.XPATH, '//*[@id="account"]/ul/li[1]/a')
    btn_register_tmenu_loc = (By.XPATH, '//*[@id="account"]/ul/li[2]/a')

    def goto_login(self):
        self.find_page_element(self.btn_login_tmenu_loc).click()
        return LoginPO(self.driver)


class BaseLoginPO(BasePO):

    btn_home_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[1]/a')
    btn_my_page_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[2]/a')
    btn_projects_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[3]/a')
    btn_administration_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[4]/a')
    btn_help_tmenu_loc = (By.XPATH, '//*[@id="top-menu"]/ul/li[5]/a')
    btn_username_tmenu_loc = (By.XPATH, '//*[@id="loggedas"]/a')
    btn_account_tmenu_loc = (By.XPATH, '//*[@id="account"]/ul/li[1]/a')
    btn_singout_tmenu_loc = (By.XPATH, '//*[@id="account"]/ul/li[2]/a')

    def goto_projects(self):
        self.find_page_element(self.btn_projects_tmenu_loc).click()
        return ProjectsPO(self.driver)

    def get_username(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_username_tmenu_loc))
        return self.find_page_element(self.btn_username_tmenu_loc).text


class LoginPO(BaseLogoutPO):

    btn_login_loc = (By.XPATH, '//*[@id="login-submit"]')
    txt_user_name_loc = (By.XPATH, '//*[@id="username"]')
    txt_user_password_loc = (By.XPATH, '//*[@id="password"]')

    flash_error_loc = (By.XPATH, '//*[@id="flash_error"]')

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def get_flash_error_text(self):
        self.wait.until(EC.visibility_of_element_located(self.flash_error_loc))
        return self.find_page_element(self.flash_error_loc).text

    def login(self, user, password):
        self.wait.until(EC.element_to_be_clickable(self.txt_user_name_loc))
        self.find_page_element(self.txt_user_name_loc).send_keys(user)
        self.find_page_element(self.txt_user_password_loc).send_keys(password)
        self.find_page_element(self.btn_login_loc).click()


class BaseProjectsPO(BaseLoginPO):

    btn_projects_mmenu_loc = (By.LINK_TEXT, 'Projects')
    btn_activity_mmenu_loc = (By.LINK_TEXT, 'Activity')
    btn_issues_mmenu_loc = (By.LINK_TEXT, 'Issues')
    btn_spent_time_mmenu_loc = (By.LINK_TEXT, 'Spent time')
    btn_gantt_mmenu_loc = (By.LINK_TEXT, 'Gantt')
    btn_calendar_mmenu_loc = (By.LINK_TEXT, 'Calendar')
    btn_news_mmenu_loc = (By.LINK_TEXT, 'News')


class ProjectsPO(BaseProjectsPO):

    chk_view_closed_projects_loc = (By.XPATH, '//*[@id="closed"]')
    btn_new_project_loc = (By.XPATH, '//*[@id="content"]/div[1]/a')

    projects_index_po = (By.XPATH, '//*[@id="projects-index"]')

    def find_project_by_name(self, project_name):
        projects = self.find_page_element(self.projects_index_po)
        return projects.find_element(By.LINK_TEXT, project_name)

    def goto_new_project(self):
        self.find_page_element(self.btn_new_project_loc).click()
        return NewProjectPO(self.driver)


class NewProjectPO(BaseProjectsPO):

    txt_project_name_loc = (By.XPATH, '//*[@id="project_name"]')
    txt_project_description_loc = (By.XPATH, '//*[@id="project_description"]')
    txt_project_id_loc = (By.XPATH, '//*[@id="project_identifier"]')
    txt_project_homepage_loc = (By.XPATH, '//*[@id="project_homepage"]')
    chk_project_is_public_loc = (By.XPATH, '//*[@id="project_is_public"]')
    ddm_subproject_of_loc = (By.XPATH, '//*[@id="project_parent_id"]')
    chk_inherit_members_loc = (By.XPATH, '//*[@id="project_inherit_members"]')
    modules_loc = (By.XPATH, '//*[@id="new_project"]/fieldset[1]')

    btn_create_loc = (By.XPATH, '//*[@id="new_project"]/input[3]')
    btn_create_and_continue_loc = (By.XPATH, '//*[@id="new_project"]/input[4]')

    def create_new_project_without_modules(self, name, id='', description='', home_page='', is_public=True):
        self.find_page_element(self.txt_project_name_loc).send_keys(name)
        if id:
            txt_id = self.find_page_element(self.txt_project_id_loc)
            txt_id.clear()
            txt_id.send_keys(id)
        self.find_page_element(self.txt_project_description_loc).send_keys(description)
        self.find_page_element(self.txt_project_homepage_loc).send_keys(home_page)
        chk_is_public = self.find_page_element(self.chk_project_is_public_loc)
        if not is_public and chk_is_public.is_selected():
            chk_is_public.click()
        modules = self.find_page_element(self.modules_loc)
        for module in modules.find_elements(By.TAG_NAME, 'input'):
            if module.is_selected():
                module.click()
        self.find_page_element(self.btn_create_loc).click()


class ProjectSettingsPO(BaseLoginPO):

    box_successful_creation_loc = (By.XPATH, '//*[@id="flash_notice"]')

    def get_flash_notice_text(self):
        self.wait.until(EC.visibility_of_element_located(self.box_successful_creation_loc))
        return self.find_page_element(self.box_successful_creation_loc).text

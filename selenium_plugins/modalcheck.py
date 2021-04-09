import re
from linkcheck import log, LOG_PLUGIN
from linkcheck.plugins import _ContentPlugin
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ModalCheck(_ContentPlugin):
    """Checks modal component."""

    PATTERN_TO_CHECK_MODAL_EXISTENCE = 'data-toggle="modal"'

    MODAL_SELECTOR = r'.btn[data-toggle="modal"]'
    OPENED_MODAL_SELECTOR = '.modal.show'
    CLOSE_BUTTON_MODAL_SELECTOR = 'button.close'

    ERROR_MSG = "ModalCheck: %s"
    ERROR_TAG = "plugin-error"

    WAIT = 1  # seconds

    def applies_to(self, url_data):
        """Check for HTML modal existence."""
        pattern = re.compile(self.PATTERN_TO_CHECK_MODAL_EXISTENCE)
        return url_data.is_html() and pattern.search(url_data.get_content())

    def check(self, url_data):
        """perform check. """
        log.debug(LOG_PLUGIN, "ModalCheck plugin")

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, self.WAIT)
        driver.get(url_data.url)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.MODAL_SELECTOR)))
        for e in elements:

            # open modal
            modal_target = e.get_attribute("data-target")
            e.click()

            # check modal opened
            modal = None
            try:
                opened_modal_selector = f'{modal_target}{self.OPENED_MODAL_SELECTOR}'
                modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, opened_modal_selector)))
            except TimeoutException:
                url_data.add_warning(self.ERROR_MSG % "can not open modal", tag=self.ERROR_TAG)

            # check modal closed
            try:
                modal.find_element_by_css_selector(self.CLOSE_BUTTON_MODAL_SELECTOR).click()
                wait.until(EC.invisibility_of_element(modal))
            except NoSuchElementException as ex:
                url_data.add_warning(self.ERROR_MSG % ex, tag=self.ERROR_TAG)
            except TimeoutException:
                url_data.add_warning(self.ERROR_MSG % "can not close modal", tag=self.ERROR_TAG)
        driver.close()

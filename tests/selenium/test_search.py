import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_search_product(self):
        driver = self.driver
        driver.get(f"{self.base_url}/shop/")

        # Sửa selector đúng với HTML thực tế
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "search-filter"))
        )
        search_box.send_keys("iphone")
        search_box.send_keys(Keys.ENTER)  # Hoặc click nút search nếu Enter không hoạt động

        time.sleep(1)
        # Kiểm tra sản phẩm mong đợi xuất hiện (ví dụ "iphone")
        self.assertIn("iphone", driver.page_source.lower())
        
        time.sleep(10)

if __name__ == "__main__":
    unittest.main()
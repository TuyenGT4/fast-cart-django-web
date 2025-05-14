import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://localhost:8000"
        cls.driver.get(f"{cls.base_url}/auth/sign-in/")
        cls.driver.find_element(By.NAME, "email").send_keys("tuyen1907004@gmail.com")
        cls.driver.find_element(By.NAME, "password").send_keys("Tuyen004.")
        cls.driver.find_element(By.XPATH, "//button[contains(text(),'Đăng nhập')]").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_checkout(self):
        driver = self.driver

        # Step 1: Thêm sản phẩm vào giỏ hàng
        add_cart_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.add_to_cart"))
        )
        add_cart_btn.click()
        time.sleep(1)

        # Step 2: Truy cập vào giỏ hàng
        driver.get(f"{self.base_url}/cart/")
    
        # Step 3: Chọn địa chỉ giao hàng và nhấn tiến hành thanh toán
        radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#address{{address.id}}.radio-custom"))
        )
        radio.click()
        
        # Nhấn nút Tiến hành thanh toán
        # driver.find_element(By.XPATH, "//button[contains(text(),'Tiến hành thanh toán')]").click()
        # time.sleep(2)

        # Step 4: Chọn thanh toán bằng COD
        # cod_radio = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @value='COD']"))
        # )
        # cod_radio.click()
        # driver.find_element(By.XPATH, "//button[contains(text(),'Đặt hàng')]").click()
        # time.sleep(2)
        # self.assertIn("đơn hàng", driver.page_source.lower())

if __name__ == "__main__":
    unittest.main()
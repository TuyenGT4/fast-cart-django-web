import unittest
import time
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
        self.driver.implicitly_wait(5)
        self.base_url = "http://localhost:8000"

    def tearDown(self):
        time.sleep(8)
        self.driver.quit()

    def test_register_valid(self):
        driver = self.driver
        driver.get(f"{self.base_url}/auth/sign-up/")

        # Tạo email duy nhất
        unique_email = f"testuser_{int(time.time())}@example.com"

        # Nhập thông tin hợp lệ
        driver.find_element(By.NAME, "full_name").send_keys("Test User 2")
        driver.find_element(By.NAME, "email").send_keys(unique_email)
        driver.find_element(By.NAME, "mobile").send_keys("0123456789")
        driver.find_element(By.NAME, "password1").send_keys("Abc123456.")
        driver.find_element(By.NAME, "password2").send_keys("Abc123456.")

        # Chọn user_type ("Khách hàng")
        user_type_select = Select(driver.find_element(By.NAME, "user_type"))
        user_type_select.select_by_visible_text("Khách hàng")

        # Click nút đăng ký
        driver.find_element(By.XPATH, "//button[contains(text(),'Đăng ký')]").click()

        # Chờ đến khi về trang chủ và thông báo xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Tài khoản của bạn đã được tạo thành công')]"))
        )
        # Kiểm tra cả nút Đăng xuất (đảm bảo đã đăng nhập)
        self.assertTrue(
            driver.find_element(By.XPATH, "//a[contains(text(),'Đăng xuất')]").is_displayed()
        )
        
    def test_login_valid(self):
        driver = self.driver
        driver.get(f"{self.base_url}/auth/sign-in/")

        # Nhập thông tin đăng nhập hợp lệ
        driver.find_element(By.NAME, "email").send_keys("tuyen1907004@gmail.com") 
        driver.find_element(By.NAME, "password").send_keys("Tuyen004.")              

        # Click nút đăng nhập
        driver.find_element(By.XPATH, "//button[contains(text(),'Đăng nhập')]").click()

        # Chờ đến khi thông báo đăng nhập thành công xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Bạn đã đăng nhập')]"))
        )
        # Kiểm tra nút Đăng xuất xuất hiện
        self.assertTrue(
            driver.find_element(By.XPATH, "//a[contains(text(),'Đăng xuất')]").is_displayed()
        )
    def test_logout(self):
        driver = self.driver
        driver.get(f"{self.base_url}/auth/sign-in/")

        # Đăng nhập trước
        driver.find_element(By.NAME, "email").send_keys("tuyen1907004@gmail.com") 
        driver.find_element(By.NAME, "password").send_keys("Tuyen004.")              
        driver.find_element(By.XPATH, "//button[contains(text(),'Đăng nhập')]").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Đăng xuất')]"))
        )

        # Nhấn nút Đăng xuất
        driver.find_element(By.XPATH, "//a[contains(text(),'Đăng xuất')]").click()

        # Chờ cho đến khi chuyển về trang đăng nhập hoặc có nút Đăng nhập xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Đăng nhập')]"))
        )
        # Đảm bảo không còn nút Đăng xuất trên trang
        self.assertEqual(
            len(driver.find_elements(By.XPATH, "//a[contains(text(),'Đăng xuất')]")), 0
        )
if __name__ == "__main__":
    unittest.main()
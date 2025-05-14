#Thêm, xóa, cập nhật số lượng giỏ hàng
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestCart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://localhost:8000"
        # Đăng nhập trước khi test giỏ hàng
        cls.driver.get(f"{cls.base_url}/auth/sign-in/")
        cls.driver.find_element(By.NAME, "email").send_keys("tuyen1907004@gmail.com")
        cls.driver.find_element(By.NAME, "password").send_keys("Tuyen004.")
        cls.driver.find_element(By.XPATH, "//button[contains(text(),'Đăng nhập')]").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)  # Đợi 5 giây trước khi đóng trình duyệt
        cls.driver.quit()

    def test_add_to_cart(self):
        driver = self.driver
        driver.get(f"{self.base_url}/")
        add_cart_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.add_to_cart"))
        )
        add_cart_btn.click()
        time.sleep(1)
        driver.get(f"{self.base_url}/cart/")
        self.assertIn("giỏ hàng", driver.page_source.lower())

    def test_update_quantity(self):
        driver = self.driver
        driver.get(f"{self.base_url}/")

        # 1. Vào giao diện giỏ hàng bằng cách click icon giỏ hàng trên header
        driver.get(f"{self.base_url}/cart/")
        time.sleep(1)  # Đợi giao diện giỏ hàng load

        # 2. Kiểm tra giỏ hàng có trống không
        cart_empty = False
        try:
            # Có thể điều chỉnh lại XPATH nếu thông báo khác
            empty_alert = driver.find_element(By.XPATH, "//*[contains(text(), 'giỏ hàng') and contains(text(), 'trống')]")
            cart_empty = True
        except:
            # Không tìm thấy thông báo, kiểm tra tiếp có sản phẩm không
            items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
            if len(items) == 0:
                cart_empty = True

        if cart_empty:
            # Giỏ hàng trống: thêm sản phẩm
            driver.get(f"{self.base_url}/")
            add_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add_to_cart"))
            )
            add_cart_btn.click()
            time.sleep(1)
            # Vào lại giao diện giỏ hàng
            driver.get(f"{self.base_url}/cart/")
            time.sleep(1)

        # 3. Đảm bảo đã có sản phẩm trong giỏ
        # Tìm nút tăng số lượng (giả sử có class .cart-plus hoặc nút cộng)
        plus_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'cart-plus') or normalize-space(text()) = '+']"
            ))
        )
        plus_btn.click()
        time.sleep(1)
        # Chờ thông báo cập nhật thành công
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Cập nhật giỏ hàng thành công')]"))
        )

        # 4. Giảm số lượng (nếu muốn test luôn nút giảm)
        minus_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'cart-minus') or normalize-space(text()) = '-']"
            ))
        )
        minus_btn.click()
        time.sleep(1)
        # Chờ thông báo cập nhật thành công lần nữa
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Cập nhật giỏ hàng thành công')]"))
        )

        # Để bạn thấy kết quả
        time.sleep(5)

    def test_remove_from_cart(self):
        driver = self.driver
        driver.get(f"{self.base_url}/cart/")
        time.sleep(1)

        # Nếu giỏ hàng trống thì thêm sản phẩm trước
        cart_empty = False
        try:
            empty_alert = driver.find_element(By.XPATH, "//*[contains(text(), 'giỏ hàng') and contains(text(), 'trống')]")
            cart_empty = True
        except:
            items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
            if len(items) == 0:
                cart_empty = True

        if cart_empty:
            driver.get(f"{self.base_url}/")
            add_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add_to_cart"))
            )
            add_cart_btn.click()
            time.sleep(1)
            driver.get(f"{self.base_url}/cart/")
            time.sleep(1)

        # 1. Tìm và click nút xóa sản phẩm
        remove_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.delete_cart_item"))
        )
        remove_btn.click()

        # 2. Chờ thông báo "Đã xóa sản phẩm khỏi giỏ hàng"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Đã xóa sản phẩm khỏi giỏ hàng')]"))
        )
    
if __name__ == "__main__":
    unittest.main()
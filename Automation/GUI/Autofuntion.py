import time
import logging
from venv import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
# from logs import configure_log
# from logs import modify_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

from datetime import datetime
import shutil
import os

class Autofuntion():

    def __init__(self) -> None:
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        self.CSS_ADD_TO_CART = '[id="add-to-cart"]'
        self.XPATH_SHOP_ALL = '//a[@_ngcontent-ng-c1066574655]' #//.text = SHOP ALL   // #ĐĂNG NHẬP // TÀI KHOẢN
        self.XPATH_HADES_STRIPED_SOLID_SHIRT = '//h5[@class="card-title text-center mb-1"]'  # " HADES STRIPED SOLID SHIRT "
        self.CSS_THEM_GIO_HANG = '[id="add-to-cart"]'
        self.XPATH_CART = '//a[@_ngcontent-ng-c1066574655]' # 'GIỎ HÀNG'
        self.XPATH_XEM_GIO_HANG = '//button[@_ngcontent-ng-c2716542086]' # "XEM GIỎ HÀNG"
        # Thanh toán trong gio hang
        self.XPATH_THANH_TOAN = "//button[@_ngcontent-ng-c2772077179]" # "THANH TOÁN"
        self.XPATH_INPUT_HO_VA_TEN = '//input[@placeholder="Họ và tên"]'
        self.XPATH_INPUT_EMAIL = '//input[@placeholder="Email"]'
        self.XPATH_INPUT_SO_DIEN_THOAI = '//input[@placeholder="Số điện thoại"]'
        self.XPATH_DIA_CHI = '//input[@placeholder="Địa chỉ"]'
        self.XPATH_TINH_THANH_PHO = '//select[@formcontrolname="province"]'
        self.XPATH_OPTION_TINH_THANH_PHO = '//option[@class="ng-star-inserted"]' # .text = "An Giang"/ "Bắc Giang" / "Bắc Ninh"
        self.CSS_QUAN_HUYEN = 'id="district"'
        self.CSS_PHUONG_XA = '[id="ward"]'
        self.CSS_SHIP = 'id="shipping"'
        self.XPATH_PTVC_PTTT = '//label[@class="form-check-label"]'
        # " Giao hàng tận nơi ", " Thanh toán khi giao hàng (COD) ", " Thanh toán bằng VNPay ", " Thanh toán bằng PayPal "
        self.HOAN_TAT_DON_HANG = '//button[@class="btn btn-success ng-star-inserted"]'
        # atribute = disabled -> ko thanh toán đc | không có là thanh toán đc
        #-> "TÀI KHOẢN"
        # self.XPATH_       
        self.CSS_HO_VA_TEN = '[placeholder="Họ và tên"]'
        self.CSS_EMAIL = '[placeholder="Email"]'
        self.CSS_SO_DIEN_THOAI = '[placeholder="Số điện thoại"]'
        self.CSS_DIA_CHI = '[placeholder="Địa chỉ"]'
        self.CSS_TINH_THANH_PHO = '[id="province"]'
        self.XPATH_OPTIONS_TINH_THANH_PHO = '//option[@class="ng-star-inserted"]' #"Bắc Giang" / quận: Châu Đức / xã: Bình Ba
        self.CSS_QUAN_HUYEN = '[id="district"]'
        self.CSS_PHUONG_XA = '[id="ward"]'
        self.XPATH_HOAN_TAT_DON_HANG = '//button[@class="btn btn-success ng-star-inserted"]'

        # ---------------- login -----
        self.CSS_EMAIL_LOGIN = '[name="email"]'
        self.CSS_PASSWORD = '[name="password"]'
        self.XPATH_SUBMIT_LOGIN = '//button [@type="submit"]'
        # --- verify sp trong gio hang
        self.XPATH_PRODUCTS_IN_SHOPPING_CART = '//h6[@_ngcontent-ng-c3804567032]' #HADES STRIPED SOLID SHIRT tên sản phẩm
        self.XPATH_TEXT_GIO_HANG = "//h4[@_ngcontent-ng-c2716542086]" #.text GIỎ HÀNG
        # ----- giỏ hàng của tôi
        self.XPATH_MY_CART = '//h6[@_ngcontent-ng-c1369544179]'


        # --- element verify giá tiền, tổng tiền, thành tiền trong giỏ hàng của tôi
        self.NAME_PRODUCT_IN_MY_CART = "//h6[text()='{}']" #  .text = name product expected //h6[text()='HADES STRIPED SOLID SHIRT']
        # self.MESSAGE_ITEM_TXT.format(text_value)
        self.PRICE_OF_PRODUCT = "//div[@class= 'col-2 text-center align-self-center']/p[@_ngcontent-ng-c1369544179]"
        self.THANH_TIEN = '//p[@_ngcontent-ng-c1369544179][2]'
        self.TONG_TIEN = "//h6[@class='me=0']" #. text = tong tien phai tra

        self.INPUT_QUANTITY = "//input[@aria-valuenow]" #//h6[text()='HADES STRIPED SOLID SHIRT']/../..//input[@aria-valuenow]


        #  ------- element verify trong tab tài khoản
        #//tr[@_ngcontent-ng-c577092477][1]//td[@_ngcontent-ng-c577092477][2] -> đoen hàng vị trí đầu tiên, với thời gian #[3] -> người nhận; sdt -> địa chỉ -> tổng tiền
        self.ORDER_FIRST = "//tr[@_ngcontent-ng-c577092477][1]"
        self.DATE_CREATE = "//td[@_ngcontent-ng-c577092477][2]"
        self.USER_CREATE = "//td[@_ngcontent-ng-c577092477][3]"
        self.NUMBER_PHONE_CREATE = "//td[@_ngcontent-ng-c577092477][4]"
        self.ADRESS_CREATE = "//td[@_ngcontent-ng-c577092477][5]"
        self.TOTAL_AMOUNT_CREATE = "//td[@_ngcontent-ng-c577092477][6]"


    def launch_browser(self, url):
        self.driver.get(url)
        # Mở toàn màn hình
        self.driver.maximize_window()
        self.clear_cache()
        logger.info("Khoi dong tring duyet va clear cache oki") 

    def close_browser(self):
        self.driver.quit()

    def choose_products(self, name_product,timeout= 10):
        try:
            logger.info('Start function choose_products')
            for attempt in range(3):
                logger.info(f"range: {attempt}")
                product_elements = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_HADES_STRIPED_SOLID_SHIRT))
                )

                for element in product_elements:
                    if element.text.strip() == name_product.strip():
                        logger.info(f'Product matches: {element.text}')
                        # Scroll to the element
                        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
                        logger.info(f'Product matches: execute_script')
                        time.sleep(5)
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(5)
                        return True  # Exit function if the product is found and clicked
                    # break
        
        except Exception as e:
            logger.error(f"Error choose products: {e}. Please check again")
            return False
        
    def add_to_cart (self, timeout=10):
        try:
            logger.info('Start function add_to_cart')
            time.sleep(timeout)

            for attempt in range(3):
                try:
                    add_to_cart_button = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.CSS_THEM_GIO_HANG))
                    )
                    self.driver.execute_script("arguments[0].click();", add_to_cart_button)
                    logger.info("Clicked 'Add to Cart' button successfully.")
                    break  # Thoát vòng lặp sau khi click thành công
                except StaleElementReferenceException:
                    logger.warning("Stale element reference: Retrying to click 'Add to Cart' button.")
                except TimeoutException:
                    logger.error("Timeout: 'Add to Cart' button not clickable.")
                    return False
        except Exception as e:
            logger.info("Error add_to_cart: {e}. Please check again")
            return False
        
    def visit_the_cart (self, timeout=10):
        try:
            logger.info('Start function visit_the_cart')
            time.sleep(timeout)
            # Tìm phần tử với XPATH_TEXT_GIO_HANG
            gio_hang_element = self.driver.find_element(By.XPATH, "//h4[@_ngcontent-ng-c2716542086]")
            print("Đã tìm thấy phần tử với text GIỎ HÀNG")

            if not gio_hang_element:

                logger.info("Tiếp tục với các bước xử lý sau khi thêm vào giỏ hàng")
                cart_button = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_CART))
                )
                for xpath_cart in cart_button:
                    if xpath_cart.text == 'GIỎ HÀNG':
                        # Click vào "GIỎ HÀNG"
                        self.driver.execute_script("arguments[0].click();", xpath_cart)
                        logger.info("click xpath_cart oki")
                    
            # Mở trang xem giỏ hàng
            logger.info("Mở trang xem giỏ hàng")
            btn_xem_gio_hang = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_XEM_GIO_HANG))
            )
            for xpath_xem_gio_hang in btn_xem_gio_hang:
                if xpath_xem_gio_hang.text == "XEM GIỎ HÀNG":
                    xpath_xem_gio_hang.click()
                    logger.info("click xpaXEM GIỎ HÀNG oki")
                    break
            
        except Exception as e:
            logger.info("Error visit_the_cart: {e}. Please check again")
            return False
        
    def verify_prices_product_in_my_cart (self, name_product, quantity, timeout=10):
        try:
            # kiểm tra xem sản phẩm có nằm trong Giỏ hàng của bạn chưa
            logger.info('Start function verify_prices_product_in_my_cart')
            time.sleep(timeout)
            print(self.NAME_PRODUCT_IN_MY_CART.format(name_product))
            logger.info(f'name_product_in_my_cart: {self.NAME_PRODUCT_IN_MY_CART.format(name_product)}')

            name_product_in_my_cart = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.NAME_PRODUCT_IN_MY_CART.format(name_product))))
            # In ra dòng XPATH đã được định dạng
            print(self.NAME_PRODUCT_IN_MY_CART.format(name_product))

            logger.info(f'name_product_in_my_cart: {name_product_in_my_cart}')
            # logger.info(f'name_product_in_my_cart: {name_product_in_my_cart.text}')

            logger.info(f'price_product product 123: {self.NAME_PRODUCT_IN_MY_CART.format(name_product) + "/../.."  + self.PRICE_OF_PRODUCT}')

            # price_product = name_product_in_my_cart.find_element(By.XPATH, "/../.." + self.PRICE_OF_PRODUCT).text
            price_product = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, f"{self.NAME_PRODUCT_IN_MY_CART.format(name_product)}/../..{self.PRICE_OF_PRODUCT}"))).text

            # Chuyển đổi chuỗi '432000đ' thành số nguyên
            price_product = int(price_product.replace("đ", "").replace(",", "").strip())
            
            logger.info(f'price_product product {name_product_in_my_cart} is : {price_product} and type is {type(price_product)}')

            logger.info(f'quantity_product 123: {self.NAME_PRODUCT_IN_MY_CART.format(name_product) + "/../.."  + self.INPUT_QUANTITY}')
            quantity_product = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, f"{self.NAME_PRODUCT_IN_MY_CART.format(name_product)}/../..{self.INPUT_QUANTITY}")))
            
            # quantity_product = name_product_in_my_cart.find_element(By.XPATH, "/../.." + self.INPUT_QUANTITY)
            quantity_product.clear()
            number_quantity = quantity_product.send_keys(quantity) #2
            logger.info(f"type number quantity: {type(number_quantity)}")
            
            logger.info(f'number_quantity product {name_product_in_my_cart} is : {number_quantity} and type is {type(number_quantity)}')

            # Tìm phần tử cha chứa giá tiền từ `name_product_in_my_cart`
            logger.info(f'TONG_TIEN 123: {self.TONG_TIEN}')
            total_amount = name_product_in_my_cart.find_element(By.XPATH, self.TONG_TIEN).text

            total_amount = int(total_amount.replace("đ", "").replace(",", "").strip())
            
            type_total_amount = type(total_amount)
            logger.info(f"type_total_amount is {type_total_amount}")
            

            #Xem thử số lượng nhân giá tiền có = tổng ko
            logger.info(f"int(price_product): {price_product} * int(number_quantity): {int(quantity)} == int(total_amount) {total_amount} is: {price_product * int(quantity)}")

            if (int(price_product) * int(quantity) == int(total_amount)):
                logger.info("Total amount is {total_amount} = prices * quantity")
                logger.info("verify_prices_product_in_my_cart successfully")
                return True

            logger.error(f"Total amount {total_amount} is NOT equal with prices * quantity {price_product * int(quantity)}")
            logger.error("verify_prices_product_in_my_cart failed")
            return False
                    
        except Exception as e:
            logger.info(f"Error verify_prices_product_in_my_cart: {e}. Please check again")
            return False
        
    def verify_name_product_in_my_cart (self, name_product, timeout=10):
        try:
            # kiểm tra xem sản phẩm có nằm trong Giỏ hàng của bạn chưa
            logger.info('Start function verify_name_product_in_my_cart')
            time.sleep(timeout)
            # Tìm phần tử với XPATH_TEXT_GIO_HANG
            # time.sleep(3)
            gio_hang_cua_ban_element = self.driver.find_elements(By.XPATH, self.XPATH_MY_CART)
            
            logger.info("Đã tìm thấy sản phẩm cần tìm trong Giỏ hàng của bạn")

            for xpath_cart in gio_hang_cua_ban_element:
                if xpath_cart.text == name_product:
                    logger.info(f"Product {xpath_cart.text} exits in my cart")
                    return True
            # Verify giá tiền
            logger.error(f"Can not find product {xpath_cart.text} in my cart")
            return False
                    
        except Exception as e:
            logger.info(f"Error verify_name_product_in_my_cart: {e}. Please check again")
            return False

    def checkout (self, timeout=10):
        try:
            logger.info('Start function checkout')
            time.sleep(timeout)
            btn_thanh_toan = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.XPATH_THANH_TOAN))
            )
            if btn_thanh_toan.text == "THANH TOÁN":
                logger.info(f"btn thanh toán :  {btn_thanh_toan.text}")
                logger.info("start clcik button Thanh toán")
                # btn_thanh_toan.click()
                logger.info('Clicked = JS')
                self.driver.execute_script("arguments[0].click();", btn_thanh_toan)
                logger.info('Clicked on the checkout button')
                # time.sleep(15)
                return True          
        except Exception as e:
            logger.info("Error checkout: {e}. Please check again")
            return False
        
    def add_products_to_cart(self, name_product, quantity, timeout=10):
        try:
            logger.info('Start function add_products_to_cart')
            shop_all_elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_SHOP_ALL))
            )
            
            for element in shop_all_elements:
                if element.text == "SHOP ALL":
                    logger.info('Found element with text: SHOP ALL, clicking...')
                    element.click()
                    logger.info('Clicked on SHOP ALL')
                    break  # Thoát vòng lặp sau khi click

            # Tìm sản phẩm theo tên
            self.choose_products(name_product, timeout)
            self.add_to_cart (timeout)   
            self.verify_products_in_shopping_cart(name_product, timeout)
            self.visit_the_cart (timeout)
            self.verify_name_product_in_my_cart (name_product, timeout)
            self.verify_prices_product_in_my_cart (name_product, quantity, timeout)
            self.checkout (timeout)     


        except Exception as e:
            logger.error(f'Error in add_products_to_cart: {e}')
            return False
        
    def verify_products_in_shopping_cart(self, name_product, timeout=10):
        try:
            logger.info('Start function verify_products_in_shopping_cart')
            time.sleep(timeout)
            # Tìm phần tử với XPATH_TEXT_GIO_HANG
            try:
                gio_hang_element = self.driver.find_element(By.XPATH, "//h4[@_ngcontent-ng-c2716542086]")
                print("Đã tìm thấy phần tử với text GIỎ HÀNG")
            except NoSuchElementException:
                logger.info("Không tìm thấy phần tử với text GIỎ HÀNG, sẽ click vào GIỎ HÀNG qua XPATH_CART")
                try:
                    logger.info("Tiếp tục với các bước xử lý sau khi thêm vào giỏ hàng")
                    cart_button = WebDriverWait(self.driver, timeout).until(
                        EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_CART))
                    )
                    for xpath_cart in cart_button:
                        if xpath_cart.text == 'GIỎ HÀNG':
                            # Click vào "GIỎ HÀNG"
                            self.driver.execute_script("arguments[0].click();", xpath_cart)
                            logger.info("click xpath_cart oki")
                            break

                except TimeoutException:
                    logger.error("Không tìm thấy phần tử GIỎ HÀNG để click vào sau khi chờ đợi.")


            logger.info('Verify name product in shopping cart')
            shop_all_elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_PRODUCTS_IN_SHOPPING_CART))
            )
            logger.info(f'name_product 123 : {name_product}')
           
            
            for element in shop_all_elements:
                logger.info(f'shop_all_elements 123 : {element.text}')
                if element.text == name_product:
                    logger.info(f'Found element with text: {name_product}')
                    logger.info('Function verify_products_in_shopping_cart successfully')
                    return True
                
            logger.info(f"No found any products with name {name_product}")
            return False  

        except Exception as e:
            logger.error(f'Error in add_products_to_cart: {e}')
            return False
        
    def check_option_province_ward_city (self, tinh_thanh, quan_huyen, phuong_xa, timeout = 10):
        try:
            logger.info("Start filling check_option_province_ward_city")  
            # Select "Tỉnh/Thành phố"
            tinh_thanh_field = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.CSS_TINH_THANH_PHO))
            )
            tinh_thanh_field.click()
            # time.sleep(5)
            options_tinh_thanh = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_OPTIONS_TINH_THANH_PHO))
            )
            logger.info("Start choose province")
            for option in options_tinh_thanh:
                logger.info("Clicked options_tinh_thanh")
                logger.info(f"options_tinh_thanh: '{option.text}' ")
                logger.info(f"tinh_thanh: '{tinh_thanh}' ")
                # time.sleep(5)
                if option.text == tinh_thanh:
                    option.click()  
                    break

            # Select "Quận/Huyện"
            # time.sleep(3)
            quan_huyen_field = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.CSS_QUAN_HUYEN))
            )

            quan_huyen_field.click()
            logger.info("Clicked quan_huyen")
            # time.sleep(3)

            # Select "Châu Đốc" in Quận huyện (District) dropdown
            district_select = self.driver.find_element(By.CSS_SELECTOR, self.CSS_QUAN_HUYEN)
            district_options = district_select.find_elements(By.TAG_NAME, 'option')
            logger.info("Start choose district")
            # time.sleep(5)
            for option in district_options:  # Reuse options if needed
                logger.info(f"options_quanhuyen: '{option.text}' ")
                logger.info(f"quan huyen: '{quan_huyen}' ")
                if option.text.strip() == quan_huyen:
                    # time.sleep(5)
                    option.click()
                    break

            # Select "Phường/Xã"
            phuong_xa_field = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.CSS_PHUONG_XA))
            )
            phuong_xa_field.click()
            logger.info("Clicked phuong_xa_field")
            # time.sleep(3)

            # Select "Châu Phú A" in Phường xã (Ward) dropdown
            ward_select = self.driver.find_element(By.CSS_SELECTOR, '[id="ward"]')
            ward_options = ward_select.find_elements(By.TAG_NAME, 'option')
            logger.info("Start choose ward")
            time.sleep(3)
            for option in ward_options:  # Reuse options if needed
                logger.info(f"options_phuong xa: '{option.text}' ")
                logger.info(f"phuong xa: '{phuong_xa}' ")
                if option.text.strip() == phuong_xa:
                    time.sleep(3)
                    # option.click()
                    # self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", option)
                    # self.driver.execute_script("arguments[0].click();", option)
                    time.sleep(3)
                    option.click()
                    logger.info(f"click phuong xa ok")
                    # break
                    return True
        
        except Exception as e:
            logger.error(f'Error in check_option_province_ward_city: {e}')
            return False

    def confirm_order (self, timeout = 10):
        try:
            logger.info("Start filling confirm_order")  
            time.sleep(3)
            hoan_tat_don_hang_button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_HOAN_TAT_DON_HANG))
            )
            logger.info("start Clicked 'Hoàn tất đơn hàng' button")
            time.sleep(3)
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", hoan_tat_don_hang_button)
            self.driver.execute_script("arguments[0].click();", hoan_tat_don_hang_button)
            logger.info("Clicked 'Hoàn tất đơn hàng' button successfully")
           
            return True
        
        except Exception as e:
            logger.error(f'Error in confirm_order: {e}')
            return False

        
    def fill_checkout_form(self, ho_va_ten, email, so_dien_thoai, dia_chi, tinh_thanh, quan_huyen, phuong_xa, timeout=10):
        try:
            logger.info("Start filling checkout form")
            time.sleep(5)
            
            # Input "Họ và tên"
            ho_va_ten_field = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.CSS_HO_VA_TEN))
            )
            ho_va_ten_field.clear()
            ho_va_ten_field.send_keys(ho_va_ten)

            # Input "Email"
            email_field = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.CSS_EMAIL))
            )
            email_field.clear()
            email_field.send_keys(email)

            # Input "Số điện thoại"
            so_dien_thoai_field = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.CSS_SO_DIEN_THOAI))
            )
            so_dien_thoai_field.clear()
            so_dien_thoai_field.send_keys(so_dien_thoai)

            # Input "Địa chỉ"
            dia_chi_field = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.CSS_DIA_CHI))
            )
            dia_chi_field.clear()
            dia_chi_field.send_keys(dia_chi)
            self.check_option_province_ward_city (tinh_thanh, quan_huyen, phuong_xa, timeout)
            time.sleep(5)

            # Click "Hoàn tất đơn hàng"
            self.confirm_order()
            time.sleep(5)
            logger.info(f"Function fill_checkout_form successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error filling checkout form: {e}")
            return False

        
    def login (self, username, password, timeout = 10):
        try:
            logger.info("Start funtion login")
            
            # Input "email"
            email = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.CSS_EMAIL_LOGIN))
            )
            email.clear()
            email.send_keys(username)

            pwd = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.CSS_PASSWORD))
            )
            pwd.clear()
            pwd.send_keys(password)

            btn_login = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.XPATH_SUBMIT_LOGIN))
            )
            time.sleep(5)
            btn_login.click()
            logger.info("click();, btn_login")

            self.verify_login(timeout)

            time.sleep(5)
            logger.info("Function login successfully")
            return True

        except Exception as e:
            logger.error(f"Error login page: {e}")
            return False

    def clear_cache(self):
        # Xóa cache qua DevTools Protocol
        self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        self.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})

    def verify_login (self, timeout = 10):
        try:
            logger.info("Verify login thanh công hay chưa")
            shop_all_elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_SHOP_ALL))
            )
            for element in shop_all_elements:
                if element.text == "ĐĂNG NHẬP":
                    logger.info('Login Unsuccessfully, please check again')
                    return False
            return True
        
        except Exception as e:
            logger.error(f"verify_login failed: {e}, please check again")
            return False
        # ============== verify đơn hàng của tài khoản

    def verify_order_in_my_account (self, ho_va_ten, so_dien_thoai, dia_chi, phuong_xa, quan_huyen, tinh_thanh, price, timeout=10):

        try:
            logger.info("Verify verify_order_in_my_account")
            time.sleep(timeout)
            shop_all_elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, self.XPATH_SHOP_ALL))
            )
            time.sleep(5)
            for element in shop_all_elements:
                if element.text == "TÀI KHOẢN":
                    element.click()
                    time.sleep(5)
                    # logger.info('Login Unsuccessfully, please check again')
                    curent_date = datetime.now().date()
                    logger.info(f'Curent date is : {curent_date}')
                    
                    date_in_order = self.driver.find_element(By.XPATH, self.DATE_CREATE).text
                    self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", self.driver.find_element(By.XPATH, self.DATE_CREATE))
                    # kết quả = '02-11-2024 22:41 PM': chỉ láy ngày tháng năm: 
                    date_only = date_in_order.split()[0]
                    logger.info(f'date_in_order is : {date_in_order}, date_only: {date_only}')
                    curent_date = datetime.now().strftime('%d-%m-%Y')
                    logger.info(f'Curent date 2 is : {curent_date} type: {type(curent_date)}')

                    user_in_order = self.driver.find_element(By.XPATH, self.USER_CREATE).text
                    logger.info(f'user_in_order is : "{user_in_order}" type {type(user_in_order)}')
                    
                    phone_number_in_order = self.driver.find_element(By.XPATH, self.NUMBER_PHONE_CREATE).text
                    logger.info(f'phone_number_in_order is : "{phone_number_in_order}" type {phone_number_in_order}')
                    
                    address_create_in_order = self.driver.find_element(By.XPATH, self.ADRESS_CREATE).text
                    logger.info(f'address_create_in_order is : "{address_create_in_order}" type {address_create_in_order}')

                    total_amount_in_order = self.driver.find_element(By.XPATH, self.TOTAL_AMOUNT_CREATE).text
                    logger.info(f'total_amount_in_order is : "{total_amount_in_order}" type {total_amount_in_order} ')

                    full_address = ", ".join([
                                            dia_chi, 
                                            f"Phường {phuong_xa}", 
                                            f"Thành phố {quan_huyen}", 
                                            f"Tỉnh {tinh_thanh}"
])

                    logger.info(f'full_address is : "{full_address}" ')
                                    # So sánh thông tin
                    logger.info(f'Start verify information in My account')            

                    logger.info(f'Check date_only "{date_only}" and {type(date_only)} ')
                    logger.info(f'Check total_amount_in_order "{total_amount_in_order}" and {type(total_amount_in_order)} ')
                    logger.info(f'Check price "{price}" and {type(price)} ')

                    if (date_only == curent_date and 
                        user_in_order == ho_va_ten and 
                        phone_number_in_order == so_dien_thoai and 
                        address_create_in_order == full_address and 
                        int(total_amount_in_order) == int(price)):    
                            time.sleep(5)
                            logger.info(f'Matched information, verify_order_in_my_account successfully ')
                            return True
                    
                    logger.error(f'NOT matched information, verify_order_in_my_account Unsuccessfully ')
                    return False
        
        except Exception as e:
            logger.error(f"verify_order_in_my_account failed: {e}, please check again")
            return False
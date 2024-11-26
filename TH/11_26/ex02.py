from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import datetime
import os
import time
import pandas as pd

class FacebookGroupScraper:
    def __init__(self):
        print("----Facebook group member------")
        
        self.get_config()
        self.setup_driver()
        
    def get_config(self):
        try:
            # Infor Đăng nhập
            print("Nhap thong tin đăng nhập")
            self.email = input("Email/Username: ").strip()
            self.password = getpass.getpass("Password: ")
            
            # ID Group
            print("\n Nhap ID thong tin Group Fb: ")
            self.group_id =input( "Group id: ").strip()
            
            # So lan Scroll
            print("\n So Lan Scroll de Load them thanh vien: ")
            self.scroll_count = int(input(" So lan Scroll (mac dinh 5) ") or "5")
                       
        except Exception as e:
            print(f" Lỗi cấu hình {e}")
            pass
        
    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        
        except Exception as e:
            print( f" Lỗi khởi tạo trình duyệt {e}")
            pass
       
    def login(self):
        try:
            self.driver.get("https://www.facebook.com")
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.send_keys(self.email)
            
            # Nhập password
            pass_input = self.driver.find_element(By.ID, "pass")
            pass_input.send_keys(self.password)
            
            # Click đăng nhập
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            
            # Chờ trang chuyển đổi sau khi đăng nhập
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("facebook.com")
            )
            print("Đăng nhập thành công")
            return True
            
        except Exception as e:
            print(f" Lỗi Đăng Nhập {e}")
            return False
    
    # Lấy từng thành viên group FB
    def get_group_member(self):
        
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(5)

            members = set()

            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                print(f"Scroll no.{i+1}/{self.scroll_count}")

                user_elements = self.driver.find_elements(By.CSS_SELECTOR,"a[href+='/user/']")
    
            for user in user_elements:
                    try:
                        href = user.get_attribute('href')
                        if '/user/' in href:
                            user_id = href.split("/user")[1].strip('/')
                            name = user.text
                            members.add((user_id, name))
                            print(user_id, " - ", name)
                        
                    except Exception:
                        continue

            return list(members)

        except Exception as e:
            print( f" Lỗi thu thập thành viên: {e}")
            return None
        
    def save_members_to_csv(self, members, file_name="group_members.csv"):
        """
        Lưu danh sách thành viên vào file CSV bằng pandas.

        Parameters:
        - members (list): Danh sách các tuple (user_id, name).
        - file_name (str): Tên file CSV để lưu dữ liệu.
        """
        try:
            # Chuyển danh sách thành viên thành DataFrame
            df = pd.DataFrame(members, columns=["user_id", "name"])
            # Lưu DataFrame vào file CSV
            df.to_csv(file_name, index=False, encoding="utf-8")
            print(f"Dữ liệu đã được lưu vào file: {file_name}")
            return df

        except Exception as e:
            print(f"Lỗi khi lưu file CSV: {e}")
            return None

def main():
    scrapper = None 
    try:
        # Khởi tạo scraper
        scrapper = FacebookGroupScraper()
        
        # Đăng nhập
        if scrapper.login():
            # Thêm thời gian chờ sau khi đăng nhập thành công
            time.sleep(20)  # Tăng thời gian chờ tại đây nếu cần
            
            print("-----------------------")
            
            # Lấy danh sách thành viên
            members = scrapper.get_group_member()
            
            # Lưu danh sách thành viên vào file CSV
            if members:
                scrapper.save_members_to_csv(members)
            
            # Thời gian chờ trước khi kết thúc
            time.sleep(20)  # Tăng thêm thời gian chờ trước khi đóng trình duyệt
        else:
            print("Đăng nhập thất bại!")
            
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi: {e}")
    finally:
        if scrapper and scrapper.driver:
            scrapper.driver.quit()  # Đảm bảo trình duyệt được đóng


    
if __name__ == "__main__" :
    main()
import requests,json,time,random,sys,re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



def get_mail():
    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    pos = json.loads(requests.post(url).text)
    return(pos['email'])

def generate_username():
    indonesian_names = ["budi", "siti", "agus", "nur", "fitri", "joko", "rini", "adi", "dewi", "agus", "eka", "ari", "rina", "andi", "novi"]
    russian_names = ["ivan", "olga", "dmitri", "tatiana", "alexei", "natalia", "sergei", "marina", "nikolai", "irina", "vladimir", "anastasia", "pavel", "yelena", "maxim"]
    chinese_names = ["jing", "wei", "li", "xin", "ming", "jun", "fang", "hui", "yi", "ning", "qing", "hua", "guo", "jia", "lin"]
    indonesian_name = random.choice(indonesian_names)
    russian_name = random.choice(russian_names)
    chinese_name = random.choice(chinese_names)
    username = f"{indonesian_name}{russian_name}{chinese_name}{random.randint(1000, 9999)}"
    return username

def check_duplicate(username, email, password):
    try:
        with open('users.json', 'r') as f:
            users_data = f.readlines()
    except FileNotFoundError:
        return False
    for line in users_data:
        try:
            user_info = json.loads(line)
        except json.decoder.JSONDecodeError:
            users_data=[]
            return False
        if user_info['username'] == username and user_info['email'] == email and user_info['password'] == password:
            return True
    return False

def save_info(username, email, password):
    user_info = {'username': username, 'email': email, 'password': password}
    if not check_duplicate(username, email, password):
        with open('users.json', 'a') as f:
            f.write(json.dumps(user_info) + '\n')
    else:
        print("Data pengguna sudah ada.")

def wait(duration):
    chars = "/—\|"
    for _ in range(int(duration / 0.1)):
        for char in chars:
            sys.stdout.write('\r' + "Loading " + char)
            sys.stdout.flush()
            time.sleep(0.1)

def waiting_animation():
    animation = "|/-\\"
    idx = 0
    while True:
        sys.stdout.write("\rMenunggu code " + animation[idx % len(animation)])
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
def wait_code(email):
    url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    p = requests.get(url).text
    pattern = r'https://github\.com/[^"]+\?via_launch_code_email=true'
    links = re.findall(pattern, p)
    valid=[]
    for link in links:
        if '\\' in link:
            pass
        else:
            valid.append(link)
    return(valid[0])

def main():
    password = 'Apalahbudak27'
    email = get_mail()
    username = generate_username()
    
    driver = webdriver.Chrome()
    driver.get('https://github.com/signup')
    wait(5)
    driver.find_element(By.ID, "email").send_keys(email)
    wait(1)
    driver.find_element(By.XPATH, "//button[@class='js-continue-button signup-continue-button form-control px-3 width-full width-sm-auto mt-4 mt-sm-0']").click()
    wait(1)
    driver.find_element(By.ID, "password").send_keys(password)
    wait(1)
    driver.find_element(By.XPATH, "//button[@data-continue-to='username-container']").click()
    wait(1)
    driver.find_element(By.ID, "login").send_keys(username)
    wait(1)
    driver.find_element(By.XPATH, "//button[@class='js-continue-button signup-continue-button form-control px-3 width-full width-sm-auto mt-4 mt-sm-0'][@data-continue-to='opt-in-container']").click()
    wait(1)
    continue_button_after_password = driver.find_element(By.XPATH, "//button[@class='js-continue-button signup-continue-button form-control px-3 width-full width-sm-auto mt-4 mt-sm-0 js-octocaptcha-load-captcha'][@data-continue-to='captcha-and-submit-container']")
    continue_button_after_password.click()
    print(f"\nUsername :  {username}\nEmail    :  {email}\nPassword :  {password}")
    input("KLIK [ENTER] JIKA SUDAH VERIFY CAPTCHA")
    link = wait_code(email=email)
    print(str(link))
    driver.get(str(link))
    driver.get('https://github.com/randsfk')
    input("KLIK [ENTER] JIKA SUDAH FOLLOW")
    driver.get("https://github.com/demonlord27")
    input("KLIK [ENTER] JIKA SUDAH FOLLOW")
    save_info(username=username, email=email, password=password)
    wait(3)
    exit()
if __name__ == "__main__":
    main()

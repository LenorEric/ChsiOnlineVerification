import requests
import json

from lxml import etree
import undetected_chromedriver as webdriver
from requests.cookies import RequestsCookieJar

session = requests.session()

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36',

}

site_url = 'https://www.chsi.com.cn'
verify_url_prefix = "https://www.chsi.com.cn/xlcx/bg.do?vcode="
captcha_url = "https://www.chsi.com.cn/xlcx/yzm.do"


def decode_element(element):
    if type(element) is str:
        return element
    if type(element) is etree._Element:
        return etree.tostring(element, encoding='utf-8', method='html').decode('utf-8')
    if type(element) is etree._ElementUnicodeResult:
        return element.encode('utf-8').decode('utf-8').strip()
    print(type(element))
    return None


def simple_parser(html_string):
    html_string = html_string.strip()[1:-1]
    html_list = html_string.split(' ')
    ret = {html_list[0]: {}}
    for item in html_list[1:]:
        key, value = item.split('=', maxsplit=1)
        value = json.loads(value)
        ret[html_list[0]][key] = value
    return ret


def extract_from_xpath(tree, path):
    ret = tree.xpath(path)
    if len(ret) == 0:
        return None
    return decode_element(ret[0])


def get_cookies(verify_url):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--incognito')
    driver = webdriver.Chrome(options=option)
    driver.get(verify_url)
    cookies_raw = driver.get_cookies()
    cookies = {}
    for cookie in cookies_raw:
        cookies[cookie['name']] = cookie['value']
    driver.quit()
    return cookies


def verify_chsi(verify_code: str):
    verify_url = verify_url_prefix + verify_code
    cookies = get_cookies(verify_url)
    cookiejar = RequestsCookieJar()
    for key in cookies:
        cookiejar.set(key, cookies[key], domain='www.chsi.com.cn', path='/')
    session.cookies = cookiejar
    response = requests.get(verify_url, headers=header)
    ret = response.text
    report_html = etree.HTML(ret)
    captcha = extract_from_xpath(report_html, '//*[@id="getXueLi"]/table/tr[1]/td[3]/img')
    if captcha is not None:
        captcha = simple_parser(captcha)['img']['src'][-4:]
        captcha_token = extract_from_xpath(report_html, '//*[@id="getXueLi"]/table/tr[1]/td[3]/input')
        captcha_token = simple_parser(captcha_token)['input']['value']
        response = session.post(captcha_url, data={'cap': captcha, 'capachatok': captcha_token, 'submit': '继续'},
                                headers=header)
        ret = response.text
    report_html = etree.HTML(ret)
    warning = extract_from_xpath(report_html, '//*[@id="rightCnt"]/div/div/h2/text()')
    if warning is not None:
        return warning
    warning = extract_from_xpath(report_html, '//*[@id="msgDiv"]/text()')
    if warning is not None:
        return warning
    try:
        portrait = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[1]/img')
        portrait = site_url + simple_parser(portrait)['img']['src']
        title = extract_from_xpath(report_html, '/html/body/div[2]/div/div[4]/div/div/div[3]/div/h4/text()')
        name = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[2]/div[2]/text()')
        gender = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[3]/div[2]/text()')
        birthday = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[4]/div[2]/text()')
        ethnic = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[5]/div[2]/text()')
        pid = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[6]/div[2]/text()')
        university = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[7]/div[2]/text()')
        degree = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[8]/div[2]/text()')
        school = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[9]/div[2]/text()')
        classes = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[10]/div[2]/text()')
        major = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[11]/div[2]/text()')
        sid = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[12]/div[2]/text()')
        forms = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[13]/div[2]/text()')
        types = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[14]/div[2]/text()')
        system = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[15]/div[2]/text()')
        admission = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[16]/div[2]/text()')
        state = extract_from_xpath(report_html, '//*[@id="resultTable"]/div/div[2]/div[17]/div[2]/text()')
        verify_data = {
            'portrait': portrait,  # 头像
            'title': title,  # 标题
            'name': name,  # 姓名
            'gender': gender,  # 性别
            'birthday': birthday,  # 生日
            'ethnic': ethnic,  # 民族
            'pid': pid,  # 身份证号
            'university': university,  # 学校
            'degree': degree,  # 层次
            'school': school,  # 学院
            'class': classes,  # 班级
            'major': major,  # 专业
            'sid': sid,  # 学号
            'form': forms,  # 学制
            'type': types,  # 类型
            'system': system,  # 形式
            'admission': admission,  # 入学时间
            'state': state  # 学籍状态
        }
    except:
        return "意外解析失败，请联系管理员修复并暂时尝试认证其他方式"
    return verify_data

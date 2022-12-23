import requests
import json
from lxml import etree

session = requests.session()

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


def verify_chsi(verify_code: str):
    verify_url = verify_url_prefix + verify_code
    ret = session.get(verify_url).text
    report_html = etree.HTML(ret)
    captcha = extract_from_xpath(report_html, '//*[@id="getXueLi"]/table/tr[1]/td[3]/img')
    if captcha is not None:
        captcha = simple_parser(captcha)['img']['src'][-4:]
        captcha_token = extract_from_xpath(report_html, '//*[@id="getXueLi"]/table/tr[1]/td[3]/input')
        captcha_token = simple_parser(captcha_token)['input']['value']
        ret = session.post(captcha_url, data={'cap': captcha, 'capachatok': captcha_token, 'submit': '继续'}).text
    report_html = etree.HTML(ret)
    warning = extract_from_xpath(report_html, '//*[@id="rightCnt"]/div/div/h2/text()')
    if warning is not None:
        return warning
    warning = extract_from_xpath(report_html, '//*[@id="msgDiv"]/text()')
    if warning is not None:
        return warning
    title = extract_from_xpath(report_html, '//*[@id="resultTable"]/div[1]/text()')
    name = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[1]/tr[1]/td[2]/img')
    name = site_url + simple_parser(name)['img']['src']
    gender = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[1]/tr[2]/td[2]/div/text()')
    pid = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[1]/tr[2]/td[4]/div/text()')
    ethnic = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[1]/tr[3]/td[2]/div/text()')
    birthday = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[1]/tr[3]/td[4]/div/text()')
    portrait = extract_from_xpath(report_html, '//*[@id="photoPositon"]')
    portrait = site_url + simple_parser(portrait)['img']['src']
    institution = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[1]/td[2]/div/text()')
    degree = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[1]/td[4]/div/text()')
    school = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[2]/td[2]/div/text()')
    classes = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[2]/td[4]/div/text()')
    major = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[3]/td[2]/div/text()')
    sid = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[3]/td[4]/div/text()')
    forms = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[4]/td[2]/div/text()')
    admission = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[4]/td[4]/div/text()')
    system = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[4]/td[6]/div/text()')
    types = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[5]/td[2]/div/text()')
    state = extract_from_xpath(report_html, '//*[@id="fixedPart"]/table[2]/tr[5]/td[4]/div/text()')
    verify_data = {
        'title': title,
        'name': name,
        'gender': gender,
        'pid': pid,
        'ethnic': ethnic,
        'birthday': birthday,
        'portrait': portrait,
        'institution': institution,
        'degree': degree,
        'school': school,
        'class': classes,
        'major': major,
        'sid': sid,
        'form': forms,
        'admission': admission,
        'system': system,
        'type': types,
        'state': state
    }
    return verify_data

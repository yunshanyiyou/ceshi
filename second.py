import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def send_message(to_user, access_token):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]

     # 开学第一周的星期一
    st_date = datetime(2022, 8, 22)
    # 现在日期
    now = datetime.today()
    # 本学期第几周
    week_num = (now - st_date).days // 7 + 1
    
    # 设置时间
    time1 = "14:30-16:00"
    time2 = "16:20-17:50"

    data = {
        "touser": to_user,
        "template_id": config["template_id2"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "time1": {
                "value": time1,
            },
             "week_num": {
                "value": week_num,
            },
            "time2": {
                "value": time2,
            }
        }
    }

    # 设置课程
    if week == "星期一":
        course1 = "今天下午"
        place1 = "没有课！"
        course2 = "没有课！！"
        place2 = "没有课！！！"
        tip = "重要的事要说三遍"
    elif week == "星期二":
        course1 = "马克思主义基本原理"
        place1 = "18-201"
        course2 = "没课了"
        place2 = "回寝室"
        tip = "别忘了带书！"
        if week_num == 7:
            course1 = "这一周没课"
            place1 = "躺平"
            tip = "我的书在哪"
    elif week == "星期三":
        course1 = "古代汉语"
        place1 = "20A-304"
        course2 = "怎么就没课了"
        place2 = "回去回去"
        tip = "求你带本书吧"
        if week_num > 1 or week_num < 13 or week_num == 17:
            course1 = "没有课呢"
            place1 = "应该在寝室吧"
            tip = "休息"
        elif week_num >= 13 and week_num <= 16:
            course1 = "形势与政策"
            place1 = "20B-201"
            tip = "有书带书"
    elif week == "星期四":
        course1 = "今天下午"
        place1 = "竟然"
        course2 = "都没有课！"
        place2 = "睡觉！"
        tip = "没有课带什么书"
    elif week == "星期五":
        course1 = "最后一天"
        place1 = "也没课了"
        course2 = "准备过周末"
        place2 = "耶耶耶！"
        tip = "摆大烂"

    #将课程数据插入data
    data["data"]["course1"] = {"value": course1}
    data["data"]["place1"] = {"value": place1}
    data["data"]["course2"] = {"value": course2}
    data["data"]["place2"] = {"value": place2}
    data["data"]["tip"] = {"value": tip, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]

    # 公众号推送消息
    for user in users:
        send_message(user, accessToken)
    os.system("pause")

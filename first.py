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
    time1 = "8:30-10:00"
    time2 = "10:20-11:50"

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
            "week_num": {
                "value": week_num,
            },
            "time1": {
                "value": time1,
            },
            "time2": {
                "value": time2,
            },
            "tip": {
                "value": "别忘了带书哦",
                "color": get_color()
            }
        }
    }

    # 设置课程
    if week == "星期一":
        course1 = "古代汉语"
        place1 = "20A-304"
        course2 = "三笔字技能训练"
        place2 = "18-203书法室"
        if week_num == (4 or 7):
            course1 = "今天早上没课"
            place1 = "睡觉"
            course2 = "今天早上没课"
            place2 = "还是睡觉"
    elif week == "星期二":
        course1 = "中国古代文学史"
        place1 = "19-402"
        course2 = "体育"
        place2 = "羽毛球场"
        if week_num == 7:
            course1 = "没有课"
            place1 = "别急着起床"
    elif week == "星期三":
        course1 = "马克思主义基本原理"
        place1 = "18-201"
        course2 = "中国当代文学史"
        place2 = "07-202"
        if week_num % 2 == 0:
            course1 = "双周没课哦"
            place1 = "继续睡吧"
        elif week_num == 7:
            course1 = "没课"
            place1 = "没课"
            course2 = "没课"
            place2 = "没课"
    elif week == "星期四":
        course1 = "中国古代文学史"
        place1 = "19-402"
        course2 = "中国当代文学史"
        place2 = "20A-304"
        if week_num == 7:
            course1 = "没课没课"
            place1 = "你怎么睡得着啊"
    elif week == "星期五":
        course1 = "第一节没课睡个懒觉吧"
        place1 = "寝室的床上"
        course2 = "专业素养培养"
        place2 = "07-303"
        if week_num > 5:
            course1 = "第一节一直都没课"
            place1 = "继续睡"
            course2 = "解放了没课了"
            place2 = "一直在睡"

    #将课程数据插入data
    data["data"]["course1"] = {"value": course1}
    data["data"]["place1"] = {"value": place1}
    data["data"]["course2"] = {"value": course2}
    data["data"]["place2"] = {"value": place2}
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

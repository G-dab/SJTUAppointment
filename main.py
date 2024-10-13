import logging
import argparse
import json
import ast
import os
import winsound

from SJTUAppointment import SJTUAppointment
from SJTUAppointment.config import FANGTANG_KEY
from SJTUAppointment.utils.messages import send_message_fangtang

def main(str, args):
    ## 解析参数
    # 1. json文件模式
    if str == 'json':
        with open(args.json, 'r', encoding='utf-8') as f:
            task = json.load(f)
    # 2. 命令行模式
    elif str == 'terminal':
        try:
            args.date = ast.literal_eval(args.date)
            args.time = ast.literal_eval(args.time)
        except:
            raise Exception("Date and Time should be list.")
        task = {
            "venue": args.venue,
            "venueItem": args.venueItem,
            "date": [int(item) for item in args.date],
            "time": [int(item) for item in args.time]
        }
    # 3. 默认
    else:
        task = {
            "venue": "气膜体育中心",
            "venueItem": "羽毛球",
            "date": [3,4,5,6,7],
            "time": [19,20,21]
        }
    
    # 创建任务
    worker = SJTUAppointment(task, headless=not args.head)
    
    try:
        worker.login()
        print("Login Successfully!")
    except Exception as e:
        print(f"[Login ERROR]: {e}")
    # 预约
    try:
        worker.book()
        print("Booking Venue!")
        send_message_fangtang('抢到场地了!', '第一行\n\n第二行', FANGTANG_KEY)
        duration = 10000  # millisecond
        freq = 440  # Hz
        winsound.Beep(freq, duration)
    except Exception as e:
        print(f"[Booking ERROR]: {e}")
        send_message_fangtang('抢场地失败!', '第一行\n\n第二行', FANGTANG_KEY)


if __name__ == "__main__":
    print("Start SJTU Sport Appointment")

    # Baic Logging Config
    currentPath = os.path.dirname(os.path.abspath(__file__))
    logfilePath = os.path.join(currentPath, "sport.log")
    logging.basicConfig(
        filename=logfilePath,
        level='INFO',
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt='%Y-%m-%d %A %H:%M:%S',
    )
    logging.info("=================================")
    logging.info("Log Started")
    
    # 解析参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--head', action='store_true')
    parser.add_argument('--json', help='json file')
    parser.add_argument('--venue', help='场馆名称')
    parser.add_argument('--venueItem', help='细分项目名称')
    parser.add_argument('--date', help='日期，用方括号表示，例如 [2,3]')
    parser.add_argument('--time', help='时间，用方括号表示，例如 [19,21]')

    args = parser.parse_args()
    if args.json:
        main('json', args)
    elif args.venue:
        main('terminal', args)
    else:
        main('default', args)
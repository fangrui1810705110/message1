import datetime


# 时间处理类
class DateUtil:
    @staticmethod
    def digital_to_week(now_date):
        '''
        根据今天日期，获取前一天对应的周几
        :param now_date: 当天日期
        :return: 返回字符串是周几
        '''
        digital = (datetime.datetime.strptime(now_date, '%Y%m%d') - datetime.timedelta(days=1)).strftime("%w")
        if digital == '0':
            return '日'
        elif digital == '1':
            return '一'
        elif digital == '2':
            return '二'
        elif digital == '3':
            return '三'
        elif digital == '4':
            return '四'
        elif digital == '5':
            return '五'
        elif digital == '6':
            return '六'

    @staticmethod
    def last_week_date(date):
        '''
        获取当前星期几上周星期几对应的日期
        :param date: 当前时间
        :return: 返回上周日期
        '''
        last_day = (datetime.datetime.strptime(date, '%Y%m%d') - datetime.timedelta(days=7)).strftime(
            "%Y%m%d")
        return str(last_day)

    @staticmethod
    def get_before_day(date):
        '''
        获取当前时间的前一天
        :param date: 当前时间
        :return: 返回前一天时间
        '''
        before_day = (datetime.datetime.strptime(date, '%Y%m%d') - datetime.timedelta(days=1)).strftime(
            "%Y%m%d")
        return before_day

    @staticmethod
    def get_after_day(date):
        '''
        返回后一天时间
        :param date:当前时间
        :return: 返回后一天的时间
        '''
        before_day = (datetime.datetime.strptime(date, '%Y%m%d') - datetime.timedelta(days=1)).strftime(
            "%Y%m%d")
        return before_day

    @staticmethod
    def get_date_time(datetime_str):
        '''
        获取当前时间
        :param datetime_str: 时间格式 %Y-%m-%d %H:%M:%S
        :return: 返回当前时间
        '''
        # # 年-月-日 时：分：秒
        # now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # # 年
        # year = datetime.datetime.now().strftime('%Y')
        # # 年-月
        # month = datetime.datetime.now().strftime('%Y-%m')
        # # 年-月-日
        # day = datetime.datetime.now().strftime('%Y-%m-%d')
        # # 时：分：秒
        # hour = datetime.datetime.now().strftime("%H:%M:%S")

        now_time = datetime.datetime.now().strftime(datetime_str)
        return now_time

    # 获取两个日期之间的时间范围
    @staticmethod
    def getEveryDay(begin_date, end_date):
        # 前闭后闭
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y%m%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list
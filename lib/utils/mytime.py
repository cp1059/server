
import time
import datetime
import random
import calendar

class UtilTime(object):

    def __init__(self, timezone='local', arrow=None):

        self.arrow = arrow
        if not self.arrow:
            import arrow
            self.arrow = arrow
        #时区
        self.timezone = timezone

    # 获取当前时间的arrow结构
    @property
    def today(self):
        return self.arrow.now(self.timezone)

    # 当前时间戳
    @property
    def timestamp(self):
        return self.today.timestamp

    # 获取当前时间,自定义format
    def get_today_format(self, format_v="YYYY-MM-DD HH:mm:ss"):
        return self.today.format(format_v)

    # 时间戳转arrow
    def timestamp_to_arrow(self, timestamp=None):
        return self.arrow.get(timestamp).to(
            self.timezone) if timestamp else timestamp

    # arrow转时间戳
    def arrow_to_timestamp(self, arrow_v=None):
        return arrow_v.timestamp if arrow_v else arrow_v

    #arrow转字符串
    def arrow_to_string(self, arrow_s=None, format_v="YYYY-MM-DD HH:mm:ss"):
        return arrow_s.format(format_v) if arrow_s else self.today.format(format_v)

    #字符串转arrow
    def string_to_arrow(self, string_s=None, format_v="YYYY-MM-DD HH:mm:ss"):
        return self.arrow.get(
            string_s, format_v, tzinfo=self.timezone) if string_s else string_s

    #时间戳转字符串
    def timestamp_to_string(self, timestamp,format_v="%Y-%m-%d %H:%M:%S"):

        time_local = time.localtime(int(timestamp))
        return time.strftime(format_v, time_local)

    # #时间戳转arrow
    # def timestamp_to_arrow(self, timestamp):
    #     return self.arrow.get(timestamp)

    #字符串转时间戳
    def string_to_timestamp(self, string_s=None,
                            format_v="YYYY-MM-DD HH:mm:ss"):
        return self.string_to_arrow(
            string_s, format_v).timestamp if string_s else string_s

    #时间日期加减
    def replace(self, arrow_v, **kwargs):
        """
			example :
				days = -1  减一天
				weeks = -1 减一周
				mounts = -1 减一个月
				quarters = -1 减一个季度
				years = -1 减一年
				hours = -1 减一小时
				minutes = -1 减一分钟
				seconds = -1 减一秒钟
		"""
        return arrow_v.shift(**kwargs)

    #判断周几
    def get_week_day(self, todays=None):
        """
			todays: "YYYY-MM-DD" 字符串
			周一:1 ... 周日:7
		"""
        format_v = "YYYY-MM-DD"
        day_arrow = self.today if not todays else self.string_to_arrow(
            todays, format_v)
        day_string = self.arrow_to_string(
            self.today, format_v) if not todays else self.arrow_to_string(
                self.string_to_arrow(todays, format_v), format_v)

        week1 = day_arrow.floor('week')
        if self.arrow_to_string(week1, format_v) == day_string:
            return 1
        elif self.arrow_to_string(week1.replace(days=1),
                                  format_v) == day_string:
            return 2
        elif self.arrow_to_string(week1.replace(days=2),
                                  format_v) == day_string:
            return 3
        elif self.arrow_to_string(week1.replace(days=3),
                                  format_v) == day_string:
            return 4
        elif self.arrow_to_string(week1.replace(days=4),
                                  format_v) == day_string:
            return 5
        elif self.arrow_to_string(week1.replace(days=5),
                                  format_v) == day_string:
            return 6
        elif self.arrow_to_string(week1.replace(days=6),
                                  format_v) == day_string:
            return 7
        else:
            return None


def send_toTimestamp(t):
    t1=str(t)
    t2=time.strptime(t1[0:19],"%Y-%m-%d %H:%M:%S")
    return time.mktime(t2)

def get_current_month_start_and_end(date):
    """
    年份 date(2017-09-08格式)
    :param date:
    :return:本月第一天日期和本月最后一天日期
    """
    if date.count('-') != 2:
        raise ValueError('- is error')
    year, month = str(date).split('-')[0], str(date).split('-')[1]
    end = calendar.monthrange(int(year), int(month))[1]
    start_date = '%s-%s-01' % (year, month)
    end_date = '%s-%s-%s' % (year, month, end)
    return start_date, end_date

if __name__ == '__main__':

    def count_downtime():

        ut = UtilTime()

        # currtime = ut.arrow_to_string(format_v="HHmmss")
        currtime="234700"
        tables=[{"id": "001", "opentime": "0030", "endtime": "002700"}, {"id": "002", "opentime": "0050", "endtime": "004700"}, {"id": "003", "opentime": "0110", "endtime": "010700"}, {"id": "004", "opentime": "0130", "endtime": "012700"}, {"id": "005", "opentime": "0150", "endtime": "014700"}, {"id": "006", "opentime": "0210", "endtime": "020700"}, {"id": "007", "opentime": "0230", "endtime": "022700"}, {"id": "008", "opentime": "0250", "endtime": "024700"}, {"id": "009", "opentime": "0310", "endtime": "030700"}, {"id": "010", "opentime": "0730", "endtime": "072700"}, {"id": "011", "opentime": "0750", "endtime": "074700"}, {"id": "012", "opentime": "0810", "endtime": "080700"}, {"id": "013", "opentime": "0830", "endtime": "082700"}, {"id": "014", "opentime": "0850", "endtime": "084700"}, {"id": "015", "opentime": "0910", "endtime": "090700"}, {"id": "016", "opentime": "0930", "endtime": "092700"}, {"id": "017", "opentime": "0950", "endtime": "094700"}, {"id": "018", "opentime": "1010", "endtime": "100700"}, {"id": "019", "opentime": "1030", "endtime": "102700"}, {"id": "020", "opentime": "1050", "endtime": "104700"}, {"id": "021", "opentime": "1110", "endtime": "110700"}, {"id": "022", "opentime": "1130", "endtime": "112700"}, {"id": "023", "opentime": "1150", "endtime": "114700"}, {"id": "024", "opentime": "1210", "endtime": "120700"}, {"id": "025", "opentime": "1230", "endtime": "122700"}, {"id": "026", "opentime": "1250", "endtime": "124700"}, {"id": "027", "opentime": "1310", "endtime": "130700"}, {"id": "028", "opentime": "1330", "endtime": "132700"}, {"id": "029", "opentime": "1350", "endtime": "134700"}, {"id": "030", "opentime": "1410", "endtime": "140700"}, {"id": "031", "opentime": "1430", "endtime": "142700"}, {"id": "032", "opentime": "1450", "endtime": "144700"}, {"id": "033", "opentime": "1510", "endtime": "150700"}, {"id": "034", "opentime": "1530", "endtime": "152700"}, {"id": "035", "opentime": "1550", "endtime": "154700"}, {"id": "036", "opentime": "1610", "endtime": "160700"}, {"id": "037", "opentime": "1630", "endtime": "162700"}, {"id": "038", "opentime": "1650", "endtime": "164700"}, {"id": "039", "opentime": "1710", "endtime": "170700"}, {"id": "040", "opentime": "1730", "endtime": "172700"}, {"id": "041", "opentime": "1750", "endtime": "174700"}, {"id": "042", "opentime": "1810", "endtime": "180700"}, {"id": "043", "opentime": "1830", "endtime": "182700"}, {"id": "044", "opentime": "1850", "endtime": "184700"}, {"id": "045", "opentime": "1910", "endtime": "190700"}, {"id": "046", "opentime": "1930", "endtime": "192700"}, {"id": "047", "opentime": "1950", "endtime": "194700"}, {"id": "048", "opentime": "2010", "endtime": "200700"}, {"id": "049", "opentime": "2030", "endtime": "202700"}, {"id": "050", "opentime": "2050", "endtime": "204700"}, {"id": "051", "opentime": "2110", "endtime": "210700"}, {"id": "052", "opentime": "2130", "endtime": "212700"}, {"id": "053", "opentime": "2150", "endtime": "214700"}, {"id": "054", "opentime": "2210", "endtime": "220700"}, {"id": "055", "opentime": "2230", "endtime": "222700"}, {"id": "056", "opentime": "2250", "endtime": "224700"}, {"id": "057", "opentime": "2310", "endtime": "230700"}, {"id": "058", "opentime": "2330", "endtime": "232700"}, {"id": "059", "opentime": "2350", "endtime": "234700"}]
        tables.sort(key=lambda k: (k.get('id')), reverse=False)
        isFlag = False
        for tItem in tables:
            item = tItem['endtime']
            if int(currtime) < int(item):
                print(currtime, item)
                end_time = (int(item[:2]) * 60 * 60) + (int(item[2:4]) * 60) + int(item[4:])
                start_time = (int(currtime[:2]) * 60 * 60) + (int(currtime[2:4]) * 60) + int(currtime[4:])
                currtime = end_time - start_time
                isFlag = True
                break
        print(isFlag)
        if not isFlag:
            item = tables[0]['endtime']
            end_time = (int(item[:2]) * 60 * 60) + (int(item[2:4]) * 60) + int(item[4:])
            start_time = (int(currtime[:2]) * 60 * 60) + (int(currtime[2:4]) * 60) + int(currtime[4:])
            print(currtime)
            currtime = end_time + (1 * 24 * 60 * 60) - start_time

            print(currtime, item)

        return {"h": currtime // 3600, "m": currtime % 3600 // 60, "s": currtime % 60}


    print(count_downtime())
    # a="102135"
    # print(a[0:2],a[2:4],a[4:])
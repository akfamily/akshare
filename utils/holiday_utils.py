# -*- coding:utf-8 -*-

# Author: PeterWeyland
# CreateTime: 2025-10-11
# Description: simple introduction of the code
import datetime
import lunardate
from typing import Set, Dict


class ChinaHolidayChecker:
    _holidays_cache: Dict[int, Set[datetime.date]] = {}

    @classmethod
    def get_holidays_for_year(cls, year: int) -> Set[datetime.date]:
        """获取指定年份的所有节假日日期"""
        if year in cls._holidays_cache:
            return cls._holidays_cache[year]

        holidays = set()

        # 元旦（阳历1月1日）
        holidays.add(datetime.date(year, 1, 1))

        # 春节（阴历12月30日到1月6日）
        spring_festival_dates = cls._get_spring_festival_dates(year)
        holidays.update(spring_festival_dates)

        # 清明节（阳历4月5日）
        holidays.add(datetime.date(year, 4, 5))

        # 劳动节（阳历5月1日到5月4日）
        for day in range(1, 5):
            holidays.add(datetime.date(year, 5, day))

        # 端午节（阴历5月5日）
        dragon_boat_date = cls._get_dragon_boat_date(year)
        holidays.add(dragon_boat_date)

        # 中秋节（阴历8月15日）
        mid_autumn_date = cls._get_mid_autumn_date(year)
        holidays.add(mid_autumn_date)

        # 国庆节（阳历10月1日到10月7日）
        for day in range(1, 8):
            holidays.add(datetime.date(year, 10, day))

        cls._holidays_cache[year] = holidays
        return holidays

    @classmethod
    def _get_spring_festival_dates(cls, year: int) -> Set[datetime.date]:
        """获取春节日期（阴历12月30日到1月6日）"""
        dates = set()

        # 春节通常在阳历的1月或2月，我们计算前一年和当年的春节
        for y in [year - 1, year]:
            try:
                # 获取阴历12月30日（除夕）
                lunar_new_year_eve = lunardate.LunarDate(y, 12, 30).toSolarDate()
                # 如果阳历年份匹配，添加到结果中
                if lunar_new_year_eve.year == year:
                    # 添加阴历12月30日到1月6日
                    for i in range(7):  # 12月30日到1月6日共7天
                        date = lunar_new_year_eve + datetime.timedelta(days=i)
                        dates.add(date)
            except ValueError:
                # 有些年份阴历12月只有29天
                try:
                    lunar_new_year_eve = lunardate.LunarDate(y, 12, 29).toSolarDate()
                    if lunar_new_year_eve.year == year:
                        for i in range(7):
                            date = lunar_new_year_eve + datetime.timedelta(days=i)
                            dates.add(date)
                except:
                    pass
        return dates

    @classmethod
    def _get_dragon_boat_date(cls, year: int) -> datetime.date:
        """获取端午节日期（阴历5月5日）"""
        lunar_date = lunardate.LunarDate(year, 5, 5)
        return lunar_date.toSolarDate()

    @classmethod
    def _get_mid_autumn_date(cls, year: int) -> datetime.date:
        """获取中秋节日期（阴历8月15日）"""
        lunar_date = lunardate.LunarDate(year, 8, 15)
        return lunar_date.toSolarDate()

    @classmethod
    def is_weekend(cls, date: datetime.date) -> bool:
        """判断是否为周末"""
        return date.weekday() in [5, 6]  # 5=周六, 6=周日

    @classmethod
    def is_holiday(cls, date: datetime.date) -> bool:
        """判断是否为节假日"""
        holidays = cls.get_holidays_for_year(date.year)
        return date in holidays

    @classmethod
    def is_workday(cls, date: datetime.date) -> bool:
        """判断是否为工作日（非周末且非节假日）"""
        return not cls.is_weekend(date) and not cls.is_holiday(date)

    @classmethod
    def should_send_message(cls, date: datetime.date) -> bool:
        """判断指定日期是否应该发送消息"""
        # 如果是工作日 → 发
        if cls.is_workday(date):
            return True

        # 如果是周六 → 不发（因为周日会发）
        if date.weekday() == 5:  # 周六
            return False

        # 如果是周日或节假日 → 检查下一天
        tomorrow = date + datetime.timedelta(days=1)

        # 如果下一天是工作日 → 今天发（作为假期最后一天）
        if cls.is_workday(tomorrow):
            return True

        # 其他情况（下一天还是假期）→ 不发
        return False


# 使用示例
def main():
    # 测试一些日期
    test_dates = [
        datetime.date(2024, 1, 1),  # 元旦（周一）- 应该发（假期最后一天）
        datetime.date(2024, 1, 2),  # 周二工作日 - 应该发
        datetime.date(2024, 1, 6),  # 周六 - 不发
        datetime.date(2024, 1, 7),  # 周日 - 发（周末最后一天）
        datetime.date(2024, 10, 1),  # 国庆节第一天 - 不发
        datetime.date(2024, 10, 7),  # 国庆节最后一天 - 发
    ]

    print("测试结果：")
    for date in test_dates:
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]
        holiday_info = "节假日" if ChinaHolidayChecker.is_holiday(date) else ""
        weekend_info = "周末" if ChinaHolidayChecker.is_weekend(date) else ""
        workday_info = "工作日" if ChinaHolidayChecker.is_workday(date) else ""

        status = holiday_info or weekend_info or workday_info
        should_send = ChinaHolidayChecker.should_send_message(date)

        print(f"{date} ({weekday}) {status:8} -> {'发送' if should_send else '不发送'}")

    # 每日检查示例
    def daily_check():
        today = datetime.date.today()
        if ChinaHolidayChecker.should_send_message(today):
            print(f"\n今天 {today} 需要发送消息！")
            # 这里执行发送消息的操作
        else:
            print(f"\n今天 {today} 不需要发送消息")

    daily_check()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sxtwl

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
# 获取相主信息
day = sxtwl.fromSolar(2001,10,9)

# 公历的年月日
s = "公历:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(),
                      day.getSolarDay())
print(s)

#年属
yearshu = day.getYearGZ()
print(Zhi[yearshu.dz])

#月属
mouthshu = day.getMonthGZ()
print(Zhi[mouthshu.dz])

#日属
dayshu = day.getDayGZ()
print(Zhi[dayshu.dz])

#相主年月日转换成数字，year代表数字，mouth代表数字，day代表数字
year = day.getSolarYear()
mouth = day.getSolarMonth()
day = day.getSolarDay()

# 获取第一年采相的年日信息
days = sxtwl.fromSolar(year + 1, mouth, day + 1)
#采相年日转换成数字，year代表数字，mouth代表数字，day代表数字
years = days.getSolarYear()
mouths = days.getSolarMonth()
dayss = days.getSolarDay()

#采相当天转换成汉字当天是什么什么年属月属日属
#年属
yearshus = days.getYearGZ()

#月属
mouthshus = days.getMonthGZ()

#日属
dayshus = days.getDayGZ()


def calculate_scores(animals):
    # 相五行
    elements = {
        '鼠': '水',
        '牛': '土',
        '虎': '木',
        '兔': '木',
        '龙': '土',
        '蛇': '火',
        '马': '火',
        '羊': '土',
        '猴': '金',
        '鸡': '金',
        '狗': '土',
        '猪': '水'
    }

    # 采相相基分
    pair_scores = {
        '龙龙': -10,
        '龙虎': 10,
        '龙鸡': 35,
        '龙蛇': 10,
        '龙猪': 10,
        '龙兔': -20,
        '龙猴': 25,
        '龙鼠': 25,
        '龙牛': 30,
        '龙羊': 10,
        '龙狗': -5,
        '龙马': 10,
        '虎虎': 10,
        '虎鸡': 10,
        '虎蛇': -20,
        '虎猪': 35,
        '虎兔': 10,
        '虎猴': -10,
        '虎鼠': 10,
        '虎牛': 10,
        '虎羊': 30,
        '虎狗': 25,
        '虎马': 25,
        '鸡鸡': -10,
        '鸡蛇': 25,
        '鸡猪': 10,
        '鸡兔': -5,
        '鸡猴': 10,
        '鸡鼠': 30,
        '鸡牛': 25,
        '鸡羊': 10,
        '鸡狗': -20,
        '鸡马': 10,
        '蛇蛇': 10,
        '蛇猪': -5,
        '蛇兔': 30,
        '蛇猴': 35,
        '蛇鼠': 10,
        '蛇牛': 25,
        '蛇羊': 10,
        '蛇狗': 10,
        '蛇马': 10,
        '猪猪': -10,
        '猪兔': 25,
        '猪猴': -20,
        '猪鼠': 10,
        '猪牛': 10,
        '猪羊': 25,
        '猪狗': 30,
        '猪马': 10,
        '兔兔': 10,
        '兔猴': 10,
        '兔鼠': -10,
        '兔牛': 10,
        '兔羊': 25,
        '兔狗': 35,
        '兔马': -10,
        '猴猴': 10,
        '猴鼠': 25,
        '猴牛': 10,
        '猴羊': 10,
        '猴狗': 10,
        '猴马': 30,
        '鼠鼠': 10,
        '鼠牛': 35,
        '鼠羊': -20,
        '鼠狗': 10,
        '鼠马': -10,
        '牛牛': 10,
        '牛羊': -10,
        '牛狗': -10,
        '牛马': -20,
        '羊羊': 10,
        '羊狗': -10,
        '羊马': 35,
        '狗狗': 10,
        '狗马': 25,
        '马马': -10
    }

    # 五行组合的分数
    element_scores = {
        ('土', '土'): 10,
        ('金', '金'): 10,
        ('水', '水'): 10,
        ('木', '木'): 10,
        ('火', '火'): 10,
        ('土', '金'): 25,
        ('金', '土'): 25,
        ('金', '水'): 25,
        ('水', '金'): 25,
        ('水', '木'): 25,
        ('木', '水'): 25,
        ('木', '火'): 25,
        ('火', '木'): 25,
        ('火', '土'): 25,
        ('土', '火'): 25,
        ('土', '水'): 0,
        ('水', '土'): 0,
        ('金', '木'): 0,
        ('木', '金'): 0,
        ('水', '火'): 0,
        ('火', '水'): 0,
        ('木', '土'): 0,
        ('土', '木'): 0,
        ('火', '金'): 0,
        ('金', '火'): 0,
    }

    total_score = 0
    element_score_total = 0
    results = {}

    # 计算属成相后的分数和相五行的分数
    for i in range(len(animals)):
        for j in range(i + 1, len(animals)):
            # 获取相
            animal_pair = animals[i] + animals[j]
            if animal_pair not in pair_scores:
                animal_pair = animals[j] + animals[i]  # 保证顺序正确
            # 计算相基分数
            pair_score = pair_scores.get(animal_pair, 0)
            total_score += pair_score
            obversion_total_score = total_score * 0.7
            # 计算五行对分数
            element_pair = (elements[animals[i]], elements[animals[j]])
            if element_pair not in element_scores:
                element_pair = (element_pair[1], element_pair[0])  # 保证顺序

            element_score = element_scores.get(element_pair, 0)
            element_score_total += element_score
            obversion_element_score_total = element_score_total * 0.3
            # 计算相基70%与相五行30%分数之和
            one = obversion_element_score_total + obversion_total_score + 0

    results['基础分'] = total_score
    results['相五行分'] = element_score_total
    results['相基的70%+相五行的30%'] = one

    return results


# 计算18年后的年份
end_year = year + 18

while years < end_year:  # 只输出到18年
    print(
        years,
        "-",
        mouths,
        ":",
        Zhi[yearshu.dz],
        Zhi[yearshus.dz],
        Zhi[dayshu.dz],
        Zhi[dayshus.dz],
    )
    years += 1

    nian = Zhi[yearshu.dz]
    yue = Zhi[yearshus.dz]
    ri = Zhi[dayshu.dz]
    shi = Zhi[dayshus.dz]

    # 示例输入
    animals = [nian, yue, ri, shi]
    results = calculate_scores(animals)
    # 只打印汇总结果
    print(f"基础分: {results['基础分']}")
    print(f"相五行分: {results['相五行分']}")
    print(f"相基的70%+相五行的30%: {results['相基的70%+相五行的30%']}")

    # 获取下一年采相的信息
    days = sxtwl.fromSolar(years, mouths, dayss)

    # 提取下一年采相当天的信息，只提取年月日，用汉字来记录
    yearshus = days.getYearGZ()
    mouthshus = days.getMonthGZ()
    dayshus = days.getDayGZ()
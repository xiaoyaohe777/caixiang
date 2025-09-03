#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sxtwl
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

class ZodiacCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("采真属相排盘工具-采相四轮宫位神")
        self.root.geometry("600x900")
        
        # 创建字体
        self.title_font = font.Font(size=14, weight='bold')  # 标题字体
        self.big_font = font.Font(size=12)  # 大字体
        self.normal_font = font.Font(size=11)  # 普通字体
        
        self.create_widgets()
        
    def create_widgets(self):
        # 输入框区域
        input_frame = ttk.LabelFrame(self.root, text="输入信息 - 年份和时辰需要单独选一下", padding=10)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # 日期输入
        ttk.Label(input_frame, text="公历日期:").grid(row=0, column=0, sticky=tk.W)
        
        self.year_var = tk.StringVar(value="2001")
        self.month_var = tk.StringVar(value="10")
        self.day_var = tk.StringVar(value="9")
        
        ttk.Entry(input_frame, textvariable=self.year_var, width=8).grid(row=0, column=1)
        ttk.Label(input_frame, text="年").grid(row=0, column=2)
        ttk.Entry(input_frame, textvariable=self.month_var, width=4).grid(row=0, column=3)
        ttk.Label(input_frame, text="月").grid(row=0, column=4)
        ttk.Entry(input_frame, textvariable=self.day_var, width=4).grid(row=0, column=5)
        ttk.Label(input_frame, text="日").grid(row=0, column=6)
        
        # 属相输入
        ttk.Label(input_frame, text="年份属相:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.year_zhi_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.year_zhi_var, values=Zhi, width=4).grid(row=1, column=1)
        
        ttk.Label(input_frame, text="时辰属相:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.hour_zhi_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.hour_zhi_var, values=Zhi, width=4).grid(row=1, column=3)
        
        # 字体大小控制滑块
        ttk.Label(input_frame, text="标题字体:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.font_size = tk.IntVar(value=14)  # 默认值14
        ttk.Scale(input_frame, from_=10, to=24, variable=self.font_size,
                 command=self.update_font_size, length=150).grid(row=2, column=1, columnspan=5)
        
        # 计算按钮
        ttk.Button(input_frame, text="计算", command=self.calculate).grid(row=2, column=7, padx=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(self.root, text="计算结果", padding=10)
        result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # 创建文本显示区域
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=25, font=self.normal_font)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置标签样式
        self.result_text.tag_configure('title', font=self.title_font)
        self.result_text.tag_configure('big', font=self.big_font)
        
        # 底部按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="清空", command=self.clear_results).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).grid(row=0, column=1, padx=5)
    
    def update_font_size(self, event=None):
        """更新标题字体大小"""
        size = self.font_size.get()
        self.title_font.configure(size=size)
        self.result_text.tag_configure('title', font=self.title_font)
    
    def calculate(self):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            day = int(self.day_var.get())
            year_zhi = self.year_zhi_var.get()
            hour_zhi = self.hour_zhi_var.get()
            
            # 验证输入有效性
            if not (1 <= month <= 12):
                raise ValueError("月份必须在1-12之间")
            if not (1 <= day <= 31):
                raise ValueError("日期必须在1-31之间")
            if year_zhi not in Zhi:
                raise ValueError("请输入有效的年份属相")
            if hour_zhi not in Zhi:
                raise ValueError("请输入有效的时辰属相")
            
            # 清空结果文本框
            self.result_text.delete(1.0, tk.END)
            
            # 获取相主信息
            day_obj = sxtwl.fromSolar(year, month, day)
            
            # 显示基本信息
            self.result_text.insert(tk.END, f"公历: {year}年{month}月{day}日\n\n", 'title')
            
            # 年属
            yearshu = day_obj.getYearGZ()
            nian = Zhi[yearshu.dz]
            self.result_text.insert(tk.END, f"年属: {nian}\n", 'big')
            
            # 月属
            mouthshu = day_obj.getMonthGZ()
            yue = Zhi[mouthshu.dz]
            self.result_text.insert(tk.END, f"月属: {yue}\n", 'big')
            
            # 日属
            dayshu = day_obj.getDayGZ()
            ri = Zhi[dayshu.dz]
            self.result_text.insert(tk.END, f"日属: {ri}\n\n", 'big')
            
            # 获取第一年采相的年日信息
            days = sxtwl.fromSolar(year + 1, month, day + 1)
            
            # 采相当天的信息
            yearshus = days.getYearGZ()
            dayshus = days.getDayGZ()
            
            # 宫位神分数据
            extra_results = {
    # 鼠年数据
    ("鼠", "鼠"): ["鼠牛 10", "鼠虎 20", "鼠兔 15", "鼠龙 -10"],
    ("鼠", "牛"): ["牛兔 -20", "牛龙 30", "牛蛇 10", "牛马 -20"],
    ("鼠", "虎"): ["虎蛇 0", "虎马 30", "虎羊 15", "虎猴 -40"],
    ("鼠", "兔"): ["兔羊 10", "兔猴 -10", "兔鸡 -30", "兔狗 10"],
    ("鼠", "龙"): ["龙鸡 50", "龙狗 5", "龙猪 10", "龙鼠 -10"],
    ("鼠", "蛇"): ["蛇猪 -30", "蛇鼠 10", "蛇牛 10", "蛇虎 0"],
    ("鼠", "马"): ["马牛 -20", "马虎 30", "马兔 15", "马龙 0"],
    ("鼠", "羊"): ["羊兔 10", "羊龙 5", "羊蛇 20", "羊马 50"],
    ("鼠", "猴"): ["猴蛇 10", "猴马 -15", "猴羊 10", "猴猴 15"],
    ("鼠", "鸡"): ["鸡羊 0", "鸡猴 25", "鸡鸡 25", "鸡狗 0"],
    ("鼠", "狗"): ["狗鸡 0", "狗狗 15", "狗猪 15", "狗鼠 -20"],
    ("鼠", "猪"): ["猪猪 0", "猪鼠 5", "猪牛 0", "猪虎 30"],
    # 牛年数据
    ("牛", "鼠"): ["鼠鼠 15", "鼠牛 10", "鼠虎 20", "鼠兔 15"],
    ("牛", "牛"): ["牛虎 -10", "牛兔 -20", "牛龙 30", "牛蛇 10"],
    ("牛", "虎"): ["虎龙 -20", "虎蛇 0", "虎马 30", "虎羊 15"],
    ("牛", "兔"): ["兔马 15", "兔羊 10", "兔猴 -10", "兔鸡 -30"],
    ("牛", "龙"): ["龙猴 30", "龙鸡 50", "龙狗 5", "龙猪 10"],
    ("牛", "蛇"): ["蛇狗 10", "蛇猪 -30", "蛇鼠 10", "蛇牛 10"],
    ("牛", "马"): ["马鼠 -20", "马牛 -20", "马虎 30", "马兔 15"],
    ("牛", "羊"): ["羊虎 15", "羊兔 10", "羊龙 5", "羊蛇 20"],
    ("牛", "猴"): ["猴龙 30", "猴蛇 10", "猴马 -15", "猴羊 10"],
    ("牛", "鸡"): ["鸡马-10", "鸡羊 0", "鸡猴 25", "鸡鸡 25"],
    ("牛", "狗"): ["狗猴 20", "狗鸡 0", "狗狗 15", "狗猪 15"],
    ("牛", "猪"): ["猪狗 15", "猪猪 0", "猪鼠 5", "猪牛 0"],
    # 虎年数据
    ("虎", "鼠"): ["鼠猪 5", "鼠鼠 15", "鼠牛 10", "鼠虎 20"],
    ("虎", "牛"): ["牛牛 15", "牛虎 -10", "牛兔 -20", "牛龙 30"],
    ("虎", "虎"): ["虎兔 25", "虎龙 -20", "虎蛇 0", "虎马 30"],
    ("虎", "兔"): ["兔蛇 25", "兔马 15", "兔羊 10", "兔猴 -10"],
    ("虎", "龙"): ["龙羊 5", "龙猴 30", "龙鸡 50", "龙狗 5"],
    ("虎", "蛇"): ["蛇鸡 -10", "蛇狗 10", "蛇猪 -30", "蛇鼠 10"],
    ("虎", "马"): ["马猪 -10", "马鼠 -20", "马牛 -20", "马虎 30"],
    ("虎", "羊"): ["羊牛 -25", "羊虎 15", "羊兔 10", "羊龙 5"],
    ("虎", "猴"): ["猴兔 -10", "猴龙 30", "猴蛇 10", "猴马 -15"],
    ("虎", "鸡"): ["鸡蛇 -10", "鸡马 -10", "鸡羊 0", "鸡猴 25"],
    ("虎", "狗"): ["狗羊 -10", "狗猴 20", "狗鸡 0", "狗狗 15"],
    ("虎", "猪"): ["猪鸡 20", "猪狗 15", "猪猪 0", "猪鼠 5"],
    # 兔年数据
    ("兔", "鼠"): ["鼠狗 -20", "鼠猪 5", "鼠鼠 15", "鼠牛 10"],
    ("兔", "牛"): ["牛鼠 10", "牛牛 15", "牛虎 -10", "牛兔 -20"],
    ("兔", "虎"): ["虎龙 -20", "虎兔 25", "虎龙 -20", "虎蛇 0"],
    ("兔", "兔"): ["兔龙 -40", "兔蛇 25", "兔马 15", "兔羊 10"],
    ("兔", "龙"): ["龙马 0", "龙羊 5", "龙猴 30", "龙鸡 50"],
    ("兔", "蛇"): ["蛇猴 10", "蛇鸡 -10", "蛇狗 10", "蛇猪 -30"],
    ("兔", "马"): ["马狗 10", "马猪 -10", "马鼠 -20", "马牛 -20"],
    ("兔", "羊"): ["羊鼠 -20", "羊牛 -25", "羊虎 15", "羊兔 10"],
    ("兔", "猴"): ["猴虎 -40", "猴兔 -10", "猴龙 30", "猴蛇 10"],
    ("兔", "鸡"): ["鸡龙 50", "鸡蛇 -10", "鸡马-10", "鸡羊 0"],
    ("兔", "狗"): ["狗马 10", "狗羊 -10", "狗猴 20", "狗鸡 0"],
    ("兔", "猪"): ["猪猴 0", "猪鸡 20", "猪狗 15", "猪猪 0"],
    # 龙年数据
    ("龙", "鼠"): ["鼠鸡 15", "鼠狗 -20", "鼠猪 5", "鼠鼠 15"],
    ("龙", "牛"): ["牛猪 0", "牛鼠 10", "牛牛 15", "牛虎 -10"],
    ("龙", "虎"): ["虎牛 -10", "虎龙 -20", "虎兔 25", "虎龙 -20"],
    ("龙", "兔"): ["兔兔 15", "兔龙 -40", "兔蛇 25", "兔马 15"],
    ("龙", "龙"): ["龙蛇 10", "龙马 0", "龙羊 5", "龙猴 30"],
    ("龙", "蛇"): ["蛇羊 20", "蛇猴 10", "蛇鸡 -10", "蛇狗 10"],
    ("龙", "马"): ["马鸡 -10", "马狗 10", "马猪 -10", "马鼠 -20"],
    ("龙", "羊"): ["羊猪 -10", "羊鼠 -20", "羊牛 -25", "羊虎 15"],
    ("龙", "猴"): ["猴牛 30", "猴虎 -40", "猴兔 -10", "猴龙 30"],
    ("龙", "鸡"): ["鸡兔 -30", "鸡龙 50", "鸡蛇 -10", "鸡马-10"],
    ("龙", "狗"): ["狗蛇 10", "狗马 10", "狗羊 -10", "狗猴 20"],
    ("龙", "猪"): ["猪羊 -10", "猪猴 0", "猪鸡 20", "猪狗 15"],
    # 蛇年数据
    ("蛇", "鼠"): ["鼠猴 10", "鼠鸡 15", "鼠狗 -20", "鼠猪 5"],
    ("蛇", "牛"): ["牛狗 10", "牛猪 0", "牛鼠 10", "牛牛 15"],
    ("蛇", "虎"): ["虎鼠 20", "虎牛 -10", "虎龙 -20", "虎兔 25"],
    ("蛇", "兔"): ["兔虎 25", "兔兔 15", "兔龙 -40", "兔蛇 25"],
    ("蛇", "龙"): ["龙龙 45", "龙蛇 10", "龙马 0", "龙羊 5"],
    ("蛇", "蛇"): ["蛇马 25", "蛇羊 20", "蛇猴 10", "蛇鸡 -10"],
    ("蛇", "马"): ["马猴 -15", "马鸡 -10", "马狗 10", "马猪 -10"],
    ("蛇", "羊"): ["羊狗 -10", "羊猪 -10", "羊鼠 -20", "羊牛 -25"],
    ("蛇", "猴"): ["猴鼠 10", "猴牛 30", "猴虎 -40", "猴兔 -10"],
    ("蛇", "鸡"): ["鸡虎 -10", "鸡兔 -30", "鸡龙 50", "鸡蛇 -10"],
    ("蛇", "狗"): ["狗龙 5", "狗蛇 10", "狗马 10", "狗羊 -10"],
    ("蛇", "猪"): ["猪马 -10", "猪羊 -10", "猪猴 0", "猪鸡 20"],
    # 马年数据
    ("马", "鼠"): ["鼠羊 -20", "鼠猴 10", "鼠鸡 15", "鼠狗 -20"],
    ("马", "牛"): ["牛鸡 30", "牛狗 10", "牛猪 0", "牛鼠 10"],
    ("马", "虎"): ["虎猪 30", "虎鼠 20", "虎牛 -10", "虎龙 -20"],
    ("马", "兔"): ["兔牛 -20", "兔虎 25", "兔兔 15", "兔龙 -40"],
    ("马", "龙"): ["龙兔 -40", "龙龙 45", "龙蛇 10", "龙马 0"],
    ("马", "蛇"): ["蛇蛇 30", "蛇马 25", "蛇羊 20", "蛇猴 10"],
    ("马", "马"): ["马羊 50", "马猴 -15", "马鸡 -10", "马狗 10"],
    ("马", "羊"): ["羊鸡 0", "羊狗 -10", "羊猪 -10", "羊鼠 -20"],
    ("马", "猴"): ["猴猪 0", "猴鼠 10", "猴牛 30", "猴虎 -40"],
    ("马", "鸡"): ["鸡牛 30", "鸡虎 -10", "鸡兔 -30", "鸡龙 50"],
    ("马", "狗"): ["狗兔 10", "狗龙 5", "狗蛇 10", "狗马 10"],
    ("马", "猪"): ["猪蛇-30", "猪马 -10", "猪羊 -10", "猪猴 0"],
    # 羊年数据
    ("羊", "鼠"): ["鼠马 -20", "鼠羊 -20", "鼠猴 10", "鼠鸡 15"],
    ("羊", "牛"): ["牛猴 30", "牛鸡 30", "牛狗 10", "牛猪 0"],
    ("羊", "虎"): ["虎狗 -10", "虎猪 30", "虎鼠 20", "虎牛 -10"],
    ("羊", "兔"): ["兔鼠 15", "兔牛 -20", "兔虎 25", "兔兔 15"],
    ("羊", "龙"): ["龙虎 -20", "龙兔 -40", "龙龙 45", "龙蛇 10"],
    ("羊", "蛇"): ["蛇龙 10", "蛇蛇 30", "蛇马 25", "蛇羊 20"],
    ("羊", "马"): ["马马 0", "马羊 50", "马猴 -15", "马鸡 -10"],
    ("羊", "羊"): ["羊猴 10", "羊鸡 0", "羊狗 -10", "羊猪 -10"],
    ("羊", "猴"): ["猴狗 20", "猴猪 0", "猴鼠 10", "猴牛 30"],
    ("羊", "鸡"): ["鸡鼠 15", "鸡牛 30", "鸡虎 -10", "鸡兔 -30"],
    ("羊", "狗"): ["狗虎 -10", "狗兔 10", "狗龙 5", "狗蛇 10"],
    ("羊", "猪"): ["猪龙 10", "猪蛇-30", "猪马 -10", "猪羊 -10"],
    # 猴年数据
    ("猴", "鼠"): ["鼠蛇 10", "鼠马 -20", "鼠羊 -20", "鼠猴 10"],
    ("猴", "牛"): ["牛羊 -25", "牛猴 30", "牛鸡 30", "牛狗 10"],
    ("猴", "虎"): ["虎鸡 -10", "虎狗 -10", "虎猪 30", "虎鼠 20"],
    ("猴", "兔"): ["兔猪 10", "兔鼠 15", "兔牛 -20", "兔虎 25"],
    ("猴", "龙"): ["龙牛 30", "龙虎 -20", "龙兔 -40", "龙龙 45"],
    ("猴", "蛇"): ["蛇兔 25", "蛇龙 10", "蛇蛇 30", "蛇马 25"],
    ("猴", "马"): ["马蛇 25", "马马 0", "马羊 50", "马猴 -15"],
    ("猴", "羊"): ["羊羊 15", "羊猴 10", "羊鸡 0", "羊狗 -10"],
    ("猴", "猴"): ["猴鸡 25", "猴狗 20", "猴猪 0", "猴鼠 10"],
    ("猴", "鸡"): ["鸡猪 20", "鸡鼠 15", "鸡牛 30", "鸡虎 -10"],
    ("猴", "狗"): ["狗牛 10", "狗虎 -10", "狗兔 10", "狗龙 5"],
    ("猴", "猪"): ["猪兔 10", "猪龙 10", "猪蛇 -30", "猪马 -10"],
    # 鸡年数据
    ("鸡", "鼠"): ["鼠龙 -10", "鼠蛇 10", "鼠马 -20", "鼠羊 -20"],
    ("鸡", "牛"): ["牛马 -20", "牛羊 -25", "牛猴 30", "牛鸡 30"],
    ("鸡", "虎"): ["虎猴 -40", "虎鸡 -10", "虎狗 -10", "虎猪 30"],
    ("鸡", "兔"): ["兔狗 10", "兔猪 10", "兔鼠 15", "兔牛 -20"],
    ("鸡", "龙"): ["龙鼠 -10", "龙牛 30", "龙虎 -20", "龙兔 -40"],
    ("鸡", "蛇"): ["蛇虎 0", "蛇兔 25", "蛇龙 10", "蛇蛇 30"],
    ("鸡", "马"): ["马龙 0", "马蛇 25", "马马 0", "马羊 50"],
    ("鸡", "羊"): ["羊马 50", "羊羊 15", "羊猴 10", "羊鸡 0"],
    ("鸡", "猴"): ["猴猴 15", "猴鸡 25", "猴狗 20", "猴猪 0"],
    ("鸡", "鸡"): ["鸡狗 0", "鸡猪 20", "鸡鼠 15", "鸡牛 30"],
    ("鸡", "狗"): ["狗鼠 -20", "狗牛 10", "狗虎 -10", "狗兔 10"],
    ("鸡", "猪"): ["猪虎 30", "猪兔 10", "猪龙 10", "猪蛇-30"],
    # 狗年数据
    ("狗", "鼠"): ["鼠兔 15", "鼠龙 -10", "鼠蛇 10", "鼠马 -20"],
    ("狗", "牛"): ["牛蛇 10", "牛马 -20", "牛羊 -25", "牛猴 30"],
    ("狗", "虎"): ["虎羊 15", "虎猴 -40", "虎鸡 -10", "虎狗 -10"],
    ("狗", "兔"): ["兔鸡 -30", "兔狗 10", "兔猪 10", "兔鼠 15"],
    ("狗", "龙"): ["龙猪 10", "龙鼠 -10", "龙牛 30", "龙虎 -20"],
    ("狗", "蛇"): ["蛇牛 10", "蛇虎 0", "蛇兔 25", "蛇龙 10"],
    ("狗", "马"): ["马兔 15", "马龙 0", "马蛇 25", "马马 0"],
    ("狗", "羊"): ["羊蛇 20", "羊马 50", "羊羊 15", "羊猴 10"],
    ("狗", "猴"): ["猴羊 10", "猴猴 15", "猴鸡 25", "猴狗 20"],
    ("狗", "鸡"): ["鸡鸡 25", "鸡狗 0", "鸡猪 20", "鸡鼠 15"],
    ("狗", "狗"): ["狗猪 15", "狗鼠 -20", "狗牛 10", "狗虎 -10"],
    ("狗", "猪"): ["猪牛 0", "猪虎 30", "猪兔 10", "猪龙 10"],
    # 猪年数据
    ("猪", "鼠"): ["鼠虎 20", "鼠兔 15", "鼠龙 -10", "鼠蛇 10"],
    ("猪", "牛"): ["牛龙 30", "牛蛇 10", "牛马 -20", "牛羊 -25"],
    ("猪", "虎"): ["虎马 30", "虎羊 15", "虎猴 -40", "虎鸡 -10"],
    ("猪", "兔"): ["兔猴 -10", "兔鸡 -30", "兔狗 10", "兔猪 10"],
    ("猪", "龙"): ["龙狗 5", "龙猪 10", "龙鼠 -10", "龙牛 30"],
    ("猪", "蛇"): ["蛇鼠 10", "蛇牛 10", "蛇虎 0", "蛇兔 25"],
    ("猪", "马"): ["马虎 30", "马兔 15", "马龙 0", "马蛇 25"],
    ("猪", "羊"): ["羊龙 5", "羊蛇 20", "羊马 50", "羊羊 15"],
    ("猪", "猴"): ["猴马 -15", "猴羊 10", "猴猴 15", "猴鸡 25"],
    ("猪", "鸡"): ["鸡猴 25", "鸡鸡 25", "鸡狗 0", "鸡猪 20"],
    ("猪", "狗"): ["狗狗 15", "狗猪 15", "狗鼠 -20", "狗牛 10"],
    ("猪", "猪"): ["猪鼠 5", "猪牛 0", "猪虎 30", "猪兔 10"],
            }
            extra_result_list = extra_results.get((year_zhi, hour_zhi), ["", "", "", ""])
            
            # 计算并显示未来70年的评分
            self.result_text.insert(tk.END, "=== 四轮采相和宫位神分值 ===\n\n", 'big')
            
            # 跳过1-18年的输出
            years_to_calc = year + 18  # 直接跳到第18年
            
            # 只输出4次结果，每次间隔13年
            for i in range(4):
                # 获取当前周期的采相信息
                days = sxtwl.fromSolar(years_to_calc, month, day + 1)
                
                # 提取当前采相当天的信息
                current_yearshus = days.getYearGZ()
                current_dayshus = days.getDayGZ()
                
                # 输出当前周期结果
                self.result_text.insert(tk.END, 
                    f"{years_to_calc}年-{month}月: {nian} {Zhi[current_yearshus.dz]} {ri} {Zhi[current_dayshus.dz]}\n", 
                    'title')
                
                # 提取宫位神分中的数字
                extra_text = extra_result_list[i]
                extra_score = 0
                if " " in extra_text:
                    try:
                        extra_score = int(extra_text.split(" ")[1])
                    except (ValueError, IndexError):
                        extra_score = 0
                
                # 计算评分
                animals = [nian, Zhi[current_yearshus.dz], ri, Zhi[current_dayshus.dz]]
                results = self.calculate_scores(animals, extra_score)
                
                # 显示评分结果
                self.result_text.insert(tk.END, f"基础分: {results['基础分']}\n", 'big')
                self.result_text.insert(tk.END, f"相五行分: {results['相五行分']}\n", 'big')
                self.result_text.insert(tk.END, f"宫位神: {extra_result_list[i]}\n", 'big')
                self.result_text.insert(tk.END, f"相基+相五行+宫位神: {results['相基的70%+相五行的30%']:.1f}\n\n", 'big')
                
                years_to_calc += 13
            
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的日期: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"计算过程中发生错误: {e}")
    
    def calculate_scores(self, animals, extra_score=0):
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
                # 计算相基70%与相五行30%分数之和，并加上宫位神分数的70%
                one = obversion_element_score_total + obversion_total_score + (extra_score * 0.7)

        results['基础分'] = total_score
        results['相五行分'] = element_score_total
        results['相基的70%+相五行的30%'] = one

        return results
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZodiacCalculator(root)
    root.mainloop()
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
        self.root.title("采真属相排盘工具-四轮采相")
        self.root.geometry("600x900")
        
        # 创建字体
        self.title_font = font.Font(size=14, weight='bold')  # 标题字体（可调节）
        self.big_font = font.Font(size=12)  # 大字体（放大）
        self.normal_font = font.Font(size=11)  # 普通字体（放大）
        
        self.create_widgets()
        
    def create_widgets(self):
        # 输入框区域
        input_frame = ttk.LabelFrame(self.root, text="输入设置", padding=10)
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
        
        # 字体大小控制滑块
        ttk.Label(input_frame, text="标题字体:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.font_size = tk.IntVar(value=14)  # 默认值14
        ttk.Scale(input_frame, from_=10, to=24, variable=self.font_size,
                 command=self.update_font_size, length=150).grid(row=2, column=1, columnspan=5)
        
        # 计算按钮
        ttk.Button(input_frame, text="计算四轮采相分值", command=self.calculate).grid(row=1, column=7, padx=10)
        
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
            
            # 验证日期有效性
            if not (1 <= month <= 12):
                raise ValueError("月份必须在1-12之间")
            if not (1 <= day <= 31):
                raise ValueError("日期必须在1-31之间")
            
            # 清空结果文本框
            self.result_text.delete(1.0, tk.END)
            
            # 获取相主信息
            day_obj = sxtwl.fromSolar(year, month, day)
            
            # 显示基本信息，使用大字体
            self.result_text.insert(tk.END, f"公历: {year}年{month}月{day}日\n\n", 'title')
            
            # 年属
            yearshu = day_obj.getYearGZ()
            self.nian = Zhi[yearshu.dz]
            self.result_text.insert(tk.END, f"年属: {self.nian}\n", 'big')
            
            # 月属
            mouthshu = day_obj.getMonthGZ()
            yue = Zhi[mouthshu.dz]
            self.result_text.insert(tk.END, f"月属: {yue}\n", 'big')
            
            # 日属
            dayshu = day_obj.getDayGZ()
            self.ri = Zhi[dayshu.dz]
            self.result_text.insert(tk.END, f"日属: {self.ri}\n\n", 'big')
            
            # 获取第一年采相的年日信息
            days = sxtwl.fromSolar(year + 1, month, day + 1)
            
            # 采相当天的信息
            yearshus = days.getYearGZ()
            dayshus = days.getDayGZ()
            
            # 计算并显示四轮采相分值
            self.result_text.insert(tk.END, "=== 四轮采相分值 ===\n\n", 'big')

            # 跳过1-18年的输出
            years_to_calc = year + 18  # 直接跳到第18年
            
            # 只输出4次结果，每次间隔13年
            for _ in range(4):
                # 获取当前周期的采相信息
                days = sxtwl.fromSolar(years_to_calc, month, day + 1)
                
                # 提取当前采相当天的信息
                current_yearshus = days.getYearGZ()
                current_dayshus = days.getDayGZ()
                
                # 输出当前周期结果，使用大字体
                self.result_text.insert(tk.END, 
                    f"{years_to_calc}年 - {month}月: {self.nian} {Zhi[current_yearshus.dz]} {self.ri} {Zhi[current_dayshus.dz]}\n", 
                    'title')
                
                # 计算评分
                animals = [self.nian, Zhi[current_yearshus.dz], self.ri, Zhi[current_dayshus.dz]]
                results = self.calculate_scores(animals)
                
                # 显示评分结果
                self.result_text.insert(tk.END, f"基础分: {results['基础分']}\n", 'big')
                self.result_text.insert(tk.END, f"相五行分: {results['相五行分']}\n", 'big')
                self.result_text.insert(tk.END, f"相基的70%+相五行的30%: {results['相基的70%+相五行的30%']}\n\n", 'big')
                
                years_to_calc += 13
            
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的日期: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"计算过程中发生错误: {e}")
    
    def calculate_scores(self, animals):
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
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZodiacCalculator(root)
    root.mainloop()
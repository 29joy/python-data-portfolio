# 导入相关包
import json
from pyecharts.charts import Line
from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, LabelOpts, TooltipOpts
from pyecharts.options import DataZoomOpts
from collections import Counter
# 得到折线图对象
line = Line()
# 处理数据
f_usa = open(r"D:\code_joy\python\pythonProject\data\USA.json", 'r', encoding = 'UTF-8')
usa_data = f_usa.read()
f_jpn = open(r"D:\code_joy\python\pythonProject\data\JPN.json", 'r', encoding = 'UTF-8')
jpn_data = f_jpn.read()
f_ind = open(r"D:\code_joy\python\pythonProject\data\IND.json", 'r', encoding = 'UTF-8')
ind_data = f_ind.read()
# json转python字典
usa_python_dict = json.loads(usa_data)
jpn_python_dict = json.loads(jpn_data)
ind_python_dict = json.loads(ind_data)
# 过滤掉值为0的数据
filtered_usa_data = [entry for entry in usa_python_dict["USA"] if entry["new_cases"] and entry["new_cases"] > 0]
filtered_jpn_data = [entry for entry in jpn_python_dict["JPN"] if entry["new_cases"] and entry["new_cases"] > 0]
filtered_ind_data = [entry for entry in ind_python_dict["IND"] if entry["new_cases"] and entry["new_cases"] > 0]
# 计算是否有重复数据
usa_dates = [entry["date"] for entry in filtered_usa_data]
date_count = Counter(usa_dates)
for date, count in date_count.items():
    if count > 1:
        print(f"USA {date} 出现了 {count} 次")

jpn_dates = [entry["date"] for entry in filtered_jpn_data]
date_count = Counter(jpn_dates)
for date, count in date_count.items():
    if count > 1:
        print(f"JPN {date} 出现了 {count} 次")

ind_dates = [entry["date"] for entry in filtered_ind_data]
date_count = Counter(ind_dates)
for date, count in date_count.items():
    if count > 1:
        print(f"IND {date} 出现了 {count} 次")
# 获取日期数据用于x轴
# 取三个国家的日期集合
usa_dates = set([entry["date"] for entry in filtered_usa_data if entry["new_cases"] > 0])
jpn_dates = set([entry["date"] for entry in filtered_jpn_data if entry["new_cases"] > 0])
ind_dates = set([entry["date"] for entry in filtered_ind_data if entry["new_cases"] > 0])
# 取三个国家的日期交集
common_dates = sorted(usa_dates & jpn_dates & ind_dates)
# 根据交集筛选每个国家的数据
def filter_by_dates(data, country_key, valid_dates):
    return [entry for entry in data[country_key] if entry["date"] in valid_dates]

usa_filtered = filter_by_dates(usa_python_dict, "USA", common_dates)
jpn_filtered = filter_by_dates(jpn_python_dict, "JPN", common_dates)
ind_filtered = filter_by_dates(ind_python_dict, "IND", common_dates)
# 分别构造 x 和 y
x_date = common_dates
y_usa = [entry["new_cases"] for entry in usa_filtered]
y_jpn = [entry["new_cases"] for entry in jpn_filtered]
y_ind = [entry["new_cases"] for entry in ind_filtered]
# 验证x轴和y轴数据量匹配
print("x轴日期数:", len(x_date))
print("USA数据点数:", len(y_usa))
print("JPN数据点数:", len(y_jpn))
print("IND数据点数:", len(y_ind))
# x轴和y轴数据赋值
line.add_xaxis(x_date)
line.add_yaxis("USA new_cases", y_usa, is_smooth=True, label_opts=LabelOpts(is_show=False))
line.add_yaxis("JPN new_cases", y_jpn, is_smooth=True, label_opts=LabelOpts(is_show=False))
line.add_yaxis("IND new_cases", y_ind, is_smooth=True, label_opts=LabelOpts(is_show=False))
# 配置全局选项
line.set_global_opts(
    title_opts=TitleOpts(title="COVID-19 New Cases Comparison", pos_left="center", pos_bottom="1%"),
    legend_opts=LegendOpts(is_show=True),
    toolbox_opts=ToolboxOpts(is_show=True),
    tooltip_opts=TooltipOpts(is_show=True),
)
# 生成图表
line.render("2020_covid_new_cases.html")
# 关闭文件对象
f_usa.close()
f_jpn.close()
f_ind.close()

# 导入相关包
from pyecharts.charts import Map
from pyecharts.options import VisualMapOpts

map = Map()
data = [
    ("北京", 399),
    ("天津", 299),
    ("上海", 699),
    ("湖北", 1299),
    ("山东", 699),
    ("河南", 799),
    ("广东", 1199),
    ("重庆", 899),
    ("浙江", 899),
    ("江苏", 899),
    ("山西", 299),
    ("辽宁", 399),
]
# [
#     "北京", "天津", "上海", "重庆", "河北", "河南", "云南", "辽宁", "黑龙江", "湖南", "安徽",
#     "山东", "新疆", "江苏", "浙江", "江西", "湖北", "广西", "甘肃", "山西", "内蒙古", "陕西",
#     "吉林", "福建", "贵州", "广东", "青海", "西藏", "四川", "宁夏", "海南", "台湾", "香港", "澳门"
# ]
map.add("地图", data, maptype="china")

# 设置全局选项
map.set_series_opts(label_opts={"is_show": True})  # 显示省份标签
map.set_global_opts(
    title_opts={"text": "中国各省新增病例分布图"},
    visualmap_opts=VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        pieces=[
            {"min":1, "max":9, "label":"1-9人", "color":"#CCFFFF"},
            {"min": 10, "max": 99, "label": "10-99人", "color": "#FFFF99"},
            {"min": 100, "max": 499, "label": "100-499人", "color": "#FF9966"},
            {"min": 500, "max": 999, "label": "500-999人", "color": "#FF6666"},
            {"min": 1000, "max": 9999, "label": "1000-9999人", "color": "#CC3333"},
            {"min": 10000, "label": "10000人以上", "color": "#990033"},
        ],
    series_index=0
    )
)
map.render("2020_covid_china_map.html")

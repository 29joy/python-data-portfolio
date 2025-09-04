# 只包含动态柱状图
# =====================================================动态柱状图=================================================================

# 动态图表需求分析
"""
1、GDP数据处理为亿级
2、有时间轴, 按照年份为时间轴的点
3、x轴和y轴反转, 同时每一年的数据只要前8名国家
4、有标题, 标题的年份会动态更改
5、设置了主题的LIGHT
"""
# ---------------------------------------------------数据处理-----------------------------------------------------------
import json
from pyecharts.charts import Bar, Timeline
from pyecharts.options import LabelOpts

# 打开文件
f = open(r"D:\code_joy\python\pythonProject\data\GDP.json", 'r', encoding = 'UTF-8')
data = f.read()
# print(data)
# 关闭文件
f.close()
# 转化为python列表
data_python_list = json.loads(data)# 一开始忘了转化成python数据, 下面进行排序一直报错

# 发现数据中包含很多非单一国家的数据, 如'World', 'High income', 'OECD members'等, 需要对数据进行过滤
sovereign_countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas, The", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei Darussalam",
    "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Dem. Rep.", "Congo, Rep.", "Costa Rica", "Cote d'Ivoire",
    "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt, Arab Rep.", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia, The", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran, Islamic Rep.",
    "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Rep.",
    "Kuwait", "Kyrgyz Republic", "Lao PDR", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
    "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
    "Mauritania", "Mauritius", "Mexico", "Micronesia, Fed. Sts.", "Moldova", "Monaco", "Mongolia", "Montenegro",
    "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russian Federation", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
    "Slovak Republic", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka",
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syrian Arab Republic", "Tajikistan", "Tanzania", "Thailand",
    "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkiye", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",
    "Venezuela, RB", "Viet Nam", "Yemen, Rep.", "Zambia", "Zimbabwe", "Holy See"
]
data_list_unitary_state = [entry for entry in data_python_list if entry["Country Name"] in sovereign_countries]
year_set = set()
for entry in data_list_unitary_state:
    year_set.add(entry["Year"])
year_list = list(year_set)
year_list = sorted(year_list)
# print(year_list)

data_list = [[] for _ in range(len(year_list))]
value_list = [[] for _ in range(len(year_list))]
country_name_list = [[] for _ in range(len(year_list))]
for i in range(len(year_list)):
    data_list[i] = []
    for entry in data_list_unitary_state:
        if entry["Year"] == year_list[i]:
            data_list[i].append(entry)
    for entry in data_list[i]:
        data_list[i].sort(key=lambda element:element["Value"], reverse=True)
    filtered_data_list = data_list[i][0:8]
    value_list[i] = []
    country_name_list[i] = []
    for entry in filtered_data_list:
        value_list[i].append(round(entry["Value"] / 100000000, 2))
        country_name_list[i].append(entry["Country Name"])
    value_list[i].reverse()
    country_name_list[i].reverse()
# print(value_list)
# print(country_name_list)

# ---------------------------------------------------创建图表-----------------------------------------------------------
# 创建时间线
timeline = Timeline()

for i in range(len(year_list)):
    bar = Bar()
    bar.add_xaxis(country_name_list[i])  # 国家为 X
    bar.add_yaxis("GDP（亿美元）", value_list[i], label_opts=LabelOpts(position="right"))
    bar.reversal_axis()
    bar.set_global_opts(title_opts={"text": f"{year_list[i]} 年全球 GDP 前8国家"})
    # bar_list.append(bar)
    timeline.add(bar, f"{year_list[i]}")
# 数据自动播放
timeline.add_schema(
    play_interval=1000,# 自动播放的时间间隔, 单位毫秒
    is_timeline_show=True,# 是否在自动播放的时候显示时间线
    is_auto_play=True,# 是否自动播放
    is_loop_play=True# 是否循环自动播放
)
# 时间线设置主题
timeline = Timeline(
    {"theme": ThemeType.LIGHT}
)
# 通过时间轴绘图
timeline.render("ALL_Countries_GDP_Comparison_Bar.html")

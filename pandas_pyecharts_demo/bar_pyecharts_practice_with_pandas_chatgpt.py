import pandas as pd
from pyecharts.charts import Bar, Timeline
from pyecharts.options import LabelOpts

# === Step 1: 加载 JSON 文件 ===
df = pd.read_json(r"D:\code_joy\python\pythonProject\data\GDP.json")  # 替换为你的实际文件路径

# === Step 2: 清洗数据 ===
df = df[df["Value"].notnull()]  # 去除空值
df = df[df["Country Name"] != "World"]  # 可选: 去除 "World"
df = df[df["Year"].between(1960, 2023)]  # 限定年份范围

# === Step 3: 获取每年 GDP 前8国家 ===
top8_per_year = df.groupby("Year").apply(
    lambda g: g.sort_values("Value", ascending=False).head(8)
).reset_index(drop=True)

# === Step 4: 构建动态柱状图 ===
timeline = Timeline()

years = sorted(top8_per_year["Year"].unique())
for year in years:
    year_data = top8_per_year[top8_per_year["Year"] == year]
    countries = year_data["Country Name"].tolist()
    gdp_values = (year_data["Value"] / 1e8).round(2).tolist()  # 转为“亿美元”

    bar = Bar()
    bar.add_xaxis(countries)
    bar.add_yaxis("GDP（亿美元）", gdp_values, label_opts=LabelOpts(position="right"))
    bar.reversal_axis()
    bar.set_global_opts(title_opts={"text": f"{year} 年全球 GDP 前8国家"})

    timeline.add(bar, str(year))

timeline.add_schema(
    play_interval=1000,
    is_auto_play=True,
    is_loop_play=True
)

timeline.render("timeline_gdp_bar_chart.html")

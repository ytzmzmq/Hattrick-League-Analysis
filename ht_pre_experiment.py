#!/usr/bin/env python
# coding: utf-8
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import random
import pandas as pd
import matplotlib.pyplot as plt #画图库
import seaborn as sns #画图库

# 设置随机种子44
random.seed(44)

# Level 1 直接取 1

# Level 2 (共 4 组，抽 2 组)
level_2_samples = sorted(random.sample(range(1, 5), 2))
print(f"Level 2 需要抽取的组号: {level_2_samples}")

# Level 3 (共 16 组，抽 4 组)
level_3_samples = sorted(random.sample(range(1, 17), 4))
print(f"Level 3 需要抽取的组号: {level_3_samples}")

# Level 4 (共 64 组，抽 8 组)
level_4_samples = sorted(random.sample(range(1, 65), 8))
print(f"Level 4 需要抽取的组号: {level_4_samples}")

# Level 5 (共 256 组，抽 15 组)
level_5_samples = sorted(random.sample(range(1, 257), 15))
print(f"Level 5 需要抽取的组号: {level_5_samples}")

# 导入文件 (确保 CSV 文件与本 py 文件放在同一个文件夹下)
file_path = "Hattrick_Points_preexperiment.csv"
df = pd.read_csv(file_path)
print(df.head())


#groupby用于分组
#['Points']只计算该列数据
#agg用于聚合
#round(2)保留两位小数
stats = df.groupby('Level')['Points'].agg(
    球队数 = 'count',
    平均分 = 'mean',
    最高分 = 'max',
    最低分 = 'min',
    方差 = 'var',
    偏度 = 'skew'
).round(2)

print(stats)


# seaborn 设置网格背景风格
sns.set_theme(style="whitegrid")

# 在图表上正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False # 防止负号显示成方块


#概率密度曲线图（KDE）
#由于截断其面积总和小于1

# plt.figure() 使matplotlib给出画布
# figsize=(10, 6) 即宽度为 10 英寸，高度为 6 英寸
plt.figure(figsize=(10, 6))

# df['Level'].unique() 会找出所有的级别（1, 2, 3, 4, 5）
# sorted() 会确保它们是按从小到大的顺序排列的
levels = sorted(df['Level'].unique())

#for循环绘制 5 条概率密度曲线曲线
for level in levels:
    # “切片”，例如 level 是 1 的时候，就把所有 Level 1 的球队数据单独抽出来
    subset = df[df['Level'] == level]

    # 呼叫 seaborn (sns) 的kdeplot函数来画 kde 概率密度曲线
    sns.kdeplot(
        data=subset,      # 画的数据是 subset
        x='Points',       # X轴的数据是 'Points'
        label=f'Level {level}',  # 给这条线贴标签，方便绘制图例
        fill=True,        # 把曲线下方的面积涂上颜色！
        alpha=0.3,         # 透明度设为 0.3（范围0-1），这样不同颜色的曲线重叠时不会互相遮挡
        clip=(0,42)       #clip()函数限制分布在0-42之间
    )

# 设置主标题（fontsize 控制字体大小）
plt.title('Hattrick 各级别联赛积分概率密度分布 (KDE)', fontsize=15)

# 设置 X 轴和 Y 轴的说明文字
plt.xlabel('联赛积分 (Points)', fontsize=12)
plt.ylabel('概率密度 (Density)', fontsize=12)

# plt.legend() 会自动把在前面写过的 label='Level x' 收集起来，放在右上角形成图例
plt.legend(title='联赛级别 (Level)')

# 调整一下排版，防止文字被边缘裁切
plt.tight_layout()

# 保存到电脑，先保存后展示
plt.savefig('KDE_Plot.png', dpi=300)

# 把画好的图展示在屏幕上！
plt.show()


#离散直方图（此时y轴是频率）
# 【不需要 plt.figure】
# 【不需要 for 循环】
# 【不需要 subset 切片】
# 直接把完整的 df 扔给 displot 即可

g = sns.displot(
    data=df,           # 直接用完整的表格
    x='Points',        # X轴是积分
    row='Level',       # displot自动按 Level 拆分成多行(完美替代了 for 循环)
    kind='hist',       # 画直方图
    discrete=True,     # 保持离散的整数柱子
    stat='probability',# Y轴显示该级别的占比
    height=2,          # 每张小图的高度（英寸）
    aspect=4,          # 每张小图的宽是高的4倍（即宽度为8）
    palette='Set2',    # 颜色风格
    hue='Level'        # 按级别涂上不同颜色
)

# 强行命令每一个子图都打开底部数字 (labelbottom=True)
for ax in g.axes.flatten():
    ax.tick_params(labelbottom=True)

# 给整个大画板加上总标题
g.figure.suptitle('各级别联赛积分真实分布 (离散直方图)', y=1.02, fontsize=15)

# X轴的说明由于是通用的，写一次就行
plt.xlabel('联赛积分 (0-42分)', fontsize=12)

# 先保存，后展示
plt.savefig('Hist_Split.png', dpi=300, bbox_inches='tight')
plt.show()


#箱线图

#figsize设置图片尺寸
plt.figure(figsize=(8, 6))

# boxplot函数绘制箱线图
sns.boxplot(
    data=df,       # 数据表
    x='Level',     # 横向按 1-5 级排开
    y='Points',    # 纵向画积分
    hue='Level',    # 颜色按 Level 划分
    palette='Set2', # 选择颜色主题
    legend=False   # 关掉重复的图例
)

plt.title('Hattrick 各级别联赛积分箱线图', fontsize=15)
plt.xlabel('联赛级别 (Level)', fontsize=12)
plt.ylabel('联赛积分 (Points)', fontsize=12)

# range()强制Y轴刻度按5分一档显示
plt.yticks(range(0, 46, 5))

#保存图片
plt.savefig('Boxplot_Focus.png', dpi=300, bbox_inches='tight')
plt.show()

#统计
# 1. 定义分位数函数
def q1(x): return x.quantile(0.25)
def q3(x): return x.quantile(0.75)

# 2. 核心聚合计算
#将所有数据储存在res里面
res = df.groupby('Level')['Points'].agg([
    ('n', 'count'),
    ('Mean', 'mean'),
    ('SD', 'std'),
    ('Median', 'median'),
    ('Q1', q1),
    ('Q3', q3),
    ('Min', 'min'),
    ('Max', 'max'),
    ('Skew', 'skew')
]).round(2)

# 3. 拼接成三线表格式的字符串列
#res[]创建新列
#res['Mean'].astype(str)将浮点数float转换为文本
# + 是文本连接符
#向量化执行（会遍历res表格的所有行）
res['均值 ± SD'] = res['Mean'].astype(str) + " ± " + res['SD'].astype(str)
res['中位数 [Q1, Q3]'] = res['Median'].astype(str) + " [" + res['Q1'].astype(str) + ", " + res['Q3'].astype(str) + "]"
res['范围 (Min-Max)'] = res['Min'].astype(str) + " - " + res['Max'].astype(str)

# 4. 只选取需要的列展示
final_table = res[['n', '均值 ± SD', '中位数 [Q1, Q3]', '范围 (Min-Max)', 'Skew']]
print(final_table)


# 分布类型计数
# 1. 定义一个分类函数，基于偏度(skew)
# 0.5为界，绝对值≤0.5为对称，＞0.5为右偏，＜0.5为左偏
def classify_dist(points):
    s = points.skew()
    if abs(s) <= 0.5: return "均衡竞争型 (对称)"
    elif s > 0.5:     return "底层密集型 (右偏)"
    else:             return "一强多弱型 (左偏)"

# 2. 对 (Level, Series_ID) 进行分组并应用分类
# 这步会生成 30 行数据，每行是一个小组的结论
# 链式调用，df.groupby(['Level', 'Series_ID'])按两个维度进行分组，['Points']指定列，.apply(classify_dist)运行定义的分类函数，.reset_index()将数据恢复标准格式
series_report = df.groupby(['Level', 'Series_ID'])['Points'].apply(classify_dist).reset_index()

# 给列重新命名，确保第三列叫“分布类型”
series_report.columns = ['Level', 'Series_ID', '分布类型']

# 3. 使用 groupby 和 unstack 做出最终的汇总表
# size() 算个数，此时仍然是纵向排列
# unstack() 把“分布类型”从行变成列
# (fill_value=0)填补空白处为0
summary = series_report.groupby(['Level', '分布类型']).size().unstack(fill_value=0)

# 4. 合计
#axis=0（默认值）：纵向求和。它会把每一列的所有数字加起来，最后在最下面多出一行
#axis=1：横向求和。它会顺着每一行，把该行所有的列（均衡、左偏、右偏）加在一起
summary['小组总计'] = summary.sum(axis=1)
summary.loc['总计'] = summary.sum(axis=0)

print(summary)

# 导出最终报表
summary.to_excel("Hattrick预实验分析报告.xlsx")


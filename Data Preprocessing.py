
import numpy as np
import pandas as pd
import re

data2024_html = 'https://www.e-stat.go.jp/stat-search/files?stat_infid=000040297536'

df_2024 = pd.read_excel(data2024_html)

# データ全体を表示
print(df_2024)

# データの上部のみを表示
print(df_2024.head())

# データの行を表示
print(df_2024.index)

# データの列を表示
print(df_2024.columns)

# データファイルの1～8行目までは、ヘッダーとして使用する7行目を除いて読み込みをスキップする。
# また「全国（人口集中地区）」「全国（人口集中地区以外の地区）」は1965年までの欠損値が大きくあるのでこれもスキップする。
# 沖縄県は1945年に欠損値がある。列番号16～18を指定して、欠損値の"-"をnp.nanに変換する。
# スキップしたあとの最初の行はヘッダーとして扱い、また最初の列はDataFrameのindexとして扱う。
# 行、列の指定はプログラム内では0から数える数値となっている。
df0 = pd.read_excel('da01.xlsx',skiprows=[0,1,2,3,4,5,7,9,10],header=0,index_col=0,converters={i:lambda x:np.nan if x=="-" else int(x) for i in range(16,19)})

# DataFrameのインデックスを整形する。
# データファイルでは0000_全国のようにコード_県名なので、
# _ 以降だけをインデックスとして使用する。
m = map(lambda l:re.findall(r".*_(.*)",l)[0],df0.index)
df0 = df0.set_axis(list(m),axis="index")

# DataFrameの列名を整形する。
# データファイルでは7行目を列名として使用するが、
# 1920年, 大正9年, (空白), ... となっている。それぞれの意味は、1920の総数、男、女の人口なので、
# それに合わせた列名になるように修正する。
column_labels = []
for i in range(0,len(df0.columns),3):
  for l in ["総数","男","女"]:
    column_labels.append(f"{df0.columns[i]}_{l}")
df0 = df0.set_axis(column_labels,axis="columns")
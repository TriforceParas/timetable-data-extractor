import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df_list = pd.read_html("http://time-table.sicsr.ac.in", match="Time:")

df = df_list[0]
df.to_csv('Timetable.csv',index=False)

df_read = pd.read_csv('Timetable.csv')
print(df_read)
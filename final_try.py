import pandas as pd
import itertools as it
import numpy as np

df1 = pd.DataFrame(
    [['emp1', (0, 1, 3)], ['emp2', (2, 2, 4)], ['emp3', (2, 3, 5)], ['emp4', (1, 1, 2)], ['emp5', (3, 3, 1)]],
    columns=['emp_id', 'e_values'])
df2 = pd.DataFrame(
    [['mach1', (1, 3, 2)], ['mach2', (3, 3, 1)], ['mach3', (4, 2, 3)], ['mach4', (2, 1, 2)], ['mach5', (2, 1, 1)]],
    columns=['mode_id', 'm_values'])
df1['key'] = 0
df2['key'] = 0
df = df2.merge(df1)
df.drop(labels='key', axis=1, inplace=True)

df['subtraction'] = df[['m_values', 'e_values']].apply(
    lambda row: [x - y for x, y in zip(row['e_values'], row['m_values'])], axis=1)

df['coef_+'] = df['subtraction'].apply(lambda x: sum([i for i in x if i > 0]))
df['coef_-'] = df['subtraction'].apply(lambda x: sum([i for i in x if i < 0]))
df['absolute_error'] = df['subtraction'].apply(lambda x: sum([abs(i) for i in x]))

df = df.sort_values(by=['absolute_error', 'coef_-', 'coef_+'], ascending=[True, False, True])
df.reset_index(drop=True, inplace=True)
all_emp = list(df['emp_id'].unique())
all_mach = list(df['mode_id'].unique())

curr_m = df['mode_id'].iloc[0]
curr_e = df['emp_id'].iloc[0]

emp_group = []
print(df)

emp_tmp = []
result_pairs = []

k = 0
for row in df.values:
    if curr_m != row[0]:
        for m, e in emp_group:
            if (len(emp_group) == 1) & (m in all_mach) & (e in all_emp):
                result_pairs.append((m, e))
                all_mach.remove(m)
                all_emp.remove(e)
            elif (m in all_mach) & (e in all_emp):
                emp_indexes = [n for n, x in enumerate(list(df['emp_id'])) if (x == e) & (n >= k)]
                if emp_indexes:
                    emp_tmp.append((m, e, min(emp_indexes)))
        if emp_tmp:
            a, b = sorted(emp_tmp, key=lambda x: x[2], reverse=True)[0][:2]
            result_pairs.append((a, b))
            all_mach.remove(a)
            all_emp.remove(b)
        emp_tmp = []
        curr_m, curr_e = row[0], row[2]
        if (row[0] in all_mach) & (row[2] in all_emp):
            emp_group = [(row[0], row[2])]
    else:
        if (row[0] in all_mach) & (row[2] in all_emp):
            emp_group.append((row[0], row[2]))
        curr_m, curr_e = row[0], row[2]
    k += 1

columns = ['mode_id', 'm_values', 'emp_id', 'e_values', 'subtraction', 'coef_+', 'coef_-', 'absolute_error']
rows = []

for m, e in sorted(result_pairs):
    print(list(df[(df['mode_id'] == m) & (df['emp_id'] == e)].values[0]))
    rows.append(list(df[(df['mode_id'] == m) & (df['emp_id'] == e)].values[0]))

res_df = pd.DataFrame(rows, columns=columns)
print(res_df[['mode_id', 'emp_id', 'coef_+', 'coef_-']].head())

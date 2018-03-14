import pandas as pd

df1 = pd.read_csv('data/employees.csv', sep='\t', index_col=0)
df2 = pd.read_csv('data/machines.csv', sep='\t', index_col=0)
df1['e_values'] = df1['e_values'].apply(lambda x: [int(d) for d in x[1:-1].split(',')])
df2['m_values'] = df2['m_values'].apply(lambda x: [int(d) for d in x[1:-1].split(',')])

df1 = pd.DataFrame(
    [['emp1', (0, 1, 3)], ['emp2', (2, 2, 4)], ['emp3', (2, 3, 5)]], columns=['empl_id', 'e_values'])
df2 = pd.DataFrame(
    [['mach1', (1, 3, 2)], ['mach2', (3, 3, 1)], ['mach3', (4, 2, 3)]], columns=['mode_id', 'm_values'])

df1['key'] = 0
df2['key'] = 0
df = df2.merge(df1)
df.drop(labels='key', axis=1, inplace=True)

df['subtraction'] = df[['m_values', 'e_values']].apply(
    lambda row: [x - y for x, y in zip(row['e_values'], row['m_values'])], axis=1)

df['coef_+'] = df['subtraction'].apply(lambda x: sum([i for i in x if i > 0]))
df['coef_-'] = df['subtraction'].apply(lambda x: sum([i for i in x if i < 0]))
df['absolute_error'] = df['subtraction'].apply(lambda x: sum([abs(i) for i in x]))

df = df.sort_values(by=['absolute_error', 'coef_-'], ascending=[True, False])
df.reset_index(drop=True, inplace=True)
# df.to_excel('CARTESIAN_PROD.xlsx', index=False)

all_emp = list(df['empl_id'].unique())
all_mach = list(df['mode_id'].unique())

curr_m = df['mode_id'].iloc[0]
curr_e = df['empl_id'].iloc[0]

emp_group = []

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
                emp_indexes = [n for n, x in enumerate(list(df['empl_id'])) if (x == e) & (n >= k)]
                if emp_indexes:
                    emp_tmp.append((m, e, min(emp_indexes)))
        if emp_tmp:
            a, b = sorted(emp_tmp, key=lambda x: x[2], reverse=True)[0][:2]
            # print( sorted(emp_tmp, key=lambda x: x[2], reverse=True))
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

columns = ['mode_id', 'm_values', 'empl_id', 'e_values', 'subtraction', 'coef_+', 'coef_-', 'absolute_error']
rows = []

for m, e in sorted(result_pairs):
    rows.append(list(df[(df['mode_id'] == m) & (df['empl_id'] == e)].values[0]))

res_df = pd.DataFrame(rows, columns=columns)

print(res_df)

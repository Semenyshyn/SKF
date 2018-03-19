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
df = df[['mode_id', 'empl_id', 'absolute_error']].reset_index(drop=True)

df_rows = iter(df.values)
curr = next(df_rows)

all_emp = list(df['empl_id'].unique())
all_mach = list(df['mode_id'].unique())

empl_group = [tuple(curr)]
emp_tmp = []

result_pairs = []

k = 0
while True:
    row = next(df_rows, None)
    if row is None:
        break
    if curr[0] != row[0]:
        # print(empl_group)
        print('====')
        for m, e, error in empl_group:
            if (len(empl_group) == 1) & (m in all_mach) & (e in all_emp):
                result_pairs.append((m, e))
                all_emp.remove(e)
                all_mach.remove(m)
            elif (m in all_mach) & (e in all_emp):
                emp_indexes = [n for n, x in enumerate(list(df['empl_id'])) if (x == e) & (n > k)]
                if emp_indexes:
                    emp_tmp.append((m, e, min(emp_indexes), df['absolute_error'].get_value(min(emp_indexes)) - error))
                    print(emp_tmp)
        # print(empl_group)
        empl_group = [tuple(row)]
        curr = row
    else:
        empl_group.append(tuple(row))
        curr = row
    k += 1

columns = ['mode_id', 'empl_id', 'absolute_error']
rows = []

for m, e in sorted(result_pairs):
    rows.append(list(df[(df['mode_id'] == m) & (df['empl_id'] == e)].values[0]))

res_df = pd.DataFrame(rows, columns=columns)
print(res_df[['mode_id', 'empl_id', 'absolute_error']])

import pandas as pd

# df1 = pd.read_csv('employees.csv', sep='\t', index_col=0)
# df2 = pd.read_csv('machines.csv', sep='\t', index_col=0)
# df1['e_values'] = df1['e_values'].apply(lambda x: [int(d) for d in x[1:-1].split(',')])
# df2['m_values'] = df2['m_values'].apply(lambda x: [int(d) for d in x[1:-1].split(',')])

df1 = pd.DataFrame(
    [['emp1', (0, 1, 3)], ['emp2', (1, 3, 4)], ['emp3', (2, 3, 2)],
     ['emp4', (4, 2, 1)],
     # ['emp5', (2, 3, 3)]
     ],
    columns=['empl_id', 'e_values'])
df2 = pd.DataFrame(
    [['mach1', (1, 3, 2)], ['mach2', (3, 3, 1)], ['mach3', (4, 2, 3)],
     ['mach4', (2, 2, 2)],
     # ['mach5', (1, 3, 1)]
     ],
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

df = df.sort_values(by=['absolute_error'], ascending=[True])
df.reset_index(drop=True, inplace=True)


def remove_pairs(m_v, e_v, df_v):
    df_v = df_v[df_v['empl_id'] != e_v]
    df_v = df_v[df_v['mode_id'] != m_v]
    df_v = df_v[['mode_id', 'empl_id', 'absolute_error']].reset_index(drop=True)
    df_rows_v = iter(df_v.values)
    curr_v = next(df_rows_v, None)
    return df_rows_v, curr_v, df_v.reset_index(drop=True)


df_2 = df[['mode_id', 'empl_id', 'absolute_error']].reset_index(drop=True)

df_rows = iter(df_2.values)
curr = next(df_rows)

mode_group = [tuple(curr)]
group_tmp = []

result_pairs = []

while True:
    row = next(df_rows, None)
    if row is None:
        try:
            a, b = curr[:2]
            result_pairs.append((a, b))
            break
        except:
            break
    if curr[1] != row[1]:
        for m, e, error in mode_group:
            if len(mode_group) == 1:
                result_pairs.append((m, e))
                df_rows, curr, df_2 = remove_pairs(m, e, df_2)
                if len(df_2) == 0:
                    break
                mode_group = [tuple(curr)]
            else:
                e_idxs = [n for n, x in enumerate(list(df_2['mode_id'])) if (x == m)]
                group_tmp.append((m, e, df_2['absolute_error'].get_value(min(e_idxs[1:])) - error))

        if group_tmp:
            a, b = sorted(group_tmp, key=lambda x: -x[2])[0][:2]
            result_pairs.append((a, b))
            df_rows, curr, df_2 = remove_pairs(a, b, df_2)
            mode_group = [tuple(curr)]
            group_tmp = []
    else:
        mode_group.append(tuple(row))
        curr = row

columns = ['mode_id', 'm_values', 'empl_id', 'e_values', 'subtraction', 'coef_+', 'coef_-', 'absolute_error']
rows = []

for m, e in sorted(result_pairs):
    rows.append(list(df[(df['mode_id'] == m) & (df['empl_id'] == e)].values[0]))

res_df = pd.DataFrame(rows, columns=columns)
print('=' * 33)
print(res_df[['mode_id', 'empl_id', 'coef_+', 'coef_-']])

# res_df.to_excel('RESULT_v2_emp.xlsx', index=False)

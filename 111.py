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
empl_group = [(curr[0], curr[1])]

while True:
    row = next(df_rows, None)
    if row is None:
        print(empl_group)
        break
    if curr[0] != row[0]:
        print(empl_group)
        empl_group = [tuple(row)]
        curr = row
    else:
        empl_group.append(tuple(row))
        curr = row

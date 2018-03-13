import pandas as pd
import itertools as it

# df1 = pd.read_csv('data/employees.csv', sep='\t', index_col=0)
# df2 = pd.read_csv('data/machines.csv', sep='\t', index_col=0)
# df1['e_values'] = df1['e_values'].apply(lambda x: [int(d) for d in x[1:-1].split(',')])
# df2['m_values'] = df2['m_values'].apply(lambda x: [int(d) for d in x[1:-1].split(',')])

df1 = pd.DataFrame(
    [['emp1', (0, 1, 3)], ['emp2', (2, 2, 4)], ['emp3', (2, 3, 5)], ['emp4', (1, 1, 2)], ['emp5', (3, 3, 1)]],
    columns=['empl_id', 'e_values'])
df2 = pd.DataFrame(
    [['mach1', (1, 3, 2)], ['mach2', (3, 3, 1)], ['mach3', (4, 2, 3)], ['mach4', (2, 1, 2)], ['mach5', (2, 1, 1)]],
    columns=['mode_id', 'm_values'])

res = None
coef = 10000

k = 0
for i in it.permutations(df1['empl_id']):
    var = list(zip(i, df2['mode_id']))
    df_tmp = pd.DataFrame(var, columns=['empl_id', 'mode_id'])
    df_tmp1 = pd.merge(df_tmp, df1, on='empl_id')
    df = pd.merge(df_tmp1, df2, on='mode_id')
    df['subtraction'] = df[['m_values', 'e_values']].apply(
        lambda row: [x - y for x, y in zip(row['e_values'], row['m_values'])], axis=1)
    df['coef_+'] = df['subtraction'].apply(lambda x: sum([i for i in x if i > 0]))
    df['coef_-'] = df['subtraction'].apply(lambda x: sum([i for i in x if i < 0]))
    s = sum(df['coef_+']) - sum(df['coef_-'])
    if s < coef:
        coef = s
        res = df
    else:
        pass
    k += 1
    if k % 1000 == 0:
        print(k)

print(res)

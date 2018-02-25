import pandas as pd
import itertools as it

df1 = pd.DataFrame([['emp1', (0, 1, 3)], ['emp2', (2, 2, 4)], ['emp3', (2, 3, 5)]], columns=['employees', 'e_values'])
df2 = pd.DataFrame([['mach1', (1, 3, 2)], ['mach2', (3, 3, 1)], ['mach3', (4, 2, 3)]], columns=['machines', 'm_values'])
emp = ['emp1', 'emp2', 'emp3']
mach = ['mach1', 'mach2', 'mach3']

coef = 1000
res = None

for i in it.permutations(emp):
    var = list(zip(i, mach))
    df_tmp = pd.DataFrame(var, columns=['employees', 'machines'])
    df_tmp1 = pd.merge(df_tmp, df1, on='employees')
    df = pd.merge(df_tmp1, df2, on='machines')
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

print(res)
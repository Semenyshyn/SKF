import pandas as pd

df1 = pd.DataFrame([['emp1', (0, 1, 3)], ['emp2', (2, 2, 4)], ['emp3', (2, 3, 5)]], columns=['emp', 'e_values'])
df2 = pd.DataFrame([['mach1', (1, 3, 2)], ['mach2', (3, 3, 1)], ['mach3', (4, 2, 3)]], columns=['mach', 'm_values'])

df1['resource'] = df1['e_values'].apply(lambda x: sum(x))
df2['needs'] = df2['m_values'].apply(lambda x: sum(x))
print(df1)
df1['key'] = 0
df2['key'] = 0
df = df2.merge(df1)
df.drop(labels='key', axis=1, inplace=True)

df['subtraction'] = df[['m_values', 'e_values']].apply(
    lambda row: [x - y for x, y in zip(row['e_values'], row['m_values'])], axis=1)

df['coef_+'] = df['subtraction'].apply(lambda x: sum([i for i in x if i > 0]))
df['coef_-'] = df['subtraction'].apply(lambda x: sum([i for i in x if i < 0]))
df['absolute_error'] = df['subtraction'].apply(lambda x: sum([abs(i) for i in x]))

df['test_c'] = df[['needs', 'resource', 'absolute_error']].apply(
    lambda x: (df1['resource'].sum() - x['resource']) / (df2['needs'].sum() - x['needs']) / x['absolute_error'], axis=1)

df = df.sort_values(by='test_c', ascending=False)

res_list = [df.iloc[0].values]
row = df.iloc[0]

for i in df.values:
    if i[0] not in [x[0] for x in res_list] and i[3] not in [x[3] for x in res_list]:
        res_list.append(i)
        row = i
    else:
        pass

res_df = pd.DataFrame(res_list, columns=df.columns)
# print(res_df)

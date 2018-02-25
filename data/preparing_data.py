import pandas as pd

mm_df = pd.read_csv('data/mm_score.csv', sep='\t')
mm_df = mm_df.drop(['MM_REQ_ID', 'Trainer_OK', 'Update_Date'], axis=1)
mm_df.columns = map(str.lower, mm_df.columns)
mm_df = mm_df.pivot_table(values='req_level', index='mode_id', columns='sill_id').reset_index()
parametrs = mm_df.drop(['mode_id'], axis=1)
names_list = parametrs.columns
mm_df['param'] = parametrs.apply(lambda row: [[row[x] for x in names_list]], axis=1)
mm_df = mm_df[['mode_id', 'param']]
mm_df['param'] = mm_df['param'].apply(lambda x: tuple(x[0]))

staff_df = pd.read_csv('data/staff_score.csv', sep='\t')
staff_df = staff_df.drop(['Score_ID', 'Trainer_OK', 'Update_Date'], axis=1)
staff_df.columns = map(str.lower, staff_df.columns)
staff_df = staff_df.pivot_table(values='score_value', index='empl_id', columns='skill_id').reset_index()
parametrs = staff_df.drop(['empl_id'], axis=1)
names_list = parametrs.columns
staff_df['param'] = parametrs.apply(lambda row: [[row[x] for x in names_list]], axis=1)
staff_df = staff_df[['empl_id', 'param']]
staff_df['param'] = staff_df['param'].apply(lambda x: tuple(x[0]))

staff_df['key'] = 0
mm_df['key'] = 0
df = staff_df.merge(mm_df, on='key')
df.drop(labels='key', axis=1, inplace=True)
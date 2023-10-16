from config import *
import numpy as np

df_old,df_new = read_files(args)
columns_of_interest = [PROFILES_COL,COL_CHANGE_ACTIVITY]

df_old= df_old.drop_duplicates(subset=PROFILES_COL,keep="first")
df_new= df_new.drop_duplicates(subset=PROFILES_COL,keep="last")

#drop line if both old and new activity are NULL
merged_df = df_old[columns_of_interest].merge(df_new[columns_of_interest], on=PROFILES_COL, suffixes=('_old', '_new'), how='inner').replace('none',np.NaN)
merged_df = merged_df.dropna(subset=[COL_CHANGE_ACTIVITY+"_old",COL_CHANGE_ACTIVITY+"_new"], thresh=1)

changed_samples_ids = merged_df.loc[(merged_df[COL_CHANGE_ACTIVITY+'_old'] != merged_df[COL_CHANGE_ACTIVITY+'_new']),PROFILES_COL].drop_duplicates()

df_changed_activity_new = df_new[df_new[PROFILES_COL].isin(changed_samples_ids)]
df_changed_activity_old = df_old[df_old[PROFILES_COL].isin(changed_samples_ids)]

# format the dataframe the good way
activity_df = pd.DataFrame()
activity_df['Nom_complet'] = df_changed_activity_new['Nom d\'exercice'] + ' ' + df_changed_activity_new["Prénom d\'exercice"]
activity_df['Numéro_identification'] = df_changed_activity_new['Identification nationale PP']
activity_df['Code_postal'] = df_changed_activity_new[COL_CHANGE_CODE_POSTAL]
activity_df['Profession'] = df_changed_activity_new['Libellé profession']
activity_df['Spécialité'] = df_changed_activity_new['Libellé savoir-faire']
activity_df['Type_d\'exercice'] = df_changed_activity_new['Code catégorie professionnelle']
activity_df['Ancienne_activité'] = df_changed_activity_old[COL_CHANGE_ACTIVITY].fillna("none")
activity_df['Nouvelle_activité'] = df_changed_activity_new[COL_CHANGE_ACTIVITY].fillna("none")

# export the dataframe
activity_df.to_parquet("changement_activité.parquet", index=False)

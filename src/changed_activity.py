from config import *
import numpy as np

df_old,df_new = read_files()
cols = [PROFILES_COL,COL_CHANGE_ACTIVITY]


df_old= df_old.drop_duplicates(subset=PROFILES_COL,keep="first")
df_new= df_new.drop_duplicates(subset=PROFILES_COL,keep="last")

#drop line if both old and new activity are NULL
merged_df = df_old[cols].merge(df_new, on=PROFILES_COL, suffixes=('_old', '_new'), how='inner').replace('none',np.nan).replace('None',np.nan)
merged_df = merged_df.dropna(subset=[COL_CHANGE_ACTIVITY+"_old",COL_CHANGE_ACTIVITY+"_new"], thresh=1)


changed_samples = merged_df.loc[(merged_df[COL_CHANGE_ACTIVITY+'_old'] != merged_df[COL_CHANGE_ACTIVITY+'_new'])]


# format the dataframe the good way
activity_df = pd.DataFrame()
activity_df['Nom_complet'] = changed_samples['Nom d\'exercice'] + ' ' + changed_samples["Prénom d\'exercice"]
activity_df['Numéro_identification'] = changed_samples['Identification nationale PP']
activity_df['Code_postal'] = changed_samples[COL_CHANGE_CODE_POSTAL]
activity_df['Profession'] = changed_samples['Libellé profession']
activity_df['Spécialité'] = changed_samples['Libellé savoir-faire']
activity_df['Type_d\'exercice'] = changed_samples['Code catégorie professionnelle']
activity_df['Ancienne_activité'] = changed_samples[COL_CHANGE_ACTIVITY+"_old"]
activity_df['Nouvelle_activité'] = changed_samples[COL_CHANGE_ACTIVITY+"_new"]


# export the dataframe
activity_df.to_csv(os.path.join(args.output_rpath,"changement_activité.csv"), index=False)

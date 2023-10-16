from config import *

df_old,df_new = read_files(args)
df_old= df_old.drop_duplicates(subset=PROFILES_COL,keep="first")
df_new= df_new.drop_duplicates(subset=PROFILES_COL,keep="last")


for i,col in enumerate(address_cols):
  if i==0:
    old_add = df_old[col].fillna("").copy().astype("str")
    new_add = df_new[col].fillna("").copy().astype("str")
  else:
    new_add+= " " + df_new[col].fillna("").astype("str")
    old_add+= " " + df_old[col].fillna("").astype("str")

df_old=df_old.drop(address_cols,axis=1)
df_new=df_new.drop(address_cols,axis=1)

df_old["full_address"] = old_add.apply(lambda x:x.strip())
df_new["full_address"] = new_add.apply(lambda x:x.strip())

merged_df = df_old[[PROFILES_COL,"full_address"]].merge(df_new, on=PROFILES_COL, suffixes=('_old', '_new'),how="inner")

changes_mask = (merged_df["full_address_old"] != merged_df["full_address_new"])

changes_df = merged_df[changes_mask].drop_duplicates()

# format the dataframe the good way
address_df = pd.DataFrame()
address_df['Nom_complet'] = changes_df['Nom d\'exercice'] + ' ' + changes_df["Prénom d\'exercice"]
address_df['Numéro_identification'] = changes_df['Identification nationale PP']
address_df['Profession'] = changes_df['Libellé profession']
address_df['Spécialité'] = changes_df['Libellé savoir-faire']
address_df['Type_d\'exercice'] = changes_df['Code catégorie professionnelle']
address_df['Ancienne_adresse'] = changes_df["full_address_old"]
address_df["Nouvelle_adresse"] = changes_df["full_address_new"]


# export the dataframe
address_df.to_csv(os.path.join(args.output_rpath,"changement_adresse.csv"), index=False)
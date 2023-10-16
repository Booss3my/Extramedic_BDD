from config import *
import numpy as np

df_old,df_new = read_files()

# df_old= df_old.drop_duplicates(subset=PROFILES_COL,keep="first")
# df_new= df_new.drop_duplicates(subset=PROFILES_COL,keep="last")


for i,col in enumerate(address_cols):
  if i==0:
    old_add = df_old[col].replace("nan",np.nan).fillna("").copy().astype("str")
    new_add = df_new[col].replace("nan",np.nan).fillna("").copy().astype("str")
  else:
    new_add+= " " + df_new[col].replace("nan",np.nan).fillna("").astype("str")
    old_add+= " " + df_old[col].replace("nan",np.nan).fillna("").astype("str")

df_old=df_old.drop(address_cols,axis=1)
df_new=df_new.drop(address_cols,axis=1)

df_old["full_address"] = old_add.apply(lambda x:x.strip())
df_new["full_address"] = new_add.apply(lambda x:x.strip())


#deleted addresses
deleted_addresses = df_old.replace("",np.nan).dropna(subset=["full_address"]).merge(df_new[[PROFILES_COL,"full_address","Nom d'exercice"]], on=[PROFILES_COL,"full_address"], suffixes=('_old', '_new'),how="left")
deleted_addresses = deleted_addresses.loc[deleted_addresses["Nom d'exercice_new"].isna()]
# format the dataframe the good way
del_address_df = pd.DataFrame()
del_address_df['Nom_complet'] = deleted_addresses['Nom d\'exercice_old'] + ' ' + deleted_addresses["Prénom d\'exercice"]
del_address_df['Numéro_identification'] = deleted_addresses['Identification nationale PP']
del_address_df['Profession'] = deleted_addresses['Libellé profession']
del_address_df['Spécialité'] = deleted_addresses['Libellé savoir-faire']
del_address_df['Type_d\'exercice'] = deleted_addresses['Code catégorie professionnelle']
del_address_df['Adresse_supprimée'] = deleted_addresses["full_address"]

del_address_df.to_csv(os.path.join(args.output_rpath,"addresses_supprimées.csv"), index=False)



#new addresses
new_addresses = df_new.replace("",np.nan).dropna(subset=["full_address"]).merge( df_old[[PROFILES_COL,"full_address","Nom d'exercice"]].replace("",np.nan).dropna(subset=["full_address"]), on=[PROFILES_COL,"full_address"], suffixes=('_new', '_old'),how="left")
#only keep profiles in previous day (to avoid counting completely new professionnals)
new_adds = new_addresses.loc[new_addresses["Nom d'exercice_old"].isna()].merge(df_old[PROFILES_COL].drop_duplicates(),how="inner")
# format the dataframe the good way
new_addresses = pd.DataFrame()
new_addresses['Nom_complet'] = new_adds['Nom d\'exercice_old'] + ' ' + new_adds["Prénom d\'exercice"]
new_addresses['Numéro_identification'] = new_adds['Identification nationale PP']
new_addresses['Profession'] = new_adds['Libellé profession']
new_addresses['Spécialité'] = new_adds['Libellé savoir-faire']
new_addresses['Type_d\'exercice'] = new_adds['Code catégorie professionnelle']
new_addresses['Adresse_ajoutée'] = new_adds["full_address"]
new_addresses.to_csv(os.path.join(args.output_rpath,"nouvelles_addresses.csv"), index=False)


#changed addresses
new_not_found = df_new[[PROFILES_COL,"full_address","Nom d'exercice"]].replace("",np.nan).dropna(subset=["full_address"]).merge(df_old[[PROFILES_COL,"full_address","Nom d'exercice"]].replace("",np.nan).dropna(subset=["full_address"]), on=[PROFILES_COL,"full_address"], suffixes=('_new', '_old'),how="left")
new_not_found = new_not_found.loc[new_not_found["Nom d'exercice_old"].isna()][[PROFILES_COL,"full_address"]]

old_not_found = df_old.replace("",np.nan).dropna(subset=["full_address"]).merge(df_new[[PROFILES_COL,"full_address","Nom d'exercice"]].replace("",np.nan).dropna(subset=["full_address"]), on=[PROFILES_COL,"full_address"], suffixes=('_old', '_new'),how="left")
old_not_found = old_not_found.loc[old_not_found["Nom d'exercice_new"].isna()]
changed_adds = old_not_found.merge(new_not_found,on=PROFILES_COL,how="inner",suffixes=('_old', '_new'))

# format the dataframe the good way
changed_addresses = pd.DataFrame()
changed_addresses['Nom_complet'] = changed_adds['Nom d\'exercice_old'] + ' ' + changed_adds["Prénom d\'exercice"]
changed_addresses['Numéro_identification'] = changed_adds['Identification nationale PP']
changed_addresses['Profession'] = changed_adds['Libellé profession']
changed_addresses['Spécialité'] = changed_adds['Libellé savoir-faire']
changed_addresses['Type_d\'exercice'] = changed_adds['Code catégorie professionnelle']
changed_addresses['Ancienne_adresses'] = changed_adds["full_address_old"]
changed_addresses['Nouvelle_adresse'] = changed_adds["full_address_new"]
# export the dataframe
changed_addresses.to_csv(os.path.join(args.output_rpath,"changement_adresse.csv"), index=False)
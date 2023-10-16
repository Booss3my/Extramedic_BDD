import pandas as pd

cree= pd.read_csv("nouveaux_profils.csv",low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_créé"},axis=1)
supp = pd.read_csv("profils_supprimés.csv",low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_supprimé"},axis=1)
chgt_act = pd.read_csv("changement_activité.csv",low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_chgmt_activité"},axis=1)
chgt_add = pd.read_csv("changement_adresse.csv",low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_chgmt_addresse"},axis=1)


statistics = cree.merge(supp,how="outer",left_index=True,right_index=True)\
.merge(chgt_act,how="outer",left_index=True,right_index=True)\
.merge(chgt_add,how="outer",left_index=True,right_index=True).fillna(0).astype("int")


statistics.loc["Nombre Total"] = statistics.sum()

statistics.to_csv("statistiques.csv",index=False)
import pandas as pd
from config import *

print("\n Création de statistiques ...")


cree= pd.read_csv(os.path.join(args.output_rpath,"nouveaux_profils.csv"),low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_créé"},axis=1)
supp = pd.read_csv(os.path.join(args.output_rpath,"profils_supprimés.csv"),low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_supprimé"},axis=1)
chgt_act = pd.read_csv(os.path.join(args.output_rpath,"changement_activité.csv"),low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_chgmt_activité"},axis=1)
nv_add= pd.read_csv(os.path.join(args.output_rpath,"nouvelles_addresses.csv"),low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_nouvelles_addresses"},axis=1)
del_add= pd.read_csv(os.path.join(args.output_rpath,"addresses_supprimées.csv"),low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_suppression_addresse"},axis=1)
chgt_add = pd.read_csv(os.path.join(args.output_rpath,"changement_adresse.csv"),low_memory=False).groupby("Profession")[["Numéro_identification"]].count().rename({"Numéro_identification": "Nombre_chgmt_addresse"},axis=1)


statistics = cree.merge(supp,how="outer",left_index=True,right_index=True)\
.merge(chgt_act,how="outer",left_index=True,right_index=True)\
.merge(nv_add,how="outer",left_index=True,right_index=True)\
.merge(del_add,how="outer",left_index=True,right_index=True)\
.merge(chgt_add,how="outer",left_index=True,right_index=True).fillna(0).astype("int")


statistics.loc["Nombre Total"] = statistics.sum()

print(statistics)

statistics.to_csv(os.path.join(args.output_rpath,"statistiques.csv"))
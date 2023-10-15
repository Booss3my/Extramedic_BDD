import pandas as pd
import argparse

parser = argparse.ArgumentParser(
                    prog='EM')

parser.add_argument('--old_path', type=str, default="Database/old.txt", help="Path to old data")
parser.add_argument('--new_path', type=str, default="Database/new.txt", help="Path to new data")

args = parser.parse_args()


df_old = pd.read_csv(args.old_path, sep="|", low_memory=False)
df_new = pd.read_csv(args.new_path, sep="|", low_memory=False)



COL_CHANGE_ACTIVITY = "Code secteur d'activité"
PROFILES_COL = "Identification nationale PP"
COL_CHANGE_NUMBER_VOIE = "Numéro Voie (coord. structure)"
COL_CHANGE_TYPE_VOIE = "Code type de voie (coord. structure)"
COL_CHANGE_LIBELLE_VOIE = "Libellé Voie (coord. structure)"
COL_CHANGE_MENTION = "Mention distribution (coord. structure)"
COL_CHANGE_CEDEX = "Bureau cedex (coord. structure)"
COL_CHANGE_CODE_POSTAL = "Code postal (coord. structure)"
COL_CHANGE_CODE_COMMUNE = "Code commune (coord. structure)"
COL_CHANGE_CODE_PAYS = "Code pays (coord. structure)"

address_cols = [
    COL_CHANGE_NUMBER_VOIE, COL_CHANGE_TYPE_VOIE, COL_CHANGE_LIBELLE_VOIE, 
    COL_CHANGE_MENTION, COL_CHANGE_CEDEX, COL_CHANGE_CODE_POSTAL, 
    COL_CHANGE_CODE_COMMUNE, COL_CHANGE_CODE_PAYS
]



#keep only columns of interest (memory)
columns_of_interest =["Identification nationale PP", "Code secteur d'activité",'Nom d\'exercice',"Prénom d\'exercice",'Libellé profession'\
                       ,'Libellé savoir-faire','Code catégorie professionnelle'] + address_cols

df_old = df_old[columns_of_interest]
df_new = df_new[columns_of_interest]
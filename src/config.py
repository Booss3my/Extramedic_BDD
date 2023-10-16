import pandas as pd
import argparse
import os
import sys



Rpath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(Rpath)
sys.path.append(os.path.join(Rpath,"src"))


parser = argparse.ArgumentParser(
                    prog='EM')

parser.add_argument('--old_path', type=str, default="Database/old.txt", help="Path to old data")
parser.add_argument('--new_path', type=str, default="Database/new.txt", help="Path to new data")
parser.add_argument('--ftype', type=str, default="csv", help="input file type")
parser.add_argument('--output_rpath', type=str, default=os.path.join(Rpath,"Output"), help="root to directory where files will be created")
args = parser.parse_args()

arguments_list = [f"--old_path={args.old_path}",f"--new_path={args.new_path}",f"--ftype={args.ftype}",f"--output_rpath={args.output_rpath}"]


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
data_folder = os.path.join(Rpath,"Dataset")

def read_files():
    df_old = pd.read_parquet(os.path.join(data_folder,"old.parquet"))
    df_new = pd.read_parquet(os.path.join(data_folder,"new.parquet"))
    return df_old,df_new
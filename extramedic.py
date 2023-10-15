import sys
import pandas as pd

# Load the data
df_old = pd.read_csv("Database/old.txt", sep="|", low_memory=False)
df_new = pd.read_csv("Database/new.txt", sep="|", low_memory=False)

# Drop the last column
df_old.drop(columns=df_old.columns[-1], inplace=True)
df_new.drop(columns=df_new.columns[-1], inplace=True)

def reformat_dataset(df):
    """
    This function returns a dataframe that only contains relevant information that are:
        - the name
        - the profession
        - the speciality (if there is one)
    """
    new_df = pd.DataFrame()
    new_df['Nom_complet'] = df['Nom d\'exercice'] + ' ' + df["Prénom d\'exercice"]
    new_df['Numéro_identification'] = df['Identification nationale PP']
    new_df['Code_postal'] = df[COL_CHANGE_CODE_POSTAL]
    new_df['Profession'] = df['Libellé profession']
    new_df['Spécialité'] = df['Libellé savoir-faire']
    new_df['Type_d\'exercice'] = df['Code catégorie professionnelle']
    return new_df

def print_loading_bar(percent):
    bar_length = 1
    filled_length = int(bar_length * percent)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r[{bar}] {percent:.1f}%', end='', flush=True)

def append_if_not_present(value, array):
    if value not in array:
        array.append(value)
    return array

def get_occurences(item, dataframe):
    # index = indexes[-1]
    # df = dataframes[0]
    occurences = 0
    occurences += dataframe['Profession'].value_counts().get(item, 0)
    occurences += dataframe['Spécialité'].value_counts().get(item, 0)
    
    return occurences

COL_CHANGE_NUMBER_VOIE = "Numéro Voie (coord. structure)"
COL_CHANGE_TYPE_VOIE = "Code type de voie (coord. structure)"
COL_CHANGE_LIBELLE_VOIE = "Libellé Voie (coord. structure)"
COL_CHANGE_MENTION = "Mention distribution (coord. structure)"
COL_CHANGE_CEDEX = "Bureau cedex (coord. structure)"
COL_CHANGE_CODE_POSTAL = "Code postal (coord. structure)"
COL_CHANGE_CODE_COMMUNE = "Code commune (coord. structure)"
COL_CHANGE_CODE_PAYS = "Code pays (coord. structure)"

"""
Le projet Extramedic

A. Comparaison quotidienne de la base de données. La principale fonctionnalité 
du projet est de comparer la base de données d'hier avec la base de données 
mise à jour du jour pour identifier les changements dans las catégories suivantes:
    1. Nouveau Profil : Les professionnels de la santé qui apparaissent dans la nouvelle base de données mais n'étaient pas présents dans l'ancienne base de données
    2. Profil Supprimé : Les professionnels de la santé qui étaient dans l'ancienne base de données mais ne sont plus présents dans la nouvelle base de données.
    3. Changement d'Activité : Les professionnels de la santé qui ont changé leur type d'activité (employé à indépendant ou vice versa) dans la nouvelle base de données.
    4. Changement de Lieu de Travail : Les professionnels de la santé qui ont changé de lieu de travail dans la nouvelle base de données.

B. Exportation des résultats. Les changements identifiés seront exportés dans des fichiers CSV, organisés par type de profession, facilitant ainsi le suivi des changements pour chaque profession spécifique.
"""

## 1. Nouveau profil
PROFILES_COL = "Identification nationale PP"

profiles_old = df_old.loc[:, PROFILES_COL]
profiles_new = df_new.loc[:, PROFILES_COL]

new_profiles = set(profiles_new) - set(profiles_old)
df_new_profiles = df_new[df_new[PROFILES_COL].isin(new_profiles)]

# format the dataframe the good way
df_new_profiles = reformat_dataset(df_new_profiles)

# export the dataframe
df_new_profiles.to_csv("nouveaux_profils.csv", index=False)

print_loading_bar(20)

## 2. Profil supprimé
merged_df = df_old.merge(df_new, on=PROFILES_COL, how='left', indicator=True)
samples_not_in_df_new = merged_df[merged_df['_merge'] == 'left_only']
samples_not_in_df_new = samples_not_in_df_new.drop(columns='_merge')

deleted_profiles_ids = samples_not_in_df_new['Identification nationale PP'].unique()

df_deleted_profiles = df_old[df_old['Identification nationale PP'].isin(deleted_profiles_ids)]

# format the dataframe the good way
df_deleted_profiles = reformat_dataset(df_deleted_profiles)

# export the dataframe
df_deleted_profiles.to_csv("profils_supprimés.csv", index=False)

print_loading_bar(40)

## 3. Changement d'Activité
COL_CHANGE_ACTIVITY = "Code secteur d'activité"
merged_df = df_old.merge(df_new, on='Identification nationale PP', suffixes=('_old', '_new'), how='inner')

changed_samples = merged_df[merged_df[COL_CHANGE_ACTIVITY+'_old'] != merged_df[COL_CHANGE_ACTIVITY+'_new']]

changed_samples_ids = changed_samples['Identification nationale PP'].unique()

df_changed_activity_new = df_new[df_new['Identification nationale PP'].isin(changed_samples_ids)]
df_changed_activity_old = df_old[df_old['Identification nationale PP'].isin(changed_samples_ids)]

# format the dataframe the good way
# df_changed_activity = reformat_dataset(df_changed_activity)

activity_df = pd.DataFrame()
activity_df['Nom_complet'] = df_changed_activity_new['Nom d\'exercice'] + ' ' + df_changed_activity_new["Prénom d\'exercice"]
activity_df['Numéro_identification'] = df_changed_activity_new['Identification nationale PP']
activity_df['Code_postal'] = df_changed_activity_new[COL_CHANGE_CODE_POSTAL]
activity_df['Profession'] = df_changed_activity_new['Libellé profession']
activity_df['Spécialité'] = df_changed_activity_new['Libellé savoir-faire']
activity_df['Type_d\'exercice'] = df_changed_activity_new['Code catégorie professionnelle']
activity_df['Ancienne_activité'] = df_changed_activity_old[COL_CHANGE_ACTIVITY]
activity_df['Nouvelle_activité'] = df_changed_activity_new[COL_CHANGE_ACTIVITY]

# export the dataframe
activity_df.to_csv("changement_activité.csv", index=False)

print_loading_bar(60)

## 4. Changement de Lieu de Travail
address_cols = [
    COL_CHANGE_NUMBER_VOIE, COL_CHANGE_TYPE_VOIE, COL_CHANGE_LIBELLE_VOIE, 
    COL_CHANGE_MENTION, COL_CHANGE_CEDEX, COL_CHANGE_CODE_POSTAL, 
    COL_CHANGE_CODE_COMMUNE, COL_CHANGE_CODE_PAYS
]

def concatenate_values(row):
    # Convert non-string values to strings before concatenation
    concatenated_values = ' - '.join(str(row[col]) if pd.notna(row[col]) else '' for col in address_cols)
    return concatenated_values

df_old_dropped = df_old.dropna(subset=[
    COL_CHANGE_NUMBER_VOIE, COL_CHANGE_TYPE_VOIE, COL_CHANGE_LIBELLE_VOIE, 
    COL_CHANGE_MENTION, COL_CHANGE_CEDEX, COL_CHANGE_CODE_POSTAL, 
    COL_CHANGE_CODE_COMMUNE, COL_CHANGE_CODE_PAYS
])

df_new_dropped = df_new.dropna(subset=[
    COL_CHANGE_NUMBER_VOIE, COL_CHANGE_TYPE_VOIE, COL_CHANGE_LIBELLE_VOIE, 
    COL_CHANGE_MENTION, COL_CHANGE_CEDEX, COL_CHANGE_CODE_POSTAL, 
    COL_CHANGE_CODE_COMMUNE, COL_CHANGE_CODE_PAYS
])

merged_df = df_old_dropped.merge(df_new_dropped, on='Identification nationale PP', suffixes=('_old', '_new'))

changes_mask = (
    (merged_df[COL_CHANGE_NUMBER_VOIE + '_old'] != merged_df[COL_CHANGE_NUMBER_VOIE + '_new']) |
    (merged_df[COL_CHANGE_TYPE_VOIE + '_old'] != merged_df[COL_CHANGE_TYPE_VOIE + '_new']) |
    (merged_df[COL_CHANGE_LIBELLE_VOIE + '_old'] != merged_df[COL_CHANGE_LIBELLE_VOIE + '_new']) |
    (merged_df[COL_CHANGE_MENTION + '_old'] != merged_df[COL_CHANGE_MENTION + '_new']) |
    (merged_df[COL_CHANGE_CEDEX + '_old'] != merged_df[COL_CHANGE_CEDEX + '_new']) |
    (merged_df[COL_CHANGE_CODE_POSTAL + '_old'] != merged_df[COL_CHANGE_CODE_POSTAL + '_new']) |
    (merged_df[COL_CHANGE_CODE_COMMUNE + '_old'] != merged_df[COL_CHANGE_CODE_COMMUNE + '_new']) |
    (merged_df[COL_CHANGE_CODE_PAYS + '_old'] != merged_df[COL_CHANGE_CODE_PAYS + '_new'])
)

changes_df = merged_df[changes_mask]

address_changed_ids = changes_df['Identification nationale PP'].unique()

df_new_address_changed = df_new[df_new[PROFILES_COL].isin(address_changed_ids)]
df_old_address_changed = df_old[df_old[PROFILES_COL].isin(address_changed_ids)]

# format the dataframe the good way
address_df = pd.DataFrame()
address_df['Nom_complet'] = df_new_address_changed['Nom d\'exercice'] + ' ' + df_new_address_changed["Prénom d\'exercice"]
address_df['Numéro_identification'] = df_new_address_changed['Identification nationale PP']
address_df['Profession'] = df_new_address_changed['Libellé profession']
address_df['Spécialité'] = df_new_address_changed['Libellé savoir-faire']
address_df['Type_d\'exercice'] = df_new_address_changed['Code catégorie professionnelle']
address_df['Ancienne_adresse'] = df_old_address_changed.apply(concatenate_values, axis=1).tolist()
address_df["Nouvelle_adresse"] = df_new_address_changed.apply(concatenate_values, axis=1)

# export the dataframe
address_df.to_csv("changement_adresse.csv", index=False)

print_loading_bar(80)

# 5. Stats sur les 4 CSV
dataframes = [
    df_deleted_profiles,
    df_new_profiles,
    activity_df,
    address_df
]

indexes = []
for dataframe in dataframes:
    for item in dataframe['Profession'].value_counts().index.tolist():
        if item != 'Médecin':
            indexes = append_if_not_present(item, indexes)
    for item in dataframe['Spécialité'].value_counts().index.tolist():
        indexes = append_if_not_present(item, indexes)

data = {}
for index in indexes:
    occurences = [get_occurences(index, dataframe) for dataframe in dataframes]
    data[index] = occurences

df_stats = pd.DataFrame.from_dict(data, orient='index', columns=['Profil supprimé', 'Profil ajouté', 'Changement activité', 'Changement adresse'])

df_stats = df_stats.sort_index()

df_stats.index.name = "Profession"
df_stats.to_csv("statistiques.csv")

print_loading_bar(100)

print("\nFin du traitement des données.")
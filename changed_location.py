from config import *


def concatenate_values(row):
    # Convert non-string values to strings before concatenation
    concatenated_values = ' - '.join(str(row[col]) if pd.notna(row[col]) else '' for col in address_cols)
    return concatenated_values

df_old = df_old.dropna(subset=address_cols)
df_new = df_new.dropna(subset=address_cols)

merged_df = df_old.merge(df_new, on=PROFILES_COL, suffixes=('_old', '_new'),how="inner")

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

changes_df = merged_df[changes_mask].drop_duplicates()


changes_df.merge()
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



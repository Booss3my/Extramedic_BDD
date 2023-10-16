

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


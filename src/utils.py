from config import COL_CHANGE_CODE_POSTAL
import pandas as pd 
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
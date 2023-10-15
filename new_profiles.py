from config import *
from utils import reformat_dataset, print_loading_bar   




profiles_old = df_old.loc[:, PROFILES_COL]
profiles_new = df_new.loc[:, PROFILES_COL]

new_profiles = set(profiles_new) - set(profiles_old)
df_new_profiles = df_new[df_new[PROFILES_COL].isin(new_profiles)]

# format the dataframe the good way
df_new_profiles = reformat_dataset(df_new_profiles)

# export the dataframe
df_new_profiles.to_csv("nouveaux_profils.csv", index=False)

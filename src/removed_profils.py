from config import *
from utils import reformat_dataset,print_loading_bar

df_old,df_new = read_files()

merged_df = df_old[[PROFILES_COL]].merge(df_new[[PROFILES_COL]], on=PROFILES_COL, how='left',indicator=True)
removed_ids = merged_df.loc[merged_df._merge=="left_only",PROFILES_COL].drop_duplicates()

# format the dataframe the good way
df_deleted_profiles = reformat_dataset(df_old.loc[df_old[PROFILES_COL].isin(removed_ids)])

# export the dataframe
df_deleted_profiles.to_csv(os.path.join(args.output_rpath,"profils_supprimés.csv"), index=False)


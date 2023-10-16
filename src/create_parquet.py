from config import * 
import os


#convert data to parquet to make reading a lot faster

print("Creating temporary parquet files for data for faster reading")

if not os.path.exists(data_folder) :
    os.mkdir(data_folder)

    if args.ftype =="csv":
        df_old = pd.read_csv(args.old_path, sep="|", low_memory=False)
        df_new = pd.read_csv(args.new_path, sep="|", low_memory=False)
    elif args.ftype =="parquet":
        df_old = pd.read_parquet(args.old_path)
        df_new = pd.read_parquet(args.new_path)
    else:
        print("Wrong ftype argument")
        exit(1)

    df_old = df_old[columns_of_interest].drop_duplicates()
    df_new = df_new[columns_of_interest].drop_duplicates()


    #convert to string then strip(), to avoid (having categories like "A " and "A")
    for col in df_old.columns:
        if df_old[col].dtype=="object":
            df_old[col] = df_old[col].astype("str").apply(lambda x:x.strip()).astype("str")
            df_new[col] = df_new[col].astype("str").apply(lambda x:x.strip()).astype("str")


df_old.to_parquet(os.path.join(data_folder,"old.parquet"))
df_new.to_parquet(os.path.join(data_folder,"new.parquet"))
import pandas as pd
import datetime as dt
import  seaborn as sns
import numpy as np

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.float_format", lambda x: '%.0f' % x)

# Veriyi Anlama ve Hazırlama

df_ = pd.read_csv("flo_data_20k.csv")
df = df_.copy()
df.head()

df.shape
df.head(10)
df.columns
df.describe().T

df.describe(percentiles=[.50,.60,.70,.80,.95,.99,.999]).T
df.describe().T
df.isnull().sum()

df["order_num_total_ever_online"].value_counts()
df.describe().T

df.info()
df["last_order_channel"].value_counts()
df["order_channel"].value_counts()
df.nunique()
df["order_channel"].value_counts()

df["interested_in_categories_12"].value_counts()

df["total_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_value"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

df.head()

df.info()
df.head()
df["last_order_date_online"].sort_values( ascending=False)
df[["last_order_date_online"]].dtypes

date_col = [col for col in df.columns if "date" in col]

df["last_order_date_online"] = df["last_order_date_online"].astype("datetime64[ns]")

df[date_col] = df[date_col].apply(pd.to_datetime)

df.groupby("order_channel").agg({"total_order":"sum",
                                 "total_value":["sum","count"]
                                    })

df.groupby("master_id").agg({"total_value":"sum"}).sort_values("total_value", ascending=False).head(10)

df.sort_values("total_value", ascending=False).head(10)

df.groupby("master_id").agg({"total_order":"sum"}).sort_values("total_order", ascending=False).head(10)

def data_preprocessing(dataframe):
    #toplam satış sayısını ve toplam satış değerini hesapladığımız kısım
    dataframe["total_order"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["total_value"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    #date içeren değişkenlerin tipini datetime yaptığımız kısım
    date_col = [col for col in df.columns if "date" in col]
    df[date_col] = df[date_col].apply(pd.to_datetime)
    return  dataframe
data_preprocessing(df)

df["interested_in_categories_12"].value_counts()
df[""]

total_categories_expense = df.groupby("interested_in_categories_12")["total_value"].sum().sort_values(
    ascending=False).reset_index().head()

total_categories_expense.head()

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10, 8))
sns.barplot(data=total_categories_expense, x='interested_in_categories_12', y='total_value')
plt.show(block=True)


df.head()
df.info()

today_date = dt.datetime(2021,6,1)

df["last_order_date"].max()
df.info()

rfm = df.groupby("master_id").agg({"last_order_date":lambda last_order_date: (today_date - last_order_date.max()).days,
                             "total_order": lambda frequency: frequency.sum(),
                             "total_value": lambda monetary: monetary.sum()
                                })

rfm.columns = ["recency", "frequency", "monetary"]
rfm.head()
rfm.describe().T

rfm["recency_score"] = pd.qcut(rfm["recency"], 5 , labels=[5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5 , labels=[1,2,3,4,5])

rfm["RF_SCORE"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)

rfm.head()

rfm.info()

seg_map = {
    r'[1-2][1-2]': "hibernating",
    r'[1-2][3-4]': "at_Risk",
    r"[1-2]5": "cant_loose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promising",
    r"51": "new_customer",
    r"[4-5][2-3]": "potential_loyalist",
    r"5[4-5]": "champions"
            }

#rfm1['RFM_score'] = (rfm1['Recency_score'].astype(str)+ rfm1['Frequency_score'].astype(str)+rfm1['Monetary_score'].astype(str) )
seg_map = {
    r'5[1-2][1-2]': 'new_customer',
    r'[1-2][1-2][1-2]': 'lost_segment',
    r'[1-2][3-5][3-5]':'cant_loose',
    r'[2-3][3-4][2-4]': 'awake_segment',
    r'[3-4][3-4][3-4]': 'potential_segment',
    r'[4][4-5][4-5]': 'loyal_segment',
    r'5[4-5][4-5]': 'top_segment'
}

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

rfm.head()

rfm.info()
rfm.groupby("segment").agg(["mean", "count"])

rfm = rfm.reset_index()
rfm_final = rfm.merge(df, on="master_id")
rfm_final.head()


kadin_ayakkabı = rfm_final.loc[(rfm_final["interested_in_categories_12"].str.contains("KADIN")) & ((rfm_final["segment"].str.contains("champions"))| (rfm_final["segment"].str.contains("loyal_customers")))]

risk_cakt_loose = rfm_final.loc[(rfm_final["interested_in_categories_12"].str.contains("KADIN")) & ((rfm_final["segment"].str.contains("cant_loose"))| (rfm_final["segment"].str.contains("at_Risk")))]

erkek = rfm_final.loc[(rfm_final["interested_in_categories_12"].str.contains("ERKEK")) & ((rfm_final["segment"].str.contains("champions"))| (rfm_final["segment"].str.contains("loyal_customers")))]

erkek.info()

risk_cakt_loose.info()

kadin_ayakkabı.info()

kadin_ayakkabı.head()

not_master_id_a = [col for col in kadin_ayakkabı if "master_id" not in col]
kadin_ayakkabı= kadin_ayakkabı.drop(not_master_id_a, axis=1)

kadin_ayakkabı.info()

kadin_ayakkabı.to_csv("kadin_ayakkabı.csv")
kadin_ayakkabı

rfm_final.head()

erkek_cocuk_indirim = rfm_final.loc[(rfm_final["interested_in_categories_12"].str.contains("ERKEK") |
    (rfm_final["interested_in_categories_12"].str.contains("COCUK"))) & ((rfm_final["segment"].str.contains("cant_loose"))|
    (rfm_final["segment"].str.contains("about_to_sleep")) | (rfm_final["segment"].str.contains("new_customer")))]

erkek_cocuk_indirim.info()

not_master_id_b = [col for col in erkek_cocuk_indirim if "master_id" not in col]
erkek_cocuk_indirim = erkek_cocuk_indirim.drop(not_master_id_b, axis=1)

erkek_cocuk_indirim.head()

erkek_cocuk_indirim.to_csv("erkek_cocuk_indirim.csv")

from pathlib import Path
filepath = Path('D:/12thTerm_DS_Bootcamp/3Week_CRM_Analytics/rfm.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
rfm.to_csv(filepath)

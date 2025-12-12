import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_ex_csv(d="sales.csv"):
    df = pd.DataFrame({
                     "date":pd.date_range("2025-01-01",periods=120),
                     "product":["A","B","C","D"]*30,
                     "units":[int(abs(x))for x in (100 + 20 * np.random.randn(120))],
                     "price":[10,15,8,20]*30
                      })
    df.to_csv(d,index=False)
    return d

def pipeline(d="sales.csv"):
    df = pd.read_csv(d, parse_dates=["date"])

    #data cleaning
    df=df.dropna()
    df["units"]=df["units"].astype(int)
    df["revenue"]=df["units"]*df["price"]

    #information: aggregate monthly revenue for product
    df.set_index("date",inplace=True)
    monthly=df.groupby([pd.Grouper(freq='M'),"product"])["revenue"].sum().reset_index()
    pivot = monthly.pivot(index='date',columns='product',values='revenue').fillna(0)
    print("Monthly revenue:\n",pivot.tail())

    #knowledge: detect product with fastest growth (compare last 3 months avg)
    last3 = pivot.tail(3).mean()
    prev3 = pivot.tail(6).head(3).mean()
    growth = ((last3-prev3)/(prev3.replace(0,1))).sort_values(ascending=False)
    print("\ngrowth rates:\n",growth)

    top=growth.idxmax()
    print(f"\nRecommendation: prioritize product {top} (highest recent growth).")

    #visualization
    pivot.plot(kind="line",title="Monthly revenue per product")
    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    d = create_ex_csv()
    pipeline(d)
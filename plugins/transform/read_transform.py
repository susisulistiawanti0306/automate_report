import pandas as pd
import glob
import os

HOME = os.path.expanduser("~")

def __append_all_files(extension, directory):
    all_filenames = [i for i in glob.glob(
        '{directory}/*.{ext}'.format(directory=directory, ext=extension))]
    combined_csv = pd.concat([pd.read_csv(f)
                             for f in all_filenames], ignore_index=True)
    combined_csv.drop(
        combined_csv[combined_csv["Quantity Ordered"] == "Quantity Ordered"].index, inplace=True)

    return combined_csv
def run_transform(group_by):
    data = __append_all_files(
        'csv', 'data/sales_product_data')
    data["total_price"] = data["Quantity Ordered"].astype(
        float) * data["Price Each"].astype(float)
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data.drop(
        data[data["Order Date"].isna()].index, inplace=True)

    if group_by.lower().strip() == 'product':
        data_transformed = data.groupby('Product').agg({"total_price": "sum"}).reset_index()
    elif group_by.lower().strip() == 'month':
        data_transformed = data.groupby(pd.Grouper(key='Order Date', freq='M')).agg({"total_price": "sum"}).reset_index()
    print(data_transformed)
    return data_transformed
if __name__ == '__main__':
    run_transform('product')

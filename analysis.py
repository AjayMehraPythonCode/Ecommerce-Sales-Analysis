import pandas as pd


def run_ecommerce_analysis():
    # --- 1. Load Data ---
    try:
        # Load your main data file 'datacamp_ecommerce.csv'
        df = pd.read_csv('datacamp_ecommerce.csv')
        print("Successfully loaded datacamp_ecommerce.csv.")
    except FileNotFoundError:
        print("Error: 'datacamp_ecommerce.csv' not found. Please place it in the same folder as the script.")
        return

    # --- 2. Rename Columns for Standardization ---
    df.rename(columns={
        'InvoiceNo': 'OrderID',
        'InvoiceDate': 'OrderDate',
        'StockCode': 'ProductID',
        'Description': 'ProductName',
        'UnitPrice': 'UnitPrice'
    }, inplace=True)
    print("Columns have been renamed for consistency.")

    print("\nInitial DataFrame Info:")
    df.info()

    # --- 3. Data Cleaning and Preprocessing ---
    # Remove rows with missing CustomerID, as they are hard to analyze.
    df.dropna(subset=['CustomerID'], inplace=True)

    # Convert CustomerID to an integer type.
    df['CustomerID'] = df['CustomerID'].astype(int)

    # Filter out negative or zero quantities, which could be returns or errors.
    df = df[df['Quantity'] > 0]

    # Filter out items with a price of zero.
    df = df[df['UnitPrice'] > 0]

    print("\nMissing values and invalid records have been handled.")

    # Check for and remove any duplicate rows.
    num_duplicates = df.duplicated().sum()
    if num_duplicates > 0:
        df.drop_duplicates(inplace=True)
        print(f"{num_duplicates} duplicate rows were removed.")

    # Correct the 'OrderDate' data type to datetime for time-series analysis.
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    print("\nData types have been corrected.")

    # --- 4. Feature Engineering (Create New Columns) ---
    # Calculate SalePrice (revenue per transaction line).
    df['SalePrice'] = df['Quantity'] * df['UnitPrice']
    print("'SalePrice' column has been created.")

    # Extract Year and Month for easier filtering and aggregation in Tableau.
    df['OrderYear'] = df['OrderDate'].dt.year
    df['OrderMonth'] = df['OrderDate'].dt.month
    df['YearMonth'] = df['OrderDate'].dt.to_period('M').astype(str)
    print("New date-related columns (Year, Month) have been created.")

    # --- 5. Final Data Export ---
    # Select and reorder columns for the final, clean export file.
    final_columns = [
        'OrderID', 'OrderDate', 'OrderYear', 'OrderMonth', 'YearMonth',
        'CustomerID', 'Country', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'SalePrice'
    ]

    cleaned_df = df[final_columns]

    # Save the cleaned data to a new CSV file.
    cleaned_df.to_csv('cleaned_ecommerce_data.csv', index=False)

    print("\n-------------------------------------------------")
    print("Data cleaning and transformation complete.")
    print("The file 'cleaned_ecommerce_data.csv' is now ready for Tableau.")
    print("-------------------------------------------------")
    print("\nPreview of the final DataFrame:")
    print(cleaned_df.head())


if __name__ == '__main__':
    run_ecommerce_analysis()

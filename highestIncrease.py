import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Read the CSV file with tab delimiter and handling spaces in column names
df = pd.read_csv('data.csv', delimiter='\t', skipinitialspace=True)

# Clean column names
df.columns = df.columns.str.strip()

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# Sort by date
df = df.sort_values('Date')

# Create a list to store weekly results
weekly_results = []

# Group by week
df['Week'] = df['Date'].dt.isocalendar().week
weekly_groups = df.groupby(df['Week'])

for week, group in weekly_groups:
    # Get Monday's data
    monday_data = group[group['Date'].dt.weekday == 0]
    if len(monday_data) == 0:
        continue
    
    monday_open = monday_data['Open'].iloc[0]
    monday_close = monday_data['Close'].iloc[0]
    
    # Get week's highest price
    week_high = group['High'].max()
    
    # Calculate percentage increases
    pct_increase_from_open = ((week_high - monday_open) / monday_open) * 100
    pct_increase_from_close = ((week_high - monday_close) / monday_close) * 100
    
    # Get the date of the highest price
    high_date = group.loc[group['High'] == week_high, 'Date'].iloc[0]
    
    weekly_results.append({
        'Week_Start': group['Date'].iloc[0].strftime('%Y-%m-%d'),
        'Week_End': group['Date'].iloc[-1].strftime('%Y-%m-%d'),
        'Monday_Open': monday_open,
        'Monday_Close': monday_close,
        'Week_High': week_high,
        'High_Date': high_date.strftime('%Y-%m-%d'),
        'Pct_Increase_From_Open': round(pct_increase_from_open, 2),
        'Pct_Increase_From_Close': round(pct_increase_from_close, 2)
    })

# Create DataFrame with results
result_df = pd.DataFrame(weekly_results)

# Export to CSV
result_df.to_csv('result.csv', index=False)

if weekly_results:
    print("\nTop 10 Highest Percentage Increases from Monday Open:")
    print("================================================")
    top_10_open = result_df.nlargest(10, 'Pct_Increase_From_Open')
    for idx, row in top_10_open.iterrows():
        print(f"\nRank {top_10_open.index.get_loc(idx) + 1}:")
        print(f"Week of: {row['Week_Start']}")
        print(f"Percentage Increase: {row['Pct_Increase_From_Open']}%")
        print(f"Monday Open: ${row['Monday_Open']:.2f}")
        print(f"Week High: ${row['Week_High']:.2f}")
        print(f"High reached on: {row['High_Date']}")
    
    print("\nTop 10 Highest Percentage Increases from Monday Close:")
    print("================================================")
    top_10_close = result_df.nlargest(10, 'Pct_Increase_From_Close')
    for idx, row in top_10_close.iterrows():
        print(f"\nRank {top_10_close.index.get_loc(idx) + 1}:")
        print(f"Week of: {row['Week_Start']}")
        print(f"Percentage Increase: {row['Pct_Increase_From_Close']}%")
        print(f"Monday Close: ${row['Monday_Close']:.2f}")
        print(f"Week High: ${row['Week_High']:.2f}")
        print(f"High reached on: {row['High_Date']}")

    # Create summary tables for both metrics
    print("\nSummary Table - Top 10 Increases from Monday Open:")
    print("================================================")
    summary_open = top_10_open[['Week_Start', 'Pct_Increase_From_Open', 'Monday_Open', 'Week_High', 'High_Date']]
    summary_open.index = range(1, 11)
    print(summary_open.to_string())

    print("\nSummary Table - Top 10 Increases from Monday Close:")
    print("================================================")
    summary_close = top_10_close[['Week_Start', 'Pct_Increase_From_Close', 'Monday_Close', 'Week_High', 'High_Date']]
    summary_close.index = range(1, 11)
    print(summary_close.to_string())

else:
    print("No weekly data available for analysis")
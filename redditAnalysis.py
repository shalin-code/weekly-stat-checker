import pandas as pd

# Read the CSV file with tab delimiter and handling spaces in column names
df = pd.read_csv('rklb.csv', delimiter='\t', skipinitialspace=True)

# Clean column names by removing any leading/trailing spaces
df.columns = df.columns.str.strip()

# Convert Date column to datetime, handling the specific date format
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# Sort by date in ascending order
df = df.sort_values('Date')

# Group by week (Monday to Friday)
weekly_groups = df.groupby(pd.Grouper(key='Date', freq='W-FRI'))

# Calculate weekly percentage change
weekly_changes = []
for name, group in weekly_groups:
    if not group.empty:
        week_start_price = group['Close'].iloc[0]
        week_end_price = group['Close'].iloc[-1]
        pct_change = ((week_end_price - week_start_price) / week_start_price) * 100
        weekly_changes.append({
            'Week_Start': group['Date'].iloc[0].strftime('%Y-%m-%d'),
            'Week_End': group['Date'].iloc[-1].strftime('%Y-%m-%d'),
            'Start_Price': week_start_price,
            'End_Price': week_end_price,
            'Percentage_Change': round(pct_change, 2)
        })

# Create DataFrame with weekly changes
result_df = pd.DataFrame(weekly_changes)

# Export to CSV
result_df.to_csv('result.csv', index=False)

# Calculate and print statistics
if weekly_changes:
    avg_change = result_df['Percentage_Change'].mean()
    max_increase = result_df['Percentage_Change'].max()
    max_decrease = result_df['Percentage_Change'].min()

    print(f"Average Weekly Percentage Change: {avg_change:.2f}%")
    print(f"Maximum Weekly Percentage Increase: {max_increase:.2f}%")
    print(f"Maximum Weekly Percentage Decrease: {max_decrease:.2f}%")
else:
    print("No weekly changes calculated - insufficient data")
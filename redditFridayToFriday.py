import pandas as pd

# Read the CSV file with tab delimiter and handling spaces in column names
df = pd.read_csv('rklb.csv', delimiter='\t', skipinitialspace=True)

# Clean column names by removing any leading/trailing spaces
df.columns = df.columns.str.strip()

# Convert Date column to datetime, handling the specific date format
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# Sort by date in ascending order
df = df.sort_values('Date')

# Filter only Fridays
fridays_df = df[df['Date'].dt.weekday == 4]

# Create a list to store the Friday to Friday changes
weekly_changes = []

# Iterate through the Fridays to calculate week-over-week changes
for i in range(len(fridays_df)-1):
    current_friday = fridays_df.iloc[i]
    next_friday = fridays_df.iloc[i+1]
    
    current_price = current_friday['Close']
    next_price = next_friday['Close']
    pct_change = ((next_price - current_price) / current_price) * 100
    
    weekly_changes.append({
        'Start_Friday': current_friday['Date'].strftime('%Y-%m-%d'),
        'End_Friday': next_friday['Date'].strftime('%Y-%m-%d'),
        'Start_Price': current_price,
        'End_Price': next_price,
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

    print("\nWeekly Statistics (Friday-to-Friday):")
    print(f"Average Weekly Percentage Change: {avg_change:.2f}%")
    print(f"Maximum Weekly Percentage Increase: {max_increase:.2f}%")
    print(f"Maximum Weekly Percentage Decrease: {max_decrease:.2f}%")
else:
    print("No Friday-to-Friday changes found in the data")

# Print additional information about the data range
if not fridays_df.empty:
    print(f"\nData Range:")
    print(f"First Friday: {fridays_df['Date'].iloc[0].strftime('%Y-%m-%d')}")
    print(f"Last Friday: {fridays_df['Date'].iloc[-1].strftime('%Y-%m-%d')}")
    print(f"Total number of Fridays: {len(fridays_df)}")
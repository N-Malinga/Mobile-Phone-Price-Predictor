import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler
import pickle

# 1. Load the dataset
df = pd.read_csv('ikman_iphones_full.csv')

# 2. Cleaning Functions
def clean_price(price_str):
    if pd.isna(price_str): return None
    clean_val = re.sub(r'[^\d.]', '', str(price_str))
    try: return float(clean_val)
    except: return None

def clean_size(size_str):
    if pd.isna(size_str): return None
    nums = re.findall(r'\d+', str(size_str))
    if nums:
        val = int(nums[0])
        if 'TB' in str(size_str).upper(): return val * 1024
        return val
    return None

# Apply cleaning
df['Price'] = df['Price'].apply(clean_price)
df['RAM_GB'] = df['RAM'].apply(clean_size)
df['Memory_GB'] = df['Memory'].apply(clean_size)

# Extract Memory from 'Edition' column if Memory column is empty
df['Memory_GB'] = df.apply(lambda r: clean_size(r['Edition']) if pd.isna(r['Memory_GB']) else r['Memory_GB'], axis=1)

# 3. Filtering
# Remove rows where Price or Memory is missing
df = df.dropna(subset=['Price', 'Memory_GB'])

# Keep only iPhone models
df = df[df['Model'].str.contains('iPhone', na=False)]

# 4. Official RAM Specification Mapping (The Knowledge Base)
iphone_ram_map = {
    'iPhone 6': 1, 'iPhone 6 Plus': 1, 'iPhone 6S': 2, 'iPhone SE': 2,
    'iPhone 7': 2, 'iPhone 8': 2, 'iPhone 7 Plus': 3, 'iPhone 8 Plus': 3,
    'iPhone X': 3, 'iPhone XR': 3, 'iPhone XS': 4, 'iPhone 11': 4,
    'iPhone 12': 4, 'iPhone 12 Pro': 6, 'iPhone 13': 4, 'iPhone 13 Pro': 6,
    'iPhone 14': 6, 'iPhone 15': 6, 'iPhone 15 Pro': 8, 'iPhone 16': 8
}

def fill_ram(row):
    if pd.isna(row['RAM_GB']):
        return iphone_ram_map.get(row['Model'], 4) # Default to 4GB if model not in map
    return row['RAM_GB']

df['RAM_GB'] = df.apply(fill_ram, axis=1)

# 5. Outlier Removal (IQR Method)
Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['Price'] >= (Q1 - 1.5 * IQR)) & (df['Price'] <= (Q3 + 1.5 * IQR))]

# 6. Encoding & Scaling
# Encode Condition (Used=1, New=0)
df['Condition_Enc'] = df['Condition'].apply(lambda x: 1 if x == 'Used' else 0)

# One-Hot Encode the 'Model'
df_final = pd.get_dummies(df, columns=['Model'], prefix='Model')

# Scaling RAM and Memory to [0, 1]
scaler = MinMaxScaler()
df_final[['RAM_GB', 'Memory_GB']] = scaler.fit_transform(df_final[['RAM_GB', 'Memory_GB']])

# Save the scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# 7. Final Output
cols_to_keep = ['Price', 'RAM_GB', 'Memory_GB', 'Condition_Enc'] + [c for c in df_final.columns if c.startswith('Model_')]
df_trainable = df_final[cols_to_keep].astype(float)

df_trainable.to_csv('preprocessed_iphones_final.csv', index=False)
print("Preprocessing Complete. Dataset saved as 'preprocessed_iphones_final.csv'")
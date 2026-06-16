import pandas as pd
import os
import sys

#get file path from user
def clean_path(p):
    return p.strip().strip("&").strip().strip("'").strip('"').replace("\\ ", " ").strip()

while True:
    path_a = clean_path(input("drop main file here: "))
    path_b = clean_path(input("drop second file here: "))

    try:
        dfa = pd.read_csv(path_a)
        dfb = pd.read_csv(path_b)
    except Exception as e:
        print(f"error reading files: {e}")
        continue

    if 'SrcCr' not in dfa.columns and 'SrcCr' not in dfb.columns:
        print("error: neither file looks like the main transfer file")
    elif 'Cr' not in dfa.columns and 'Cr' not in dfb.columns:
        print("error: neither file looks like the second transfer file")
    elif 'SrcCr' in dfa.columns and 'SrcCr' in dfb.columns:
        print("error: both files have SrcCr — drop different files")
    elif 'Cr' in dfa.columns and 'Cr' in dfb.columns:
        print("error: both files have Cr — drop different files")
    else:
        break
    
    


if 'SrcCr' in dfa.columns:
    df1, df2 = dfa, dfb
    main_path = path_a
else:
    df1, df2 = dfb, dfa
    main_path = path_b



#read the csv file and calculate the total initial credit, total final credit, initial GPA, and final GPA
pd.set_option('display.max_rows', None)
#print(df1)
valid = df1[pd.to_numeric(df1['SrcCr'], errors='coerce').notna()]
sub_total_initila_cradit_1 = pd.to_numeric(df1['SrcCr'], errors='coerce').sum()
total_final_credit = pd.to_numeric(valid['TgtCr'], errors='coerce').sum()
initial_Pre_GPA_1= (pd.to_numeric(valid['Gr'], errors='coerce') * pd.to_numeric(valid['SrcCr'], errors='coerce')).sum()
final_GPA = (pd.to_numeric(valid['Gr'], errors='coerce') * pd.to_numeric(valid['TgtCr'], errors='coerce')).sum() / total_final_credit

#read the second csv file and calculate the total initial credit and initial GPA
#print(df2)
sub_total_initila_cradit_2 = pd.to_numeric(df2['Cr'], errors='coerce').sum()
initial_Pre_GPA_2= (pd.to_numeric(df2['Gr'], errors='coerce') * pd.to_numeric(df2['Cr'], errors='coerce')).sum()

#calculate the total initial credit and initial GPA
total_initial_credit = sub_total_initila_cradit_1 + sub_total_initila_cradit_2
initial_GPA = (initial_Pre_GPA_1 + initial_Pre_GPA_2) / total_initial_credit

#print the results for debugging
'''
print(f"total initial credit: {total_initial_credit}")
print(f"total final credit: {total_final_credit}")
print(f"final GPA: {final_GPA}")
print(f"initial GPA: {initial_GPA}")
'''

#new dataframe
df3 = pd.DataFrame({
    'Label': ['Initial GPA', 'Final GPA', 'Initial Credits', 'Final Credits'],
    'Value': [initial_GPA, final_GPA, total_initial_credit, total_final_credit]
})

# export
base_name = os.path.splitext(os.path.basename(main_path))[0]
output_path = os.path.join(os.path.dirname(main_path), f'{base_name} - output.xlsx')
with pd.ExcelWriter(output_path) as writer:
    df1.to_excel(writer, sheet_name='Transferred', index=False)
    df2.to_excel(writer, sheet_name='Non-Transferred', index=False)
    df3.to_excel(writer, sheet_name='Summary', index=False)

print(f"saved to: {output_path}")
input("press enter to close...")
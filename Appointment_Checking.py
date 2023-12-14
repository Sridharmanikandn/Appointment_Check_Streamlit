import streamlit as st
import pandas as pd

Transaction_File = st.file_uploader("Upload The Transaction File")
First_xlsx_File = st.file_uploader("Upload The First xlsx file")
Second_xlsx_File = st.file_uploader("Upload The Second xlsx file")

file1 = None
file2 = None

if Transaction_File is not None:
    payment_data = pd.read_csv(Transaction_File)
    status = payment_data.loc[payment_data['Transaction status'] == 'success']
    print("Filtered data by Status only success data...")
    print(status)

    look_for_vals = set(status['Merchant Transaction ID'].tolist())
    print(look_for_vals)
    print(len(look_for_vals))
    
else:
    st.warning("Please upload the Transaction File.")

if First_xlsx_File is not None:
    file1 = pd.read_excel(First_xlsx_File)
else:
    st.warning("Please Upload the First xlxs file")

if Second_xlsx_File is not None:
    file2 = pd.read_excel(Second_xlsx_File)
else:
    st.warning("Please Upload the Second file")


if file1 is not None and file2 is not None:
    merged_data = pd.merge(file1, file2, on=['ReferenceId', 'AppointmentId'], how='outer')

    selected_columns = merged_data[['ReferenceId', 'AppointmentId']]

    selected_columns.to_csv('merged_data.csv', index=False)

    print("Selected columns have been saved as merged_data.csv")

    combined_app_data = pd.read_csv('merged_data.csv')
    mismatch_vals = combined_app_data.loc[combined_app_data["ReferenceId"].isin(look_for_vals)]
    print("Following are Mismatch apps")
    print(mismatch_vals)
    print(len(mismatch_vals))
    if(mismatch_vals.empty):
     st.title("There is not any Mismatch Appointments :smile:")
    else:
     st.title("Following are Mismatch apps")
     st.write(mismatch_vals)
else:
    st.warning("Cannot perform the merge as one or both files are missing.")
    
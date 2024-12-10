import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory


def convert_txt_to_vcast_script(input_file, output_directory, folder_name):
    try:
        # Read the tab-separated data from the .txt file into a DataFrame
        df = pd.read_csv(input_file, sep='\t')

        # Check if required columns are present
        if 'Testcase ID' not in df.columns or 'Branch Name' not in df.columns:
            raise ValueError("Input file must contain 'Testcase ID' and 'Branch Name' columns.")

        # Extract function name from the first Testcase ID
        function_name = df['Testcase ID'].iloc[0].split('.')[0]

        # Create output file path
        output_file = os.path.join(output_directory, f"{function_name}.tst")

        with open(output_file, 'w') as f:
            # Write header info
            f.write("-- VectorCAST 23.sp1 (05/21/23)\n")
            f.write("-- Test Case Script\n--\n")
            f.write(f"-- Environment    : {folder_name.upper()}\n")
            f.write(f"-- Unit(s) Under Test: {folder_name}\n--\n")
            f.write("-- Script Features\n")
            f.write("TEST.SCRIPT_FEATURE:C_DIRECT_ARRAY_INDEXING\n")
            f.write("TEST.SCRIPT_FEATURE:CPP_CLASS_OBJECT_REVISION\n")
            f.write("TEST.SCRIPT_FEATURE:MULTIPLE_UUT_SUPPORT\n")
            f.write("TEST.SCRIPT_FEATURE:REMOVED_CL_PREFIX\n")
            f.write("TEST.SCRIPT_FEATURE:MIXED_CASE_NAMES\n")
            f.write("TEST.SCRIPT_FEATURE:STATIC_HEADER_FUNCS_IN_UUTS\n")
            f.write("TEST.SCRIPT_FEATURE:VCAST_MAIN_NOT_RENAMED\n--\n\n")

            f.write(f"-- Unit: {folder_name}\n-- Subprogram: {function_name}\n\n")

            # Iterate over rows to write test case blocks
            for _, row in df.iterrows():
                test_case = row['Testcase ID']
                branch_note = row['Branch Name'] if pd.notna(row['Branch Name']) else ""

                f.write(f"-- Test Case: {test_case}\n")
                f.write(f"TEST.UNIT:{folder_name}\n")
                f.write(f"TEST.SUBPROGRAM:{function_name}\n")
                f.write("TEST.NEW\n")

                if branch_note:
                    f.write("TEST.NOTES:\n")
                    f.write(f"{branch_note}\n")
                    f.write("TEST.END_NOTES:\n")

                f.write(f"TEST.NAME:{test_case}\n")

                for col in df.columns:
                    input_value = row[col] if pd.notna(row[col]) else ''
                    if col.startswith('STUB') and input_value:
                        f.write(f"TEST.STUB:{folder_name}.{input_value.strip()}\n")
                    elif '=' in col:
                        variable_name = col.split('=')[-1].strip()
                        f.write(f"TEST.VALUE:uut_prototype_stubs.{variable_name}:{input_value}\n")
                    elif col not in ['Testcase ID', 'Branch Name']:
                        if input_value:
                            f.write(f"TEST.VALUE:{folder_name}.<<GLOBAL>>.{col}:{input_value}\n")

                f.write("TEST.END\n\n")

        print(f"Converted data written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Create a Tkinter root window (hidden)
    root = Tk()
    root.withdraw()

    # Ask for input and output directories
    input_directory = askdirectory(title="Select Input Directory")
    if not input_directory:
        print("No input directory selected. Exiting.")
        return

    output_directory = askdirectory(title="Select Output Directory")
    if not output_directory:
        print("No output directory selected. Exiting.")
        return

    folder_name = os.path.basename(input_directory)

    # Process all .txt files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_directory, filename)
            convert_txt_to_vcast_script(input_file, output_directory, folder_name)


if __name__ == "__main__":
    main()

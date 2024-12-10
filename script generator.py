import os

def generate_final_script():
    import tkinter as tk
    from tkinter import filedialog

    # Initialize dialog
    tk.Tk().withdraw()

    # Ask for folder location
    folder_path = filedialog.askdirectory(title="Select Folder Containing Test Scripts")
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    # Extract folder name details
    folder_name = os.path.basename(folder_path)
    environment_name = folder_name.upper()
    unit_under_test_name = folder_name
    unit_name = folder_name

    # Collect all `.tst` files in the folder
    tst_files = [f for f in os.listdir(folder_path) if f.endswith('.tst')]
    if not tst_files:
        print("No .tst files found in the selected folder. Exiting.")
        return

    # Ask for save location
    save_location = filedialog.asksaveasfilename(
        title="Save Consolidated Test Script",
        defaultextension=".tst",
        filetypes=[("Test Script Files", "*.tst")]
    )
    if not save_location:
        print("No save location specified. Exiting.")
        return

    # Script Features (static for now)
    script_features = [
        "C_DIRECT_ARRAY_INDEXING",
        "CPP_CLASS_OBJECT_REVISION",
        "MULTIPLE_UUT_SUPPORT",
        "REMOVED_CL_PREFIX",
        "MIXED_CASE_NAMES",
        "STATIC_HEADER_FUNCS_IN_UUTS",
        "VCAST_MAIN_NOT_RENAMED",
    ]

    # Start building the consolidated script
    consolidated_script = []
    consolidated_script.append("-- VectorCAST 23.sp1 (05/21/23)")
    consolidated_script.append("-- Test Case Script")
    consolidated_script.append("--")
    consolidated_script.append(f"-- Environment    : {environment_name}")
    consolidated_script.append(f"-- Unit(s) Under Test: {unit_under_test_name}")
    consolidated_script.append("--")
    consolidated_script.append("-- Script Features")
    for feature in script_features:
        consolidated_script.append(f"TEST.SCRIPT_FEATURE:{feature}")
    consolidated_script.append("--")
    consolidated_script.append(f"-- Unit: {unit_name}")
    consolidated_script.append("")  # Leave one space between the features and the subprograms

    # Process each `.tst` file
    seen_subprograms = set()  # To track and avoid duplicate subprograms
    for tst_file in tst_files:
        tst_path = os.path.join(folder_path, tst_file)
        with open(tst_path, 'r') as file:
            lines = file.readlines()

        # Extract subprogram name
        subprogram_name = tst_file.split('.')[0]
        if subprogram_name not in seen_subprograms:
            consolidated_script.append(f"-- Subprogram: {subprogram_name}")
            seen_subprograms.add(subprogram_name)

        # Add test case details
        for line in lines:
            stripped_line = line.strip()
            # Exclude unnecessary headers and repeated subprogram names
            if not (stripped_line.startswith("-- VectorCAST") or
                    stripped_line.startswith("-- Test Case Script") or
                    stripped_line.startswith("-- Environment") or
                    stripped_line.startswith("-- Unit(s) Under Test") or
                    stripped_line.startswith("-- Script Features") or
                    stripped_line.startswith("TEST.SCRIPT_FEATURE") or
                    stripped_line.startswith("-- Unit") or
                    stripped_line.startswith("-- Subprogram")):
                # Append non-empty lines directly
                if stripped_line:
                    consolidated_script.append(stripped_line)
        consolidated_script.append("")  # Ensure separation after each test case (if needed)

    # Save the consolidated script
    with open(save_location, 'w') as output_file:
        output_file.write("\n".join(consolidated_script).strip() + "\n")  # Remove trailing blank lines

    print(f"Consolidated script saved at {save_location}.")

# Run the script generator
generate_final_script()

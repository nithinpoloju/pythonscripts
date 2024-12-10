import os

def split_txt_file(input_file_content, output_directory):
    try:
        lines = input_file_content.splitlines()

        # Initialize variables
        current_header = None
        current_data = []
        function_name = None
        os.makedirs(output_directory, exist_ok=True)

        for line in lines:
            # Check if the line contains a header (starts with 'Testcase ID')
            if line.strip().startswith('Testcase ID'):
                # Write the previous section to a file
                if current_data and function_name:
                    output_file = os.path.join(output_directory, f"{function_name}.txt")
                    with open(output_file, 'w') as f:
                        f.write(current_header + '\n' + '\n'.join(current_data))

                # Reset for the new section
                current_header = line
                current_data = []
                function_name = None

            # Check if the line contains a function name (starts with a prefix like 'Vent_')
            elif line.strip() and not current_header:
                raise ValueError("File format is incorrect. A header is expected before data rows.")

            elif current_header and not function_name:
                # Extract the function name from the first 'Testcase ID'
                function_name = line.split('.')[0]
                current_data.append(line)

            else:
                current_data.append(line)

        # Write the last section to a file
        if current_data and function_name:
            output_file = os.path.join(output_directory, f"{function_name}.txt")
            with open(output_file, 'w') as f:
                f.write(current_header + '\n' + '\n'.join(current_data))

        print(f"Split completed! Files saved in {output_directory}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main(input_file_content, output_directory):
    # Split the .txt file
    split_txt_file(input_file_content, output_directory)

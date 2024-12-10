async function loadPyodideAndRunWithArgs(scriptName, args) {
    try {
        const pyodide = await loadPyodide();
        const pythonCode = await fetchPythonScript(scriptName);
        if (pythonCode) {
            pyodide.runPython(pythonCode);
            pyodide.globals.set("args", args);
            await pyodide.runPython(`
import sys
sys.argv = [scriptName] + args
exec(open(scriptName).read())
`);
        }
    } catch (error) {
        console.error(`Error running Python script (${scriptName}):`, error);
    }
}

async function selectFilesAndRunScript(scriptName) {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt"; // Allow only .txt files
    fileInput.multiple = true; // Allow selecting multiple files

    fileInput.addEventListener("change", async () => {
        const files = Array.from(fileInput.files);
        if (files.length === 0) {
            alert("No .txt files selected!");
            return;
        }

        // Prompt the user for save location
        const saveLocation = prompt("Enter the save location (output directory):");
        if (!saveLocation) {
            alert("No save location provided!");
            return;
        }

        // Collect file paths for processing
        const filePaths = files.map(file => file.name); // Using file names for simplicity
        await loadPyodideAndRunWithArgs(scriptName, [saveLocation, ...filePaths]);
    });

    fileInput.click(); // Trigger file input dialog
}

function bindButtonToScript(buttonId, scriptName) {
    document.getElementById(buttonId).addEventListener("click", () => {
        selectFilesAndRunScript(scriptName);
    });
}

// Bind buttons to their respective scripts
bindButtonToScript("button1", "Folder_of_Txt_files_to_VCAST_Script_with_stubbed_funs_with_loc_var_and_stub.py");
bindButtonToScript("button2", "script_generator.py");
bindButtonToScript("button3", "text_file_generator.py");

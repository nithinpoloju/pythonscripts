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

async function processFolderAndRunScript(scriptName) {
    const folderInput = document.createElement("input");
    folderInput.type = "file";
    folderInput.webkitdirectory = true; // Allow folder selection

    folderInput.addEventListener("change", async () => {
        const files = Array.from(folderInput.files);
        const txtFiles = files.filter(file => file.name.endsWith(".txt"));

        if (txtFiles.length === 0) {
            alert("No .txt files found in the selected folder!");
            return;
        }

        // Extract the folder path from the first file's relative path
        const folderPath = txtFiles[0]?.webkitRelativePath?.split('/')[0];
        if (!folderPath) {
            alert("No folder selected!");
            return;
        }

        // Prompt the user for save location
        const saveLocation = prompt("Enter the save location (output directory):");
        if (!saveLocation) {
            alert("No save location provided!");
            return;
        }

        // Pass the folder path and save location to the script
        const txtFilePaths = txtFiles.map(file => file.webkitRelativePath);
        await loadPyodideAndRunWithArgs(scriptName, [folderPath, saveLocation, ...txtFilePaths]);
    });

    folderInput.click();
}

function bindButtonToScript(buttonId, scriptName) {
    document.getElementById(buttonId).addEventListener("click", () => {
        processFolderAndRunScript(scriptName);
    });
}

// Bind buttons to their respective scripts
bindButtonToScript("button1", "Folder_of_Txt_files_to_VCAST_Script_with_stubbed_funs_with_loc_var_and_stub.py");
bindButtonToScript("button2", "script_generator.py");
bindButtonToScript("button3", "text_file_generator.py");

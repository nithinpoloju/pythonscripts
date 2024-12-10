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

async function runScriptWithFolder(scriptName) {
    // Create and simulate a file input element to select a folder
    const folderInput = document.createElement("input");
    folderInput.type = "file";
    folderInput.webkitdirectory = true; // Allow folder selection
    folderInput.addEventListener("change", async () => {
        const folderPath = Array.from(folderInput.files)[0]?.webkitRelativePath?.split('/')[0];
        if (!folderPath) {
            alert("No folder selected!");
            return;
        }

        // Prompt the user for save location
        const saveLocation = prompt("Enter the save location (including file name):");
        if (!saveLocation) {
            alert("No save location provided!");
            return;
        }

        // Run the specified Python script with the folder path and save location
        await loadPyodideAndRunWithArgs(scriptName, [folderPath, saveLocation]);
    });

    folderInput.click(); // Simulate a click to open the folder selection dialog
}

function bindButtonToScript(buttonId, scriptName) {
    document.getElementById(buttonId).addEventListener("click", () => {
        runScriptWithFolder(scriptName);
    });
}

// Bind buttons to their respective scripts
bindButtonToScript("button1", "Folder_of_Txt_files_to_VCAST_Script_with_stubbed_funs_with_loc_var_and_stub.py");
bindButtonToScript("button2", "script_generator.py");
bindButtonToScript("button3", "text_file_generator.py");

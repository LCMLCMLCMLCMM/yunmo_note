Set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

currentFolder = fso.GetParentFolderName(WScript.ScriptFullName)

parentFolder = fso.GetParentFolderName(currentFolder)

runFolder = fso.BuildPath(parentFolder, "run")

WshShell.CurrentDirectory = parentFolder

WshShell.Run "python\python313\python -m run\runyunmo.py", 0, True
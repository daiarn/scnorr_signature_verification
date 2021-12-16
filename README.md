# scnorr_signature_verification
Scnorr Signature Verification Desktop app

# Steps to Create an Executable from Python Script using Pyinstaller

* Step 1: Install the Pyinstaller Package
In the Windows Command Prompt, type the following command to install the pyinstaller package (and then press Enter):
```
pip install pyinstaller
```

* Step 2: Create the Executable using Pyinstaller
Simply go to the Command Prompt, and then type: cd followed by the location where your Python script is stored. In my case, I typed the following in the command prompt:
```
cd C:\Users\User\Desktop\MyPython
```
Next, use the following template to create the executable:
```
pyinstaller --onefile main.py
```

* Step 3: Run the Executable
our executable should now get created at the location that you specified.
In my case, I went back to the location where I originally stored the ‘main’ script (C:\Users\User\Desktop\MyPython). Few additional files got created at that location. To find the executable file, open the dist folder.

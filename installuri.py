# light script to help you register xdg-open with novetusuri.exe
import sys
import os
from pathlib import Path

class NovetusURIReg:
    def __init__(self):
        self.appPath = str(Path.home()) + "/.local/share/applications/"
        self.fName = "NovetusURI.desktop"

        if os.geteuid() == 0:
            result = self.inputWaiter("This is NOT recommended to run as root. Are you sure you want to continue?", yesnoPrompt=True)
            if result == "no": sys.exit(0)
        

        if os.path.exists(self.appPath + self.fName):
            result = self.inputWaiter(f"It seems there already is a {self.fName} file in: {self.appPath}\nWould you like to overwrite it?", yesnoPrompt=True)
            if result == "no": sys.exit(0)

        arg = "Please enter your Novetus install directory"
        self.installDir = self.inputWaiter(arg, exitAllowed=True)
        if not self.installDir.endswith("/"):
            self.installDir += "/"

        arg = "If you use a custom wine install, please type the location to the binary. If not, please just press enter."
        self.wineLoc = self.inputWaiter(arg)
        if self.wineLoc == "":
            self.wineLoc = "wine"


        self.run()


    def inputWaiter(self, message, exitAllowed=False, yesnoPrompt=False):
        if exitAllowed:
            message += " (type 'exit' to exit)"
        if yesnoPrompt:
            message += " (answer yes / no)"

        while True:
            print(message)
            result = input("> ")

            if exitAllowed and result.lower() == "exit":
                sys.exit(0)
            
            if yesnoPrompt:
                if result == "no" or result == "yes":
                    return result
                else:
                    continue
            
            return result


    def registerXDG(self):
        cmd = "xdg-mime default NovetusURI.desktop x-scheme-handler/novetus"
        print("Associating NovetusURI.desktop with novetus:// using the command:\n" + cmd)
        os.system(cmd)
        print("Done")

    
    def createFile(self):
        '''Creates a .desktop file for the URI launcher.'''
        print(f"\nCreating file: {self.appPath}{self.fName}")

        # Very good looking
        fileCon = f"""[Desktop Entry]
Type=Application
Name=Novetus URI Launcher
Comment=Launch Novetus with a URI string
Terminal=false
Icon={self.installDir}NovetusIcon.ico
StartupNotify=false
Exec={self.wineLoc} {self.installDir}bin/NovetusURI.exe %U
"""
        with open(f"{self.appPath}{self.fName}", "w") as f:
            f.write(fileCon)

        print("Done writing file\n")


    def run(self):
        self.createFile()
        self.registerXDG()


if __name__ == "__main__":
    NUR = NovetusURIReg()

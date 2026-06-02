import subprocess
import os


class RTKLIBService:

    def __init__(self):

        self.process = None

    def start_strsvr(self):

        exe_path = os.path.join(
            "rtklib",
            "strsvr.exe"
        )

        self.process = subprocess.Popen(

            [exe_path],

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE
        )

        print("STRSVR INICIADO")

    def stop_strsvr(self):

        if self.process:

            self.process.terminate()

            self.process = None

            print("STRSVR DETENIDO")
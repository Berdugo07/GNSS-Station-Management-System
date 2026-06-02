import os

from PySide6.QtCore import (
    QProcess,
    QFileSystemWatcher
)

processes = {}


class RTKLIBManager:

    def __init__(self, log_callback=None):

        self.log_callback = log_callback

        self.trace_watcher = QFileSystemWatcher()

        self.trace_watcher.fileChanged.connect(
            self.read_trace
        )

        self.trace_file = "str2str.trace"

    def start_stream(
            self,
            name,
            input_stream,
            output_stream,
            messages="",
            lat="",
            lon="",
            height=""
     ):

        process = QProcess()

        exe_path = os.path.abspath(
            "rtklib/str2str.exe"
        )

        self.log(
            f"EXE: {exe_path}"
        )

        self.log(
            f"EXISTE EXE: {os.path.exists(exe_path)}"
        )

        args = [

            "-in",
            input_stream,

            "-out",
            output_stream
        ]

        # ==========================
        # MENSAJES RTCM
        # ==========================

        if messages:

            args.extend([

                "-msg",
                messages

            ])

        # ==========================
        # POSICIÓN BASE
        # ==========================

        if lat and lon and height:

            args.extend([

                "-p",
                lat,
                lon,
                height

            ])

        self.log(
            f"INICIANDO: {exe_path}"
        )

        command = " ".join(args)

        self.log(
            f"COMANDO: {command}"
        )

        process.setProgram(exe_path)

        process.setArguments(args)

        process.readyReadStandardOutput.connect(

            lambda: self.read_stdout(
                process
            )
        )

        process.readyReadStandardError.connect(

            lambda: self.read_stderr(
                process
            )
        )

        process.start()

        process.waitForStarted()

        self.log(
         f"ERROR STRING: {process.errorString()}"
        )

        state = process.state()     

        self.log(
            f"STATE: {state}"
        )

        if state == QProcess.Running:

            self.log(
                "STR2STR INICIADO CORRECTAMENTE"
            )

        else:

            self.log(
                "ERROR AL INICIAR STR2STR"
            )

        processes[name] = process

        self.log(
            f"{name} iniciado"
        )

        if os.path.exists(self.trace_file):

            if self.trace_file not in self.trace_watcher.files():

                self.trace_watcher.addPath(
                    self.trace_file
                )

    def stop_stream(self, name):

        if name in processes:

            processes[name].kill()

            processes[name].waitForFinished()

            del processes[name]

            self.log(
                f"{name} detenido"
            )

    def read_trace(self):

        try:

            if not os.path.exists(
                self.trace_file
            ):
                return

            with open(

                self.trace_file,
                "r",
                encoding="utf-8",
                errors="ignore"

            ) as f:

                text = f.read()

            if text.strip():

                self.log(text)

        except Exception as e:

            print(
                f"ERROR TRACE: {e}"
            )
    
    def read_stdout(self, process):

        try:

            data = process.readAllStandardOutput()

            text = bytes(data).decode(

                "utf-8",
                errors="ignore"

            )

            if text.strip():

                self.log(text)

        except Exception as e:

            self.log(
                f"STDOUT ERROR: {e}"
            )
            
    def read_stderr(self, process):

        try:

            data = process.readAllStandardError()

            text = bytes(data).decode(

                "utf-8",
                errors="ignore"

            )

            if text.strip():

                self.log(text)

        except Exception as e:

            self.log(
                f"STDERR ERROR: {e}"
            )

    def log(self, text):

        print(text)

        if self.log_callback:

            self.log_callback(text)
import socket
import threading
import base64
from datetime import datetime
import json

from config import SETTINGS
from database import load_users


# =========================
# SETTINGS
# =========================

NTRIP_PORT = SETTINGS["ntrip_port"]

API_PORT = SETTINGS["api_port"]


# =========================
# MOUNTPOINTS
# =========================

MOUNTPOINTS = {}

for name, data in SETTINGS["mountpoints"].items():

    MOUNTPOINTS[name] = {

        "host": data["ip"],

        "port": data["port"]
    }


# =========================
# ONLINE USERS
# =========================

active_connections = []


# =========================
# VALIDATE USER
# =========================

def validate_user(

    username,
    password,
    mountpoint
):

    try:

        users = load_users()

        for user in users:

            if str(user["username"]) != str(username):

                continue

            # PASSWORD

            if str(user["password"]) != str(password):

                print("PASSWORD INCORRECTO")

                return False

            # MOUNTPOINTS

            allowed_mountpoints = str(

                user["mountpoints"]

            ).split(",")

            allowed_mountpoints = [

                mp.strip()

                for mp in allowed_mountpoints
            ]

            if mountpoint not in allowed_mountpoints:

                print("MOUNTPOINT DENEGADO")

                return False

            # ACTIVO

            if not user.get("active", False):

                print("USUARIO INACTIVO")

                return False

            # FECHA EXPIRACIÓN

            expire_date = datetime.strptime(

                user["expire_date"],
                "%Y-%m-%d"

            ).date()

            if datetime.now().date() > expire_date:

                print("USUARIO EXPIRADO")

                return False

            return True

        print("USUARIO NO EXISTE")

        return False

    except Exception as e:

        print("ERROR VALIDATE USER:", e)

        return False


# =========================
# SOURCETABLE
# =========================

def build_sourcetable():

    table = "SOURCETABLE 200 OK\r\n"

    for mp in MOUNTPOINTS:

        table += (

            f"STR;{mp};{mp};RTCM 3.0;"
            f"1004(1),1005(10);"
            f"2;GPS;GSI;BOLIVIA;0;0;"
            f"1;1;GSI;none;B;N;0;\r\n"
        )

    table += "ENDSOURCETABLE\r\n"

    return table.encode()


# =========================
# API ONLINE USERS
# =========================

def api_online_server():

    api_server = socket.socket(

        socket.AF_INET,
        socket.SOCK_STREAM
    )

    api_server.setsockopt(

        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    api_server.bind(

        ("127.0.0.1", API_PORT)
    )

    api_server.listen(10)

    print(f"API ONLINE USERS : {API_PORT}")

    while True:

        client, addr = api_server.accept()

        try:

            users = []

            for user in active_connections:

                users.append({

                    "username": user["username"],

                    "ip": user["ip"],

                    "mountpoint": user["mountpoint"],

                    "connected_at": str(
                        user["connected_at"]
                    )
                })

            data = json.dumps(users)

            client.sendall(
                data.encode()
            )

        except Exception as e:

            print("ERROR API:", e)

        finally:

            client.close()


# =========================
# CLIENT HANDLER
# =========================

def handle_client(

    client_socket,
    addr
):

    client_data = None

    rtcm_socket = None

    try:

        request = client_socket.recv(
            4096
        ).decode(
            errors="ignore"
        )

        print("\n====================")
        print("NUEVO CLIENTE")
        print("====================")

        first_line = request.split(
            "\r\n"
        )[0]

        print(first_line)

        # =========================
        # SOURCETABLE
        # =========================

        if "GET / HTTP" in request:

            print("Enviando SOURCETABLE")

            client_socket.sendall(

                build_sourcetable()
            )

            client_socket.close()

            return

        # =========================
        # AUTH
        # =========================

        auth_line = ""

        for line in request.split("\r\n"):

            if "Authorization:" in line:

                auth_line = line

        if not auth_line:

            print("SIN AUTENTICACION")

            client_socket.close()

            return

        encoded = auth_line.split(" ")[2]

        decoded = base64.b64decode(
            encoded
        ).decode()

        username, password = decoded.split(":")

        mountpoint = first_line.split(" ")[1]

        mountpoint = mountpoint.replace("/", "")

        print("Usuario:", username)

        print("Mountpoint:", mountpoint)

        # =========================
        # VALIDATE
        # =========================

        valid = validate_user(

            username,
            password,
            mountpoint
        )

        if not valid:

            print("ACCESO DENEGADO")

            client_socket.send(

                b"HTTP/1.1 401 Unauthorized\r\n\r\n"
            )

            client_socket.close()

            return

        print("ACCESO PERMITIDO")

        # =========================
        # ONLINE USERS
        # =========================

        client_data = {

            "username": username,

            "ip": addr[0],

            "mountpoint": mountpoint,

            "connected_at": datetime.now()
        }

        active_connections.append(
            client_data
        )

        print(
            f"ONLINE USERS: {len(active_connections)}"
        )

        # =========================
        # RESPONSE
        # =========================

        client_socket.send(

            b"ICY 200 OK\r\n\r\n"
        )

        # =========================
        # RTCM CONNECT
        # =========================

        rtklib_ip = MOUNTPOINTS[mountpoint]["host"]

        rtklib_port = MOUNTPOINTS[mountpoint]["port"]

        rtcm_socket = socket.socket(

            socket.AF_INET,
            socket.SOCK_STREAM
        )

        rtcm_socket.connect(

            (rtklib_ip, rtklib_port)
        )

        print(
            f"Conectado RTCM {rtklib_port}"
        )

        # =========================
        # STREAM
        # =========================

        while True:

            data = rtcm_socket.recv(4096)

            if not data:

                print("RTCM DESCONECTADO")

                break

            client_socket.sendall(data)

    except Exception as e:

        print("ERROR CLIENT:", e)

    finally:

        # =========================
        # REMOVE ONLINE USER
        # =========================

        if client_data:

            try:

                if client_data in active_connections:

                    active_connections.remove(
                        client_data
                    )

                    print(
                        f"ONLINE USERS: {len(active_connections)}"
                    )

            except Exception as e:

                print(
                    "ERROR REMOVE USER:",
                    e
                )

        # =========================
        # CLOSE RTCM
        # =========================

        try:

            if rtcm_socket:

                rtcm_socket.close()

        except:
            pass

        # =========================
        # CLOSE CLIENT
        # =========================

        try:

            client_socket.close()

        except:
            pass


# =========================
# START SERVER
# =========================

def start_server():

    threading.Thread(

        target=api_online_server,

        daemon=True

    ).start()

    server = socket.socket(

        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(

        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(

        ("0.0.0.0", NTRIP_PORT)
    )

    server.listen(50)

    print("========================")
    print("GSI NTRIP CASTER")
    print("========================")

    print(f"NTRIP PORT : {NTRIP_PORT}")

    while True:

        client_socket, addr = server.accept()

        print(f"\nCLIENTE {addr}")

        client_thread = threading.Thread(

            target=handle_client,

            args=(client_socket, addr),

            daemon=True
        )

        client_thread.start()


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    start_server()
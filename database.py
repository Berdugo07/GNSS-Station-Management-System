import json
import os


# =========================
# APP DATA DIRECTORY
# =========================

BASE_DIR = os.path.join(

    os.path.expanduser("~"),

    "AppData",
    "Roaming",
    "GSI_NTRIP"
)

if not os.path.exists(BASE_DIR):

    os.makedirs(BASE_DIR)

print(BASE_DIR)

USERS_FILE = os.path.join(

    BASE_DIR,

    "users.json"
)


# =========================
# CREAR JSON SI NO EXISTE
# =========================

if not os.path.exists(USERS_FILE):

    with open(USERS_FILE, "w", encoding="utf-8") as f:

        json.dump([], f, indent=4)


# =========================
# LEER JSON
# =========================

def load_users():

    try:

        with open(USERS_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except:

        return []


# =========================
# GUARDAR JSON
# =========================

def save_users(users):

    with open(USERS_FILE, "w", encoding="utf-8") as f:

        json.dump(

            users,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================
# OBTENER TODOS
# =========================

def get_users():

    try:

        users = load_users()

        result = []

        for user in users:

            result.append((

                user["username"],
                user["fullname"],
                user["phone"],
                user["mountpoints"],
                user["expire_date"],
                user["active"]
            ))

        return result

    except Exception as e:

        print("ERROR get_users:", e)

        return []


# =========================
# OBTENER USUARIO
# =========================

def get_user(username):

    try:

        users = load_users()

        for user in users:

            if user["username"] == username:

                return {

                    "username": user["username"],
                    "password": user["password"],
                    "fullname": user["fullname"],
                    "phone": user["phone"],
                    "mountpoints": user["mountpoints"],
                    "active": user["active"],
                    "expire_date": user["expire_date"]
                }

        return None

    except Exception as e:

        print("ERROR get_user:", e)

        return None


# =========================
# CREAR USUARIO
# =========================

def create_user(

    username,
    password,
    mountpoints,
    expire_date,
    fullname,
    phone
):

    users = load_users()

    for user in users:

        if user["username"] == username:

            raise Exception(
                "El usuario ya existe"
            )

    new_user = {

        "username": username,
        "password": password,
        "fullname": fullname,
        "phone": phone,
        "mountpoints": mountpoints,
        "active": True,
        "expire_date": expire_date
    }

    users.append(new_user)

    save_users(users)

    return True


# =========================
# ACTUALIZAR USUARIO
# =========================

def update_user(

    username,
    password,
    fullname,
    phone,
    mountpoints,
    active,
    expire_date
):

    try:

        users = load_users()

        for user in users:

            if user["username"] == username:

                user["password"] = password
                user["fullname"] = fullname
                user["phone"] = phone
                user["mountpoints"] = mountpoints
                user["active"] = active
                user["expire_date"] = expire_date

        save_users(users)

        return True

    except Exception as e:

        print("ERROR update_user:", e)

        return False


# =========================
# ELIMINAR USUARIO
# =========================

def delete_user(username):

    try:

        users = load_users()

        users = [

            user for user in users

            if user["username"] != username
        ]

        save_users(users)

        return True

    except Exception as e:

        print("ERROR delete_user:", e)

        return False


# =========================
# ÚLTIMOS USUARIOS
# =========================

def get_last_users(limit=5):

    try:

        users = load_users()

        users.reverse()

        result = []

        for user in users[:limit]:

            result.append((

                user["username"],
                user["fullname"],
                user["phone"],
                user["mountpoints"],
                user["expire_date"],
                user["active"]
            ))

        return result

    except Exception as e:

        print("ERROR get_last_users:", e)

        return []
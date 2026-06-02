import os


def build_strsvr_config(data):

    config = f"""
[in]
type=ntripcli
path={data['host']}:{data['port']}/{data['mountpoint']}
user={data['user']}
password={data['password']}

[out]
type=tcpserver
port={data['output_port']}
"""

    config_path = os.path.join(
        "configs",
        "strsvr.conf"
    )

    with open(
        config_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(config)

    return config_path
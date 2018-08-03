import random
import string
import subprocess
import time
import urllib.request, json
from os.path import expanduser



def spawn_bitcoind(network, zmq_port, rpc_port, rpc_user, rpc_password, dir_root):
    args = ["bitcoind", "-daemon", "-conf=''" "-dbcache=3000", "-disablewallet", "-maxuploadtarget=1000",
            "-nopeerbloomfilters=1", "-permitbaremultisig=0" "-server=1", "-txindex=1",
            f"-zmqpubrawblock=tcp://127.0.0.1:{zmq_port}", f"-zmqpubrawtx=tcp://127.0.0.1:{zmq_port}",
            f"-rpcport={rpc_port}" f"-rpcuser={rpc_user}", f"-rpcpassword={rpc_password}",
            f"-assumevalid={url_to_json('https://blockchain.info/latestblock').hash}", f"-datadir={dir_root}/bitcoin"]
    subprocess.Popen(args)


def spawn_lnd(network, lnd_rpc_port, rpc_user, rpc_pass, zmq_port, rpc_port, dir_root):
    args = ["lnd"
            "--maxpendingchannels=10"
            "--minchansize=250000"
            f"--rpclisten={lnd_rpc_port}"
            "--autopilot.active=1"
            "--autopilot.maxchannels=10",
            "autopilot.maxchansize=250000",
            "autopilot.allocation=0.8",
            "bitcoin.active=1",
            "bitcoin.feerate=1000",
            "bitcoin.node=bitcoind",
            f"bitcoind.rpcuser={rpc_user}", f"bitcoind.rpcpass={rpc_pass}", f"bitcoind.zmqpath={zmq_port}",
            f"bitcoind.rpcport={rpc_port}", f"--datadir={dir_root}/lnd_bitcoin/logs",
            f"--tlscertpath={dir_root}/lnd_bitcoin/tls.cert", f"--tlskeypath={dir_root}/lnd_bitcoin/tls.key",
            f"--adminmacaroonpath={dir_root}/lnd_bitcoin/admin.macaroon"]

    subprocess.Popen(args)

zmq_port = 10000
rpc_port = 10001
rpc_user = "user"
rpc_pass = "bluequartz"

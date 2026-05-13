from flask import Flask
from flask import request
from flask import jsonify

from topology import Topology
import json


# ====================================
# RESET TOPOLOGY ON START
# ====================================

default_topology = {

    "routers": [],

    "switches": [],

    "vms": [],

    "vlans": [],

    "connections": []
}

with open(

    "topology.json",

    "w"
) as f:

    json.dump(

        default_topology,

        f,

        indent=4
    )

app = Flask(__name__)

# ====================================
# CREATE TOPOLOGY
# ====================================

topology = Topology()

# ====================================
# CREATE ROUTER
# ====================================

@app.route("/routers", methods=["POST"])

def create_router():

    data = request.json

    name = data.get("name")

    if not name:

        return jsonify({

            "error": "Router name required"

        }), 400

    topology.add_router(name)

    return jsonify({

        "message":
        f"Router {name} created"
    })

# ====================================
# CREATE SWITCH
# ====================================

@app.route("/switches", methods=["POST"])

def create_switch():

    data = request.json

    name = data.get("name")

    if not name:

        return jsonify({

            "error": "Switch name required"

        }), 400

    topology.add_switch(name)

    return jsonify({

        "message":
        f"Switch {name} created"
    })

# ====================================
# CREATE VM
# ====================================

@app.route("/vms", methods=["POST"])

def create_vm():

    data = request.json

    name = data.get("name")

    vlan = data.get("vlan")

    if not name:

        return jsonify({

            "error": "VM name required"

        }), 400

    topology.add_vm(

        name,
        vlan
    )

    return jsonify({

        "message":
        f"VM {name} created"
    })

# ====================================
# CREATE VLAN
# ====================================

@app.route("/vlans", methods=["POST"])

def create_vlan():

    data = request.json

    vlan_id = data.get("vlan_id")

    if vlan_id is None:

        return jsonify({

            "error":
            "VLAN ID required"

        }), 400

    topology.add_vlan(vlan_id)

    return jsonify({

        "message":
        f"VLAN {vlan_id} created"
    })

# ====================================
# CONNECT DEVICES
# ====================================

@app.route("/connect", methods=["POST"])

def connect_devices():

    data = request.json

    device1 = data.get("device1")

    device2 = data.get("device2")

    if not device1 or not device2:

        return jsonify({

            "error":
            "Both devices required"

        }), 400

    result = topology.connect_devices(

        device1,
        device2
    )

    if not result:

        return jsonify({

            "error":
            "Connection failed"

        }), 400

    return jsonify({

        "message":
        f"{device1} connected to {device2}"
    })

# ====================================
# GET FULL TOPOLOGY
# ====================================

@app.route("/topology", methods=["GET"])

def get_topology():

    return jsonify(topology.data)

# ====================================
# DELETE ROUTER
# ====================================

@app.route("/routers/<name>", methods=["DELETE"])

def delete_router(name):

    result = topology.delete_router(name)

    if not result:

        return jsonify({

            "error":
            "Router not found"

        }), 404

    return jsonify({

        "message":
        f"Router {name} deleted"
    })

# ====================================
# DELETE SWITCH
# ====================================

@app.route("/switches/<name>", methods=["DELETE"])

def delete_switch(name):

    result = topology.delete_switch(name)

    if not result:

        return jsonify({

            "error":
            "Switch not found"

        }), 404

    return jsonify({

        "message":
        f"Switch {name} deleted"
    })

# ====================================
# DELETE VM
# ====================================

@app.route("/vms/<name>", methods=["DELETE"])

def delete_vm(name):

    result = topology.delete_vm(name)

    if not result:

        return jsonify({

            "error":
            "VM not found"

        }), 404

    return jsonify({

        "message":
        f"VM {name} deleted"
    })

# ====================================
# DELETE VLAN
# ====================================

@app.route("/vlans/<int:vlan_id>", methods=["DELETE"])

def delete_vlan(vlan_id):

    result = topology.delete_vlan(vlan_id)

    if not result:

        return jsonify({

            "error":
            "VLAN not found"

        }), 404

    return jsonify({

        "message":
        f"VLAN {vlan_id} deleted"
    })

# ====================================
# RUN APP
# ====================================

if __name__ == "__main__":

    app.run(debug=False, use_reloader=False)
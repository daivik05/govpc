from flask import Flask
from flask import request
from flask import jsonify

from topology import Topology

app = Flask(__name__)

topology = Topology()

# =========================
# CREATE ROUTER
# =========================

@app.route("/routers", methods=["POST"])
def create_router():

    data = request.json

    name = data.get("name")

    if not name:
        return jsonify({
            "error": "Router name required"
        }), 400

    success = topology.add_router(name)

    if not success:
        return jsonify({
            "error": "Router already exists"
        }), 400

    return jsonify({
        "message": f"Router {name} created"
    })

# =========================
# GET ROUTERS
# =========================

@app.route("/routers", methods=["GET"])
def get_routers():

    return jsonify(
        list(topology.routers.keys())
    )

# =========================
# DELETE ROUTER
# =========================

@app.route("/routers/<name>", methods=["DELETE"])
def delete_router(name):

    success = topology.delete_router(name)

    if not success:
        return jsonify({
            "error": "Router not found"
        }), 404

    return jsonify({
        "message": f"Router {name} deleted"
    })

# =========================
# CREATE SWITCH
# =========================

@app.route("/switches", methods=["POST"])
def create_switch():

    data = request.json

    name = data.get("name")

    if not name:
        return jsonify({
            "error": "Switch name required"
        }), 400

    success = topology.add_switch(name)

    if not success:
        return jsonify({
            "error": "Switch already exists"
        }), 400

    return jsonify({
        "message": f"Switch {name} created"
    })

# =========================
# CONNECT ROUTERS
# =========================

@app.route("/connect", methods=["POST"])
def connect_routers():

    data = request.json

    r1 = data.get("router1")
    r2 = data.get("router2")

    success = topology.connect_routers(r1, r2)

    if not success:

        return jsonify({
            "error": "Router missing"
        }), 400

    return jsonify({
        "message": f"{r1} connected to {r2}"
    })

# =========================
# GET ROUTE (BFS)
# =========================

@app.route("/route", methods=["POST"])
def get_route():

    data = request.json

    source = data.get("source")
    destination = data.get("destination")

    if source not in topology.routers:
        return jsonify({
            "error": "Source router missing"
        }), 400

    if destination not in topology.routers:
        return jsonify({
            "error": "Destination router missing"
        }), 400

    path = topology.routers[source].get_path(destination)

    if not path:

        return jsonify({
            "error": "No route found"
        }), 404

    route = [router.name for router in path]

    return jsonify({
        "route": route
    })

if __name__ == "__main__":

    app.run(debug=True)
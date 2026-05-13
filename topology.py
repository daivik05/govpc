import json


class Topology:

    def __init__(self):

        self.file_name = "topology.json"

        # ====================================
        # LOAD TOPOLOGY
        # ====================================

        try:

            with open(
                self.file_name,
                "r"
            ) as f:

                self.data = json.load(f)

        except:

            self.data = {

                "routers": [],

                "switches": [],

                "vms": [],

                "vlans": [],

                "connections": []
            }

            self.save_topology()

    # ====================================
    # SAVE TOPOLOGY
    # ====================================

    def save_topology(self):
        with open(
            self.file_name,
            "w"
        ) as f:
            json.dump(
                self.data,
                f,
                indent=4
            )

    # ====================================
    # ADD ROUTER
    # ====================================

    def add_router(self, name):

        if name not in self.data["routers"]:

            self.data["routers"].append(name)

            self.save_topology()

    # ====================================
    # DELETE ROUTER
    # ====================================

    def delete_router(self, name):

        if name in self.data["routers"]:

            self.data["routers"].remove(name)

            self.remove_connections(name)

            self.save_topology()

            return True

        return False

    # ====================================
    # ADD SWITCH
    # ====================================

    def add_switch(self, name):

        if name not in self.data["switches"]:

            self.data["switches"].append(name)

            self.save_topology()

    # ====================================
    # DELETE SWITCH
    # ====================================

    def delete_switch(self, name):

        if name in self.data["switches"]:

            self.data["switches"].remove(name)

            self.remove_connections(name)

            self.save_topology()

            return True

        return False

    # ====================================
    # ADD VM
    # ====================================

    def add_vm(

        self,

        name,

        vlan=None
    ):

        # Avoid duplicates
        for vm in self.data["vms"]:

            if vm["name"] == name:

                return

        vm_data = {

            "name": name,

            "vlan": vlan
        }

        self.data["vms"].append(vm_data)

        self.save_topology()

    # ====================================
    # DELETE VM
    # ====================================

    def delete_vm(self, name):

        for vm in self.data["vms"]:

            if vm["name"] == name:

                self.data["vms"].remove(vm)

                self.remove_connections(name)

                self.save_topology()

                return True

        return False

    # ====================================
    # ADD VLAN
    # ====================================

    def add_vlan(self, vlan_id):

        if vlan_id not in self.data["vlans"]:

            self.data["vlans"].append(vlan_id)

            self.save_topology()

    # ====================================
    # DELETE VLAN
    # ====================================

    def delete_vlan(self, vlan_id):

        if vlan_id in self.data["vlans"]:

            self.data["vlans"].remove(vlan_id)

            self.save_topology()

            return True

        return False

    # ====================================
    # CONNECT DEVICES
    # ====================================

    def connect_devices(

        self,

        device1,
        device2
    ):

        all_devices = []

        # Routers
        all_devices.extend(

            self.data["routers"]
        )

        # Switches
        all_devices.extend(

            self.data["switches"]
        )

        # VMs
        for vm in self.data["vms"]:

            all_devices.append(
                vm["name"]
            )

        # ====================================
        # VALIDATE DEVICES
        # ====================================

        if device1 not in all_devices:

            return False

        if device2 not in all_devices:

            return False

        connection = [

            device1,
            device2
        ]

        reverse_connection = [

            device2,
            device1
        ]

        # ====================================
        # AVOID DUPLICATES
        # ====================================

        if (
            connection
            not in self.data["connections"]

            and

            reverse_connection
            not in self.data["connections"]
        ):

            self.data["connections"].append(
                connection
            )

            self.save_topology()

        return True

    # ====================================
    # REMOVE CONNECTIONS
    # ====================================

    def remove_connections(

        self,

        device_name
    ):

        updated_connections = []

        for conn in self.data["connections"]:

            if (
                device_name not in conn
            ):

                updated_connections.append(
                    conn
                )

        self.data["connections"] = (
            updated_connections
        )

        self.save_topology()
import requests
import os
import json
import sys
import datetime

# API Setup
API_KEY = os.getenv("TAKTILE_API_KEY")  # Securely retrieve the API key from environment variables
BASE_URL = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY
}

# Log file setup
LOG_FILE = "script_log.txt"

def log_message(message):
    """Adds messages to the logs and prints in the console"""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry)

    # Print messages to the console
    print(message)


# Get changed files from GitHub Actions
changed_files = [os.path.basename(f).replace(".py", "") for f in sys.argv[1:]]  # Remove '.py' extension


def list_decision_flows():
    """Retrieve all flow IDs for the company."""
    url = f"{BASE_URL}/list-decision-graphs/sandbox/decide"
    payload = {
        "data": {"organization_name": "NB36"},
        "metadata": {"version": "v1.0"},
        "control": {"execution_mode": "sync"}
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        flows = response.json().get("data", {}).get("flows", [])
        flow_ids = [flow["flow_id"] for flow in flows]
        log_message(f"Retrieved {len(flow_ids)} decision flow(s).")
        return flow_ids
    else:
        log_message(f"Error fetching decision flows: {response.text}")
        return []


def get_decision_graph(flow_id):
    """Fetch decision graph and return code nodes (node_id, node_name)."""
    url = f"{BASE_URL}/get-decision-graph/sandbox/decide"
    payload = {
        "data": {"flow_id": flow_id},
        "metadata": {"version": "v1.0"},
        "control": {"execution_mode": "sync"}
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        data = response.json().get("data", {}).get("graph", [])
        nodes = {node["node_name"]: node["node_id"] for node in data if node["node_type"] == "code_node"}
        return nodes
    else:
        log_message(f"Error fetching decision graph for flow {flow_id}: {response.text}")
        return {}


def update_code_node(flow_id, node_id, src_code):
    """Patch decision graph to update the code node"""
    url = f"{BASE_URL}/patch-decision-graph/sandbox/decide"
    payload = {
        "data": {
            "flow_id": flow_id,         
            "node_id": node_id,
            "src_code": src_code  # New code 
        },
        "metadata": {
            "version": "v1.0",
            "entity_id": "string"
        },
        "control": {
            "execution_mode": "sync"
        }
    }
    
    log_message(f"Sending POST request with payload:\n{json.dumps(payload, indent=4)}")

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        log_message(f"Successfully updated node with id {node_id} in flow {flow_id}.")
    else:
        log_message(f"Failed to update node with id {node_id}: {response.text}")


def main():
    """Exececute the main function"""
    log_message("\n================== GitHub to Taktile Sync Started ==================\n")

    if not changed_files:
        log_message("No changed scripts detected")
        return

    log_message(f"Detecting changes for: {changed_files}")

    # Retrieve flow IDs dynamically
    flow_ids = list_decision_flows()

    if not flow_ids:
        log_message("No decision flows have been found")
        return

    for flow_id in flow_ids:
        taktile_nodes = get_decision_graph(flow_id)

        for script_name in changed_files:
            if script_name in taktile_nodes:
                node_id = taktile_nodes[script_name]
                script_path = f"scripts/{script_name}.py"

                try:
                    with open(script_path, "r", encoding="utf-8") as file:
                        src_code = file.read()

                    log_message(f"Updating {script_name}.py in Taktile (Flow ID: {flow_id}, Node ID: {node_id})...")
                    update_code_node(flow_id, node_id, src_code)

                except FileNotFoundError:
                    log_message(f"Error: {script_path} not found.")

            else:
                log_message(f"No matching node found for {script_name}.py in flow {flow_id}")

    log_message("\n================== Script Execution Finished ==================\n")


if __name__ == "__main__":
    main()

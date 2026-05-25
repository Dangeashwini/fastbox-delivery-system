import json
import math
import os


# ---------------------------------------------------
# Assumptions:
# 1. One package is assigned to only one nearest agent.
# 2. Agents start from their current location.
# 3. Distance formula used: Euclidean distance.
# 4. Total delivery distance =
#    Agent -> Warehouse + Warehouse -> Destination
# 5. Efficiency =
#    total_distance / packages_delivered
#    Lower efficiency value means better performance.
# 6. If two agents are at same distance,
#    first encountered agent is selected.
# ---------------------------------------------------


def euclidean_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    """
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


def load_data(filename):
    """
    Load JSON data from file.
    """
    with open(filename, "r") as file:
        return json.load(file)


def assign_packages(data):

    warehouses = data["warehouses"]

    agents = data["agents"]

    assignments = []

    for package in data["packages"]:

        warehouse_id = package["warehouse"]

        warehouse_location = warehouses[warehouse_id]

        nearest_agent = None

        minimum_distance = float("inf")

        for agent_id, agent_location in agents.items():

            distance = euclidean_distance(
                agent_location,
                warehouse_location
            )

            if distance < minimum_distance:

                minimum_distance = distance

                nearest_agent = agent_id

        assignments.append({
            "package_id": package["id"],
            "agent_id": nearest_agent,
            "warehouse_location": warehouse_location,
            "destination": package["destination"]
        })

    return assignments


def simulate_deliveries(assignments, data):

    agents = data["agents"]

    report = {}

    # Initialize report
    for agent_id in agents:

        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0
        }

    # Process deliveries
    for assignment in assignments:

        agent_id = assignment["agent_id"]

        agent_location = agents[agent_id]

        warehouse_location = assignment["warehouse_location"]

        destination = assignment["destination"]

        # Distance calculations
        agent_to_warehouse = euclidean_distance(
            agent_location,
            warehouse_location
        )

        warehouse_to_destination = euclidean_distance(
            warehouse_location,
            destination
        )

        total_trip_distance = (
            agent_to_warehouse +
            warehouse_to_destination
        )

        report[agent_id]["packages_delivered"] += 1

        report[agent_id]["total_distance"] += total_trip_distance

    # Efficiency calculation
    for agent_id in report:

        packages = report[agent_id]["packages_delivered"]

        total_distance = report[agent_id]["total_distance"]

        if packages > 0:

            efficiency = total_distance / packages

        else:

            efficiency = float("inf")

        report[agent_id]["total_distance"] = round(
            total_distance,
            2
        )

        report[agent_id]["efficiency"] = round(
            efficiency,
            2
        )

    # Best agent
    best_agent = min(
        report,
        key=lambda x: report[x]["efficiency"]
    )

    report["best_agent"] = best_agent

    return report

def save_report(report, filename):
    """
    Save report to JSON file.
    """
    with open(filename, "w") as file:
        json.dump(report, file, indent=4)


def main():

    current_folder = "."

    for file_name in os.listdir(current_folder):

        # Process only test case JSON files
        if file_name.startswith("test_case_") and file_name.endswith(".json"):

            print(f"\nRunning: {file_name}")

            data = load_data(file_name)

            assignments = assign_packages(data)

            report = simulate_deliveries(
                assignments,
                data
            )

            # Create report filename
            report_file = (
                file_name.replace(".json", "_report.json")
            )

            # Save report
            with open(report_file, "w") as file:

                json.dump(report, file, indent=4)

            print(json.dumps(report, indent=4))

if __name__ == "__main__":
    main()
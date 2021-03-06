"""Json data I/O handler."""

import json


class JsonData:
    """Static class to hadel jsondata."""

    @staticmethod
    def load_json_file(filename):
        """Load json file."""
        json_data = open(filename).read()
        return json.loads(json_data)

    @staticmethod
    def environment_object_to_json(objects):
        """Convert env objects to json object."""
        json_objects = []
        if objects is not None:
            for i in range(len(objects)):
                object_temp = {}
                object_temp["x"] = objects[i].location[0]
                object_temp["y"] = objects[i].location[1]
                object_temp["radius"] = objects[i].radius
                try:
                    object_temp["q_value"] = objects[i].q_value
                except (KeyError, AttributeError):
                    pass

                json_objects.append(object_temp)
            return json_objects
        else:
            return []

    @staticmethod
    def agent_to_json(agent):
        """Agent object to json."""
        agent_dict = {}
        agent_dict["x"] = agent.location[0]
        agent_dict["y"] = agent.location[1]
        agent_dict["id"] = agent.name
        agent_dict["direction"] = agent.direction
        agent_dict["state"] = "Nan"

        """
        if agent.signal.grid:
            agent_dict["signal"] = 1
            agent_dict["signal_radius"] = 40
        else:
            agent_dict["signal"] = 0
            agent_dict["signal_radius"] = 0
        """
        return agent_dict

    @staticmethod
    def to_json(width, height, hub, sites, obstacles, traps,
                cues, food, debris, agents):
        """Convert simulation to json."""
        return(
            json.dumps(
                {
                    "type": "update",
                    "data":
                    {
                        "x_limit": width / 2,
                        "y_limit": height / 2,
                        "hub": JsonData.environment_object_to_json(hub),
                        "sites": JsonData.environment_object_to_json(sites),
                        "obstacles": JsonData.environment_object_to_json(
                            obstacles),
                        "traps": JsonData.environment_object_to_json(traps),
                        # "cues": JsonData.environment_object_to_json(cues),
                        "food": JsonData.environment_object_to_json(food),
                        "debris": JsonData.environment_object_to_json(debris),
                        "agents": [JsonData.agent_to_json(
                            agent) for agent in agents],
                    }
                })
        )


class JsonPhenotypeData:
    """Static class to hadel jsondata.

    Handles phenotype data.
    """

    @staticmethod
    def load_json_file(filename):
        """Load json file."""
        json_data = open(filename).read()
        return eval(json.loads(json_data))

    @staticmethod
    def to_json(phenotypes, filename):
        """Convert phenotype data to json."""
        data = json.dumps({'phenotypes': phenotypes})

        with open(filename, 'w') as f:
            json.dump(data, f)

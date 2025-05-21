def get_keepingFullTimeInMinutes_dict(agent_id, steps, value):
    dict = {
        "actor": "PERSON",
        "id": agent_id,
        "steps": steps,
        "operator": "MULTIPLY",
        "fieldName": "keepingFullTimeInMinutes",
        "value": value,
        "accessors": [
            {
                "manipulationType": "FIELD",
                "name": "foodNeed"
            }
        ]
    }

    return dict

def get_fullnessDecreasePerStep_dict(agent_id, steps, value):
    dict =  {
        "actor": "PERSON",
        "id": agent_id,
        "steps": steps,
        "operator": "MULTIPLY",
        "fieldName": "fullnessDecreasePerStep",
        "value": value,
        "accessors": [
            {
                "manipulationType": "FIELD",
                "name": "foodNeed"
            }
        ]
    }

    return dict

def get_outlierDegree_dict(agent_id, steps, value):
    dict =  {
        "actor": "PERSON",
        "id": agent_id,
        "steps": steps,
        "operator": "SET",
        "fieldName": "outlierDegree",
        "value": value,
        "accessors": [
            {
                "manipulationType": "FIELD",
                "name": "outlier"
            }
        ]
    }

    return dict

def get_setOutlierType_dict(agent_id, steps, outlier_type):
    dict = {
        "actor": "PERSON",
        "id": agent_id,
        "steps": steps,
        "accessors": [
            {
                "manipulationType": "METHOD",
                "name": "setOutlierType",
                "parameters": [
                    outlier_type
                ]
            }
        ]
    }

    return dict

def get_shiftInterest_dict(agent_id, steps, interest_value):
    dict =  {
        "actor": "PERSON",
        "id": agent_id,
        "steps": steps,
        "accessors": [
            {
                "manipulationType": "METHOD",
                "name": "shiftInterest",
                "parameters": [
                    interest_value
                ]
            }
        ]
    }

    return dict

def get_method_manipulations_json(agent_id, steps, method_name, parameters, actor="PERSON"):
    if not isinstance(parameters, list):
        parameters = [parameters]
        
    if method_name == "infectPopularPub":
        agent_id = -1

    dict = {
        "actor": actor,
        "id": agent_id,
        "steps": steps,
        "accessors": [
            {
                "manipulationType": "METHOD",
                "name": method_name,
                "parameters": parameters
            }
        ]
    }
    if agent_id < 0:
        dict.pop("id")
    return dict
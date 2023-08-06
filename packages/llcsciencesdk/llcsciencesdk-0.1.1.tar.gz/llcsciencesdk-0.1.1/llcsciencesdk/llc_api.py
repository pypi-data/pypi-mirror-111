import requests
import pandas as pd


def toDf(data):
    return pd.DataFrame(data)


BASE_API_URL = (
    "https://internal-landlifecompany.appspot.com/"
)

AUTH_URL = (
    "https://internal-landlifecompany.appspot.com/api/v1/token/"
)

GET_MODEL_INPUT = f"{BASE_API_URL}/sciencemodel/fasttrackinput/planting_design_config/"


def get_model_inputs(config_option, username, password):
    r = requests.post(AUTH_URL, data={"username": username, "password": password})
    token = r.json()["access"]
    data = requests.get(
        GET_MODEL_INPUT + str(config_option),
        headers={"Authorization": f"Bearer {token}"},
    )

    site_info = data.json()["site_info"]
    plot_types = data.json()["plot_types"]
    parameter_data = data.json()["parameter_data"]
    parameter_info = data.json()["parameter_info"]
    species_info = data.json()["species_info"]
    model_info = data.json()["model_info"]

    df_sites_info = pd.json_normalize(site_info)
    df_plot_types = pd.json_normalize(plot_types)
    df_parameter_data = pd.json_normalize(parameter_data)
    df_parameter_info = pd.json_normalize(parameter_info)
    df_species_info = pd.json_normalize(species_info)
    df_model_info = pd.json_normalize(model_info)

    return (
        df_sites_info,
        df_plot_types,
        df_parameter_data,
        df_parameter_info,
        df_species_info,
        df_model_info,
    )

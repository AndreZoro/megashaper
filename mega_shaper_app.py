import base64
import streamlit as st
import pyvista as pv
from pyvista import themes

pv.set_plot_theme(themes.DarkTheme())
from stpyvista import stpyvista
import tempfile

import requests


st.set_page_config(
    page_title="MEGA Shaper",
    page_icon=":nut_and_bolt:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)


st.title(
    "The best geometry designer out there (maybe not, but at least easy to use...)"
)

pv.start_xvfb()


whl_dia = 20
messages = []


@st.cache_data
def get_rim(payload):
    payload["geo_part"] = "rim"
    endpoint = st.secrets.connections.shaper_geo_api.url + "/v1/small_rim"
    r = requests.get(
        endpoint,
        auth=(
            st.secrets.connections.shaper_geo_api.usr,
            st.secrets.connections.shaper_geo_api.pw,
        ),
        # "http://127.0.0.1:8000/v1/small_rim",
        json=payload,
        headers={"Content-type": "application/json"},
    )
    data = r.json()
    mesh = base64.b64decode(data["rim_geo"])
    # Write the decoded data to a temporary STL file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".stl") as temp_file:
        temp_file.write(mesh)
        temp_rim_stl_filename = temp_file.name

        with open(temp_rim_stl_filename, "rb") as f:
            stl_data = f.read()
        # Read the STL file using PyVista
        mesh = pv.read(temp_rim_stl_filename)
    return mesh, stl_data, data["message"]


@st.cache_data
def get_tire(
    whl_dia,
    whl_wdt,
    tre_dia,
):
    payload = {
        "geo_part": "tire",
        "whl_dia": whl_dia,
        "axl_dia": 1,
        "whl_wdt": whl_wdt,
        "tre_dia": tre_dia,
        "bck_spc": 0,
        "cnv_dtp": 0,
        "sld_hgt": 0,
        "sld_wdt": whl_wdt / 2,
        "sld_pos": whl_wdt / 4,
        "n_holes": 5,
        "main_dia": whl_dia / 3,
        "hole_dia": whl_dia / 8,
        "lyr_hgt": 0.01,
        "nzl_wdt": 0.4,
        "spoke_dropdown": "SpeedDisk",
    }
    endpoint = st.secrets.connections.shaper_geo_api.url + "/v1/small_rim"
    r = requests.get(
        endpoint,
        auth=(
            st.secrets.connections.shaper_geo_api.usr,
            st.secrets.connections.shaper_geo_api.pw,
        ),
        json=payload,
        headers={"Content-type": "application/json"},
    )
    data = r.json()
    mesh = base64.b64decode(data["rim_geo"])
    # Write the decoded data to a temporary STL file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".stl") as temp_file:
        temp_file.write(mesh)
        temp_filename = temp_file.name

        # Read the STL file using PyVista
        mesh = pv.read(temp_filename)
    return mesh, data["message"]


rim, rim_stl, rim_msg = get_rim(
    {
        "whl_dia": 20,
        "axl_dia": 3,
        "whl_wdt": 10,
        "tre_dia": 24,
        "bck_spc": 2,
        "cnv_dtp": 2,
        "sld_hgt": 1,
        "sld_wdt": 5,
        "sld_pos": 2,
        "n_holes": 5,
        "main_dia": 6,
        "hole_dia": 5,
        "lyr_hgt": 0.12,
        "nzl_wdt": 0.4,
        "spoke_dropdown": "LamboStyle",
    }
)
tire, tire_msg = get_tire(
    20,
    10,
    24,
)


param_col, threed_col = st.columns(2)

with param_col:
    with st.form("Define Rim Design:"):
        rd_tab1, rd_tab2, rd_tab3, rd_tab4, rd_tab5 = st.tabs(
            ["Main Dims", "Des Dims", "Shoulder Dims.", "Spokes", "Misc."]
        )

        with rd_tab1:
            st.write("Main dimensions:")
            t1_col1, t1_col2 = st.columns([2, 1])
            with t1_col1:
                st.image("assets/main_dims_anot.png")
            with t1_col2:
                whl_dia = st.slider(
                    "Wheel Diameter",
                    min_value=2.0,
                    max_value=50.0,
                    value=20.0,
                    step=0.1,
                    help="Wheel (rim) diameter in mm",
                )
                axl_dia = st.slider(
                    "Axle Diameter",
                    min_value=0.2,
                    max_value=10.0,
                    value=3.0,
                    step=0.1,
                    help="Axel diameter in mm",
                )
                whl_wdt = st.slider(
                    "Wheel Width",
                    min_value=2.0,
                    max_value=50.0,
                    value=10.0,
                    step=0.1,
                    help="Wheel (rim) width in mm",
                )
                tre_dia = st.slider(
                    "Tire Diameter",
                    min_value=whl_dia,
                    max_value=60.0,
                    value=1.2 * whl_dia,
                    step=0.1,
                    help="Tire diameter in mm\n(Only needed for visualisation purposes)",
                )

        with rd_tab2:
            st.write("Additional dimensions:")
            t2_col1, t2_col2 = st.columns([2, 1])
            with t2_col1:
                st.image("assets/des_dims_anot.png")
            with t2_col2:
                bck_spc = st.slider(
                    "Back Spacing",
                    min_value=0.0,
                    max_value=10.0,
                    value=2.0,
                    step=0.1,
                    help="Help not ready yet",
                )
                cnv_dtp = st.slider(
                    "Convex Depth",
                    min_value=0.0,
                    max_value=10.0,
                    value=2.0,
                    step=0.1,
                    help="Help not ready yet",
                )

        with rd_tab3:
            st.write("Use a shoulder:")
            t3_col1, t3_col2 = st.columns([2, 1])
            with t3_col1:
                st.image("assets/shoulder_dims_anot.png")
            with t3_col2:
                sld_hgt = st.slider(
                    "Shoulder Height",
                    min_value=0.0,
                    max_value=10.0,
                    value=1.0,
                    step=0.1,
                    help="Shoulder Height in mm",
                )
                sld_wdt = st.slider(
                    "Shoulder Width",
                    min_value=1.0,
                    max_value=40.0,
                    value=5.0,
                    step=0.1,
                    help="Shoulder Width in mm",
                )
                sld_pos = st.slider(
                    "Shoulder Position",
                    min_value=0.0,
                    max_value=30.0,
                    value=2.5,
                    step=0.1,
                    help="Shoulder Position in mm",
                )

        with rd_tab4:
            st.write("Speed Disk rims do not need any further settings.")
            st.divider()
            st.write("Lambo Style rim settings:")
            ls_col1, ls_col2, ls_col3 = st.columns(3)
            with ls_col1:
                n_holes = st.slider(
                    "Number of holes in rim",
                    min_value=1,
                    max_value=12,
                    value=5,
                    step=1,
                    help="Choose the number of holes along the main diameter",
                )
            with ls_col2:
                main_dia = st.slider(
                    "Main diameter",
                    min_value=1,
                    max_value=12,
                    value=6,
                    step=1,
                    help="In mm, the holes get arranged along this contruction geometry",
                )
            with ls_col3:
                hole_dia = st.slider(
                    "Diameter of lambo holes",
                    min_value=1,
                    max_value=12,
                    value=5,
                    step=1,
                    help="In mm",
                )
            st.divider()
            st.write("Spoke Rims are not implemented yet!")

        with rd_tab5:
            st.write("FDM 3D Printer settings:")
            st.markdown(
                """
    ### FDM 3D Printer settings:
    Use these settings when using an FDM 3D Printer.
    The layer height and nozzle diameter are used
    to calculate some of the dimensions on the part to
    make sure they will work with your slicer software.
    If you are using an SLS based printer, just set the
    values to your resolution or something low."""
            )
            prt_col1, prt_col2 = st.columns(2)
            with prt_col1:
                lyr_hgt = st.slider(
                    "Layer Height",
                    min_value=0.04,
                    max_value=1.0,
                    value=0.12,
                    step=0.01,
                    help="Layer height in mm of fdm 3D printer.",
                )
            with prt_col2:
                nzl_wdt = st.slider(
                    "Nozzle Diameter",
                    min_value=0.04,
                    max_value=1.0,
                    value=0.4,
                    step=0.01,
                    help="Nozzel diameter in mm of fdm 3D printer.",
                )

        st.divider()
        end_col1, end_col2 = st.columns([3, 1])
        with end_col1:
            spoke_dropdown = st.selectbox(
                "Select Spoke Type:",
                ["Speed Disk", "Lambo Style", "Spokes"],
            )
        with end_col2:
            st.write("When you are done, click here:")
            submitted = st.form_submit_button("Generate Rim")
            if submitted:
                st.write("Creating new rim...")
                rim_params = {
                    "whl_dia": whl_dia,
                    "axl_dia": axl_dia,
                    "whl_wdt": whl_wdt,
                    "tre_dia": tre_dia,
                    "bck_spc": bck_spc,
                    "cnv_dtp": cnv_dtp,
                    "sld_hgt": sld_hgt,
                    "sld_wdt": sld_wdt,
                    "sld_pos": sld_pos,
                    "n_holes": n_holes,
                    "main_dia": main_dia,
                    "hole_dia": hole_dia,
                    "lyr_hgt": lyr_hgt,
                    "nzl_wdt": nzl_wdt,
                    "spoke_dropdown": spoke_dropdown.replace(" ", ""),
                }

                st.write("Requesting new rim:")
                rim, rim_stl, rim_msg = get_rim(rim_params)
                tire, tire_msg = get_tire(
                    whl_dia,
                    whl_wdt,
                    tre_dia,
                )

                st.write("Request done.")

        if spoke_dropdown == "Spokes":
            st.write("Spoke rims are not implemented yet.")
        for msg in messages:
            st.write(msg)

with threed_col:
    st.write("3D View:")

    def delmodel():
        del st.session_state.fileuploader

    placeholder = st.empty()

    if rim:
        ## Initialize pyvista reader and plotter
        plotter = pv.Plotter(border=False, window_size=[600, 600])
        plotter.background_color = "darkgrey"

        plotter.add_mesh(rim, color="orange", specular=0.5)
        plotter.view_xz()

        plotter.add_mesh(tire, color="black", specular=0.25, opacity=0.6)

        plotter.view_vector([1, 1, 1])

        ## Show in webpage
        with placeholder.container():
            st.button("🔙 Restart", "btn_rerender", on_click=delmodel)
            stpyvista(plotter)

        u3d_col_01, u3d_col_02 = st.columns([3, 1])
        with u3d_col_01:
            st.write(rim_msg + "\n" + tire_msg)
        with u3d_col_02:
            st.download_button(
                "Download your rim as stl", rim_stl, file_name="your_cool_rim.stl"
            )

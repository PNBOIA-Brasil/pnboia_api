import csv
from io import StringIO
from fastapi import Response
from sqlalchemy import inspect
from datetime import datetime


class APIUtils:
    def __init__(self):
        pass

    def csv_response(self, result:list, filename:str):
        if filename:
            first_object = result[0]
            inspector = inspect(first_object.__class__)

            cols_to_ignore = ['id','raw_id','geom']

            column_names = [column.key for column in inspector.columns if column.key not in cols_to_ignore]
            csv_data = StringIO()
            csv_writer = csv.DictWriter(csv_data, fieldnames=column_names)
            csv_writer.writeheader()

            for r in result:
                obj_dict = {column.key: getattr(r, column.key) for column in inspector.columns if column.key not in cols_to_ignore}
                csv_writer.writerow(obj_dict)

            csv_response = Response(content=csv_data.getvalue())
            csv_response.headers["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
            csv_response.headers["Content-Type"] = "text/csv"
            # print(csv_response.body)

        else:
            return result
        return csv_response

    def file_name_composition(self, buoy_name:str, start_date:datetime=None, end_date:datetime=None):
        buoy_name = (buoy_name
                .lower()
                .replace(' - ','-')
                .replace(' ','_')
            )

        if start_date and end_date:
            start_date = start_date.strftime("%Y%m%d%H%M")
            end_date = end_date.strftime("%Y%m%d%H%M")

            filename = buoy_name + "_" + start_date + "_" + end_date
        else:
            filename = buoy_name + "last_data"

        return filename

    def get_buoy_type(self, buoy_name:str):
        return buoy_name.split(" ")[0]

        #  return buoy_type

    def compose_base_html(self, buoy, buoys_metadata):

        base_html = f"""
    <p>METADADOS - BOIA {buoy.name}</p>

    <p>INFORMAÇÕES SOBRE FUNDEIO:</p>
    <ul>
        <li>Posição (LAT, LON): {buoy.latitude}, {buoy.longitude}</li>
        <li>Local: {buoy.local}</li>
        <li>Profundidade de fundeio: {buoys_metadata[0].depth} m</li>
    </ul>

    <p>INFORMAÇÕES SOBRE A BOIA:</p>
    <ul>
        <li>Fabricante: {buoys_metadata[0].brand}</li>
        <li>Modelo: {buoys_metadata[0].model}</li>
        <li>Diâmetro: {buoys_metadata[0].diameter} m</li>
        <li>Peso: {buoys_metadata[0].weight} kg</li>
    """
        return base_html

    def compose_buoy_information(self, setup_buoys, buoy_parameters):
        buoys_information_html = "</ul><p>CONFIGURAÇÃO DE SENSORES:</p><ul>"

        if "wspd2" in buoy_parameters:
            buoys_information_html += f"<li>Altura do Anemômetro 1 (sensor 1): {setup_buoys[0].height_anemometer_1} m</li>"
            buoys_information_html += f"<li>Altura do Anemômetro 2 (sensor 2): {setup_buoys[0].height_anemometer_2} m</li>"

        if "cspd1" in buoy_parameters:
            buoys_information_html += f"<li>Tamanho célula ADCP: {setup_buoys[0].cell_size_adcp} m</li>"
            buoys_information_html += f"<li>Profundidade Inicial (limite superior primeira celula) ADCP: {setup_buoys[0].depth_adcp} m</li>"


        buoys_information_html += "</ul>"

        return buoys_information_html

    def list_parameters(self, parameters, buoy_parameters):
        parameters_html = f"""<p>PARAMETROS:</p><ul>"""

        params_dict = {}
        for param in parameters:
            if param.parameter in buoy_parameters:
                params_dict.update({param.id: f"<li>{param.parameter}: {param.description}</li>"})

        keys_list = list(params_dict.keys())
        keys_list.sort()
        print(keys_list)
        sorted_params_texts = [params_dict[i] for i in keys_list]
        for text in sorted_params_texts:
            parameters_html += text

        return parameters_html

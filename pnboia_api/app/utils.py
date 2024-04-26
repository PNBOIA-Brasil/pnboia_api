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

    def compose_buoy_information(self, setup_buoys, buoy_parameters, buoy_type):
        buoys_information_html = ""

        if buoy_type in ("SPOTTER","TRIAXYS"):
            buoys_information_html += "</ul>"
            return buoys_information_html

        elif buoy_type == "METOCEAN":
            buoys_information_html += "</ul><p>CONFIGURAÇÃO DE SENSORES:</p><ul>"

            if "wspd2" in buoy_parameters:
                buoys_information_html += f"<li>Altura do Anemômetro 1 (sensor 1): {setup_buoys[0].height_anemometer_1} m</li>"
                buoys_information_html += f"<li>Altura do Anemômetro 2 (sensor 2): {setup_buoys[0].height_anemometer_2} m</li>"

            if "cspd1" in buoy_parameters:
                buoys_information_html += f"<li>Tamanho célula ADCP: {setup_buoys[0].cell_size_adcp} m</li>"
                buoys_information_html += f"<li>Profundidade Inicial (limite superior primeira celula) ADCP: {setup_buoys[0].depth_adcp} m</li>"


            buoys_information_html += "</ul>"

        return buoys_information_html

    def list_parameters(self, parameters, buoy_parameters, buoy_type):
        parameters_html = f"""<p>PARAMETROS:</p><ul>"""

        params_dict = {}
        for param in parameters:
            if param.parameter in buoy_parameters:
                params_dict.update({param.id: f"<li>{param.parameter}: {param.description}</li>"})

            if buoy_type == "METOCEAN" and any(item in param.parameter for item in ["cspd", "cdir"]):
                params_dict.update({param.id: f"<li>{param.parameter}: {param.description}</li>"})


        keys_list = list(params_dict.keys())
        keys_list.sort()

        params_dict.update({(max(keys_list) + 1): f'<li>flag_[parâmetro]* : coluna que reúne flags indicativas do controle de qualidade referente ao respectivo parâmetro. A relação de flags pode ser consultada na sessão "CONTROLE DE QUALIDADE".</li></ul>'})

        keys_list = list(params_dict.keys())
        keys_list.sort()

        sorted_params_texts = [params_dict[i] for i in keys_list]
        for text in sorted_params_texts:
            parameters_html += text



        return parameters_html



    def compose_quality_control_section(self):
        quality_control_html = """<p>CONTROLE DE QUALIDADE:</p><ul>
        <li> Flag 0: dado considerado saudável;</li>
        <li> Flag 1  (miss_value, hard flag): valores faltosos (nulos);</li>
        <li> Flag 2 (gross_range, hard flag): valores que estão acima ou abaixo dos limites de detecção do respectivo sensor. Tais valores são filtrados (i.e. transformados em -9999);</li>
        <li> Flag 6 (stuck_sensor, soft flag): marca valores que se repetem 7 vezes consecutivas, indicando possível travamento do sensor naquele período;</li>
        <li> Flag 8 (time_continuity, soft flag): marca valores anômalos em comparação aos valores vizinhos, indicando possível inconsistência temporal;</li>
        <li> Flag 9 (fine_range, soft flag): marca possíveis outliers em relação aos dados históricos (PNBoia) da região da bóia.</li></ul>

        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Detalhes sobre os procedimentos do controle de qualidade podem ser conultados na <a href="https://www.marinha.mil.br/chm/sites/www.marinha.mil.br.chm/files/u1947/controle_de_qualidade_dos_dados.pdf">Documentação do Controle de Qualidade</a>.
        """

        return quality_control_html

    def compose_observations_section(self):
        observations_html = """<p>OBSERVAÇÕES:</p><ul>
  <li> Atentar ao início/fim de cada série temporal, uma vez que podem compreender dados de trajeto do navio de operação de lançamento/recolhimento da boia;</li>
  <li> As soft flags (Flags 6, 8 e 9) são sugestões de controle de qualidade, ficando a cargo do usuário utilizá-las para filtragem dos dados;</li>
        """
        return observations_html

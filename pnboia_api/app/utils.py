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
            filename = buoy_name + "_real_time"

        return filename

    def get_buoy_type(self, buoy_name:str):
        return buoy_name.split(" ")[0]

        #  return buoy_type

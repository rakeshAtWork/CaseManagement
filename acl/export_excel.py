import io
from datetime import datetime
import xlsxwriter
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import logging

User = get_user_model()

logger = logging.getLogger(name="CMS")

MODULES = {"ROLE_MANAGEMENT": {"Role Name": {"value": "role_name"},
                               "Role Description": {"value": "role_description"},
                               "Created On(UTC)": {"value": "created_on"},
                               "Created By": {"value": "created_by"}, "Modified On(UTC)": {"value": "modified_on"},
                               "Modified By": {"value": "modified_by"}},

           "ROLE_PERMISSION": {
               "Privilege Name": {"value": "privilege_name"}, "Privilege Description": {"value": "privilege_desc"}},

           "CLIENT_PRIVILEGE": {"Privilege": {"value": "privilege"}, "Client": {"value": "client"},
                                "Created On(UTC)": {"value": "created_on"},
                                "Created By": {"value": "created_by"}, "Modified On(UTC)": {"value": "modified_on"},
                                "Modified By": {"value": "modified_by"}},

           }


def return_user_info():
    queryset = User.objects.values('id', 'first_name', 'last_name')
    user_dict = {user['id']: f"{user['first_name']} {user['last_name']}".strip() for user in queryset}
    return user_dict


def export_query_to_excel(data, module_name):
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"EXPORT_{module_name}_{now_str}.xlsx"
    headers = MODULES.get(module_name)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Export_Report")

    # Write header row with field names
    header_format = workbook.add_format({'bold': True})
    for col, field in enumerate(headers.keys()):
        worksheet.write(0, col, field, header_format)
    user_info_dict = return_user_info()
    # Write data rows
    for row, item in enumerate(data, start=1):
        for col, header in enumerate(headers.keys()):
            header_value = headers.get(header)
            field = header_value.get("value")
            value = item.get(field)

            if field in ["modified_on", "created_on"] and value:
                try:
                    # Attempt to parse the datetime string as the first format
                    try:
                        parsed_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                    except:
                        parsed_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    value = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    value = str(value)
            elif field in ["modified_by", "created_by"] and isinstance(value, int):
                value = user_info_dict.get(value, value)

            worksheet.write(row, col, value)
    # Close workbook and get output as bytes
    workbook.close()
    excel_data = output.getvalue()

    # Create a response with Excel content type and attachment
    response = HttpResponse(excel_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    response['Access-Control-Allow-Origin'] = '*'
    response["Access-Control-Expose-Headers"] = "*"

    return response

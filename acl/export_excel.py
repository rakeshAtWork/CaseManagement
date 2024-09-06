import io
from datetime import datetime
import xlsxwriter
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import logging

from configuration.models import ColumnConfiguration

User = get_user_model()

logger = logging.getLogger(__name__)

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
           "USER_MANAGEMENT": {
               "User ID": {"value": "id"},
               "Email": {"value": "email"},
               "First Name": {"value": "first_name"},
               "Last Name": {"value": "last_name"},
               "Phone Number": {"value": "phone_number"},
               "Organisation Name": {"value": "organisation_name"},
               "Timezone": {"value": "timezone"},
               "Country": {"value": "country"},
               "Created On(UTC)": {"value": "created_on"},
               "Created By": {"value": "created_by"},
               "Modified On(UTC)": {"value": "modified_on"},
               "Modified By": {"value": "modified_by"},
               "Last Login": {"value": "last_login"},
               "Is Active": {"value": "is_active"},
               "Is Deleted": {"value": "is_delete"}
           },
           'ACTIVITY_LOG_MANAGEMENT': {
               'Module ID': {
                   'value': 'module_id',
                   'header': 'Module ID',
               },
               'User Email ID': {
                   'value': 'user_email_id',
                   'header': 'User Email ID',
               },
               'Column Name': {
                   'value': 'column_name',
                   'header': 'Column Name',
               },
               'Before Input': {
                   'value': 'before_input',
                   'header': 'Before Input',
               },
               'After Input': {
                   'value': 'after_input',
                   'header': 'After Input',
               },
               'Action Type': {
                   'value': 'action_type',
                   'header': 'Action Type',
               },
               'Action By': {
                   'value': 'action_by',
                   'header': 'Action By',
               },
               'Action Date': {
                   'value': 'action_date',
                   'header': 'Action Date',
               },
               'Table Name': {
                   'value': 'table_name',
                   'header': 'Table Name',
               },
               'Description': {
                   'value': 'description',
                   'header': 'Description',
               },
               'IP Address': {
                   'value': 'ip_address',
                   'header': 'IP Address',
               },
               'Remote URL': {
                   'value': 'remote_url',
                   'header': 'Remote URL',
               },
               'User Agent': {
                   'value': 'user_agent',
                   'header': 'User Agent',
               },
               'Created By': {
                   'value': 'created_by',
                   'header': 'Created By',
               },
               'Modified By': {
                   'value': 'modified_by',
                   'header': 'Modified By',
               },
               'Created On': {
                   'value': 'created_on',
                   'header': 'Created On',
               },
               'Modified On': {
                   'value': 'modified_on',
                   'header': 'Modified On',
               },
               'Deleted At': {
                   'value': 'deleted_at',
                   'header': 'Deleted At',
               },
           },
           "LEGAL_ENTITY_MANAGEMENT": {
               "Legal Entity ID": {"value": "legal_entity_id"},
               "Entity Name": {"value": "entity_name"},
               "Street Name": {"value": "street_name"},
               "Zip Code": {"value": "zip_code"},
               "AP Contact Email": {"value": "ap_contact_email"},
               "Business Unit": {"value": "business_unit"},
               "City": {"value": "city"},
               "Company Number": {"value": "company_number"},
               "Country Code": {"value": "country"},
               "Destination Hold": {"value": "destination_hold"},
               "EAN Number": {"value": "ean_number"},
               "Identifier": {"value": "identifier"},
               "Message ID": {"value": "message_id"},
               "Overrule Document Group": {"value": "overrule_document_group"},
               "Review Flag": {"value": "review_flag"},
               "VAT Number": {"value": "vat_number"},
               "Is Active": {"value": "is_active"},
               "Is Deleted": {"value": "is_delete"},
               "Created By": {"value": "created_by"},
               "Modified By": {"value": "modified_by"},
               "Created On(UTC)": {"value": "created_on"},
               "Modified On(UTC)": {"value": "modified_on"}
           },

           }


def return_config(module_id):
    queryset = ColumnConfiguration.objects.filter(module_id=module_id, is_disabled=False).order_by('id').values('label',
                                                                                                          'key')
    user_dict = {config['label']: config["key"].strip() for config in queryset}
    return user_dict


def return_user_info():
    queryset = User.objects.values('id', 'first_name', 'last_name')
    user_dict = {user['id']: f"{user['first_name']} {user['last_name']}".strip() for user in queryset}
    return user_dict


def export_query_to_excel(data, module_name, module_id):
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"EXPORT_{module_name}_{now_str}.xlsx"
    # headers = MODULES.get(module_name)
    headers = return_config(module_id)
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
            # header_value = headers.get(header)
            # field = header_value.get("value")
            field =headers.get(header)
            value = item.get(field)

            if field in ["modified_on", "created_on"] and value:
                try:
                    # Attempt to parse the datetime string as the first format
                    try:
                        parsed_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                    except Exception as e:
                        logger.warning(f'Error at Export as Excel:{str(e)}')
                        parsed_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    value = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    logger.warning(f'Error at Export as Excel:{str(e)}')
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

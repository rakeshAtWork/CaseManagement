from rest_framework.views import exception_handler


def error_handler(exc, context):
    response = exception_handler(exc, context)
    if response and response.status_code == 400:
        try:
            data = response.data
            if isinstance(data, list):
                error = ", ".join(data)
                response.data = {'message': error, "error": data}
            elif isinstance(data, str):
                response.data = {'message': data, "error": data}

            elif isinstance(data, dict):
                try:
                    first_key = list(data.keys())[0]
                    first_value = data[first_key]
                    if first_value and isinstance(first_value, list):
                        message = first_value[0]
                        if isinstance(message, str) and message.startswith(f"This {first_key}"):
                            message = message.replace(f"This ", "")
                        message = message.replace("this", first_key).replace("This", first_key)

                    elif isinstance(first_value, str):
                        message = first_value
                    else:
                        message = "some thing went wrong"

                except Exception:
                    message = "some thing went wrong"

                response.data = {'message': message, "error": response.data}
        except ValueError:
            pass
        except Exception:
            pass
    if response is not None and "detail" in response.data and isinstance(response.data, dict):
        response.data['message'] = response.data.pop('detail')

    return response

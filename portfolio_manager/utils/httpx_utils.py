import httpx


def request(method, url, params=None, data=None, json=None):
    """
    Send an HTTP request.

    Args:
        method (str): The HTTP method (e.g., GET, POST, PUT, DELETE).
        url (str): The URL to send the request to.
        params (dict, optional): The parameters to include in the request. Defaults to None.
        data (dict, optional): The data to include in the request body. Defaults to None.
        json (dict, optional): The JSON data to include in the request body. Defaults to None.

    Returns:
        dict: The JSON response from the request.
    """
    with httpx.Client() as client:
        try:
            response = client.request(method, url, params=params, data=data, json=json)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

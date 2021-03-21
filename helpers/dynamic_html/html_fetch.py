from .Client import Client


def get_dynamic_html(url):
    client_response = Client(url)
    html = str(client_response.mainFrame().toHtml())
    return html

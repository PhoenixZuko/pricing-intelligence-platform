from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    return True  # acceptă orice, Traefik face autentificarea reală

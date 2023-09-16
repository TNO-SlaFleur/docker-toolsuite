import csv

from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection

keycloak_server_url = "http://keycloak.test.nwn-design-toolkit-poc.nl/auth/"
admin_username = 'admin'
admin_password = 'fai'

keycloak_connection = KeycloakOpenIDConnection(
    server_url=keycloak_server_url,
    username=admin_username,
    password=admin_password,
    realm_name="esdl-mapeditor",
    user_realm_name="master")

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

role_name = "Editor"
client_id = keycloak_admin.get_client_id("essim-dashboard")
role = keycloak_admin.get_client_role(client_id=client_id, role_name=role_name)

# Add user
with open('users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    for row in reader:
        print('Generating user', row)
        new_user = keycloak_admin.create_user({
            "email": row['email'],
            "username": row['username'],
            "enabled": True,
            'emailVerified': False,
            "firstName": row['first_name'],
            "lastName": row['last_name'],
            "attributes": {
                "role": "essim"
            },
            "requiredActions": ['VERIFY_EMAIL', 'UPDATE_PASSWORD']
        },
            exist_ok=True)
        user_id = keycloak_admin.get_user_id(row['username'])

        keycloak_admin.assign_client_role(client_id=client_id, user_id=user_id, roles=[role])

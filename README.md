## A proxy for OpenStack Keystone that hides exotic identity providers

### Usage

1. Edit `keystone_babel.py` to match your setup.
2. Start the proxy server via `./keystone_babel.py`
3. Configure your OpenStack client to use the proxy as auth-url:
```
export OS_AUTH_URL="http://127.0.0.1:5000/v3"
export OS_USERNAME="<your_username>"
export OS_PASSWORD="<your_password>"
export OS_TENANT_ID="<your_project_id>"
```

Instead of `OS_TENANT_ID` you can also use:
```
export OS_TENANT_NAME="<your_project_name>"
export OS_PROJECT_DOMAIN_NAME="<your_project_domain>"
```

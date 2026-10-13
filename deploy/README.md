# Ansible Ornipedia

## Setup

### Configure the inventory

Create a file named `inventory.ini` containing the host to use for the deployment.

> An example of this inventory file can be found in [inventory_example.ini](inventory_example.ini).

### Configure the playbooks variables

The confidential variables must be configured in a file named `vault.yml`. An example of this vault file can be found in [vault_example.yml](vars/vault_example.yml).

> [!WARNING]  
> It is highly recommended to encrypt the file `vault.yml` as it contains sensitive data. This can be done through [ansible-vault](https://docs.ansible.com/ansible/2.8/user_guide/vault.html).

The other variables used by the playbooks are located in the folder [vars](./vars/).

## Playbooks

- `api.yml` : deploys the API (FastAPI + Uvicorn + Gunicorn service)
- `front.yml` : deploys the static HTML front
- `certbot.yml` : setup a certbot certificate with autorenew
- `nginx.yml` : setup NGINX to serve the API and front
- `full.yml` : deploys the whole application (performs all the actions of the above playbooks)

## Example usage

```bash
ansible-playbook full.yml -i inventory.ini
```

## Database migrations

The `api.yml` playbook copies the Alembic migrations on the server but does not apply them. After a deployment containing new migrations, run on the server:

```bash
cd ~/ornipedia/api
PYTHONPATH=. venv/bin/alembic upgrade head
```

> [!IMPORTANT]
> The first time, as the database already exists, run `PYTHONPATH=. venv/bin/alembic stamp 0001` before upgrading (see [api/README.md](../api/README.md#database-migrations)).

## GitHub Actions deployment

The [Deploy Front with Ansible](../.github/workflows/deploy-front.yml) workflow builds the front and runs the `front.yml` playbook. It is started manually (`workflow_dispatch`) and uses the following settings of the `production` environment:

| Name | Type | Content |
| --- | --- | --- |
| `SSH_PRIVATE_KEY` | secret | private SSH key used to connect to the server |
| `ANSIBLE_INVENTORY` | secret | content of the `inventory.ini` file |
| `ANSIBLE_VAULT` | secret | content of the `vars/vault.yml` file |
| `ANSIBLE_BECOME_PASSWORD` | secret | sudo password of the remote user (if needed) |
| `VITE_API_URL` | variable | URL of the API used by the front, e.g. `https://my.awesome.host.com/api` |

# Ansible Ornipedia

## Setup

### Configure the inventory

Create a file named `inventory.ini` containing the host to use for the deployment.

> An example of this inventory file can be found in [inventory_example.ini](inventory_example.ini).

### Configure the playbooks variables

The confidential variables must be configured in a file named `vault.yml`. An example of this vault file can be found in [vault_example.yml](vars/vault_example.yml).

> [!WARNING]  
> It is hightly recommended to encrypt the file `vault.yml` as it contains sensitive data. This can be done throught [ansible-vault](https://docs.ansible.com/ansible/2.8/user_guide/vault.html).

The other variables used by the playbooks are located in the folder [vars](./vars/).

## Playbooks

- `api.yml` : deploys the API (FastAPi + Uvicorn + Gunicorn service)
- `front.yml` : deploys the static HTML front
- `certbot.yml` : setup a certbot certificate with autorenew
- `nginx.yml` : setup NGINX to serve the API and front
- `full.yml` : deploys the whole application (performs all the actions of the above playbooks)

## Example usage

```bash
ansible-playbook full.yml -i inventory.ini
```

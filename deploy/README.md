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
ansible-playbook full.yml -i inventory.ini -K
```

`-K` (`--ask-become-pass`) asks for the sudo password of the remote user, needed by the tasks run with `become` (packages, NGINX and systemd files).

## Next instance (next.ornipedia.com)

A second instance of the application, the development version, can be deployed on <https://next.ornipedia.com>, on the same server as the production one. It has its own folder (`~/ornipedia-next`), Gunicorn service (`gunicorn-ornipedia-next`), NGINX site, certificate and database.

The instance is selected by the variables of the inventory, see [inventory_next_example.ini](inventory_next_example.ini):

| Variable | Description | Default |
| --- | --- | --- |
| `ornipedia_instance` | name of the instance (remote folder `~/<name>`, service `gunicorn-<name>`) | `ornipedia` |
| `ornipedia_vault_file` | vault file (in `vars/`) to use | `vault.yml` |
| `ornipedia_run_migrations` | apply the database migrations when deploying the API | `false` |
| `ornipedia_noindex` | add a `X-Robots-Tag: noindex` header (keeps the instance out of search engines) | `false` |
| `ornipedia_img_folder` | folder of the images | `~/<name>/images` |

### First setup

1. Create the DNS record `next.ornipedia.com` pointing to the server (in DigitalOcean, the certificate is obtained with the DigitalOcean DNS plugin).
2. Create the database of the instance, for instance as a copy of the production one (the image paths stored in the database then point to the production images, which are shared):

   ```bash
   createdb ornipedia_next
   pg_dump ornipedia | psql ornipedia_next
   ```

   If the production database has never been migrated with Alembic (no `alembic_version` table), mark the copy as being at the initial schema, so that the migrations applied at each deployment start from there (this is what `alembic stamp 0001` does):

   ```sql
   CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL PRIMARY KEY);
   INSERT INTO alembic_version VALUES ('0001');
   ```

3. Create `inventory_next.ini` from [inventory_next_example.ini](inventory_next_example.ini) and `vars/vault_next.yml` from [vault_example.yml](vars/vault_example.yml) with the credentials of this database.
4. Build the front with the API URL of the instance, then deploy the whole instance (certificate, API, front and NGINX):

   ```bash
   (cd ../front && VITE_API_URL=https://next.ornipedia.com/api npm run build:prod)
   ansible-playbook full.yml -i inventory_next.ini -K
   ```

### Continuous deployment

The [Deploy Next](../.github/workflows/deploy-next.yml) workflow deploys the API and the front on the next instance at each push on the `next` branch. It can also be started manually for any branch (Actions > Deploy Next > Run workflow).

It uses the same secrets as the [GitHub Actions deployment](#github-actions-deployment), defined in a GitHub environment named `next`:

- `ANSIBLE_INVENTORY`: content of `inventory_next.ini`
- `ANSIBLE_VAULT`: content of `vars/vault_next.yml`
- `SSH_PRIVATE_KEY` and `ANSIBLE_BECOME_PASSWORD`: same as the production ones
- `VITE_API_URL` (variable, optional): defaults to `https://next.ornipedia.com/api`

## Administration

The administration page (`/admin`) is enabled by setting `vault_admin_password` in the vault of the instance (see [vault_example.yml](vars/vault_example.yml)); it is disabled when the variable is missing. For the GitHub Actions deployments, add it to the `ANSIBLE_VAULT` secret of the environment.

## Database migrations

The `api.yml` playbook copies the Alembic migrations on the server but only applies them when `ornipedia_run_migrations` is enabled (as for the next instance). For the production instance, after a deployment containing new migrations, run on the server:

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

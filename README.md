# Django Zato Example: Proof of concept

## Development setup
* Ubuntu Server 14.04 LTS (Trusty) amd64 Virtual Machine running in Hyper-V on Windows 8 Pro
* Packages / software:
    1. Postgresql 9.3: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04
    2. Redis (Latest): http://tosbourn.com/install-latest-version-redis-ubuntu/
    3. Zato: https://zato.io/docs/admin/guide/install-ubuntu.html
* Configuration:
    1. Configure PostgreSQL user (e.g. "zato") and a database for this user (e.g. "django-zato-db")
    2. Configure Zato project (quickstart): https://zato.io/docs/admin/cli/quickstart-create.html
    3. Configure Zato services that will be used in the Django Zato Example project: https://zato.io/blog/posts/django-web-services-integration.html
    4. Do not use the exchangerates.py script in the previous link, use the one that can be found in this repo under "services". Deploy that script.
    5. Check and update Zato configuration parameters, see application/settings.py in this repo
* Run django service and go to http://localhost:8000 (or whatever url your django service is running on)
* Profit!
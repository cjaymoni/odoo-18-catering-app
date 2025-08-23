FROM odoo:18.0

USER root
# Install Twilio SDK; Flask is not required since Odoo serves webhooks itself
RUN python3 -m pip install --no-cache-dir --break-system-packages twilio

USER odoo

FROM bitnami/odoo:16.0.20240415-debian-12-r0
RUN apt-get update
COPY requirements.txt /opt/bitnami/odoo/
ENV VIRTUAL_ENV=/opt/bitnami/odoo/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r /opt/bitnami/odoo/requirements.txt
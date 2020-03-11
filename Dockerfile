FROM python:3
ARG ssh_prv_key
ARG ssh_pub_key
ARG ssh_host_ip

# Authorize SSH Host
RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh && ssh-keyscan "$ssh_host_ip" > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

# Avoid cache purge by adding requirements first
ADD ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt
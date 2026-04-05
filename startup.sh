#!/bin/bash
# Install Microsoft repo
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install the ODBC driver
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18

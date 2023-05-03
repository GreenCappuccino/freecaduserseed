#!/bin/sh

podman cp ./seedimport.php phpbb_phpbb_1:/opt/bitnami/phpbb
podman cp ../phpbb_export.csv phpbb_phpbb_1:/opt/bitnami/phpbb
podman exec -t -i phpbb_phpbb_1 php /opt/bitnami/phpbb/seedimport.php

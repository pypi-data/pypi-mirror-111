#!/bin/bash

set -ex

function prepare_environment() {
    : ${MY_IP:=0.0.0.0}
}

function setup_gitea() {
    local serial=$1
    
    docker run --rm --name gitea$serial -p 878$serial:3000 -p 272$serial -d gitea/gitea:1.14.2

    success=false
    for delay in 15 15 15 15 15 30 30 30 30 30 30 ; do
	if curl --fail --verbose --data-binary "db_type=SQLite3&db_host=localhost%3A3306&db_user=root&db_passwd=&db_name=gitea&ssl_mode=disable&db_schema=&charset=utf8&db_path=%2Fdata%2Fgitea%2Fgitea.db&app_name=Gitea%3A+Git+with+a+cup+of+tea&repo_root_path=%2Fdata%2Fgit%2Frepositories&lfs_root_path=%2Fdata%2Fgit%2Flfs&run_user=git&domain=${MY_IP}&ssh_port=22&http_port=3000&app_url=http%3A%2F%2F${MY_IP}%3A878${serial}%2F&log_root_path=%2Fdata%2Fgitea%2Flog&smtp_host=&smtp_from=&smtp_user=&smtp_passwd=&enable_federated_avatar=on&no_reply_address=&password_algorithm=pbkdf2&admin_name=gitea_admin&admin_passwd=admin123&admin_confirm_passwd=admin123&admin_email=admin@example.com" http://${MY_IP}:878$serial/ ; then
	    success=true
	    break
	fi
	sleep $delay
    done
    $success
}

function setup() {
    local serial
    for serial in 1 2 ; do
	setup_gitea $serial
    done
}

function teardown() {
    local serial
    for serial in 1 2 ; do
	docker stop gitea$serial || true
    done
}

for f in prepare_environment ${@:-teardown setup} ; do
    $f
done

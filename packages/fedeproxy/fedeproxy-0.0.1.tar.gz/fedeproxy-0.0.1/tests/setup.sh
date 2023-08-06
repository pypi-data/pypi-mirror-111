#!/bin/bash

set -e

tests/setup-gitlab.sh "$@"
tests/setup-gitea.sh "$@"

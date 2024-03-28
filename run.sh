#!/bin/bash
docker run --rm -v $PWD:/app -p 8080:8080 ds-backend

#!/bin/bash
LAMBDA_FUNC="programmers_lambda_api"
sudo zip -r programmers_lambda_api.zip ./url/*
sudo aws lambda update-function-code --function-name $LAMBDA_FUNC --zip-file fileb://programmers_lambda_api.zip
sudo rm programmers_lambda_api.zip

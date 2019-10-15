#!/bin/bash
LAMBDA_FUNC="aws_lambda_api"
sudo zip -r aws_lambda_api.zip ./url/*
sudo aws lambda update-function-code --function-name $LAMBDA_FUNC --zip-file fileb://aws_lambda_api.zip
sudo rm aws_lambda_api.zip

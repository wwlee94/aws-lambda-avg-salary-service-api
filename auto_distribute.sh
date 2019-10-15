#!/bin/bash
LAMBDA_FUNC="programmers_avgSalaryService_api"
FILE_NAME=$LAMBDA_FUNC'.zip'
sudo zip -r $FILE_NAME ./src/*
sudo aws lambda update-function-code --function-name $LAMBDA_FUNC --zip-file fileb://programmers_avgSalaryService_api.zip
sudo rm './'$FILE_NAME

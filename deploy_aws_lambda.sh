source .env

aws lambda update-function-code --function-name ScrapePushReddit --image-uri $AWS_ECR/data_scrape_pipeline:latest

aws lambda update-function-code --function-name TransformLoadDB --image-uri $AWS_ECR/data_prep_pipeline:latest

aws lambda update-function-code --function-name PredictSentimentML --image-uri $AWS_ECR/ml_predict:latest
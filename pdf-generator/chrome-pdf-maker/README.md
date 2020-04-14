### Lambda which runs headless Chrome to generate pdf from url
- Uses [Chrome Lambda layer](https://github.com/shelfio/chrome-aws-lambda-layer) to keep Lambda function size manageable
- Triggered by SNS message containing the URL e.g `aws sns publish --topic-arn 'arn:aws:sns:ap-south-1:691823188847:c19-pdf-channel' --message '"https://c19.zyxw365.in/pdfs/batch_24x60.html"'`
- Saves PDF to S3

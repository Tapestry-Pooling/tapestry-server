    const chromium = require('chrome-aws-lambda');
    const AWS = require('aws-sdk');
    const S3 = new AWS.S3({
        signatureVersion: 'v4',
        region: process.env.REGION
    });

    exports.handler = async(event, context) => {
        console.log("Event : " + JSON.stringify(event));
        let result = null;
        let browser = null;
        if (event.hasOwnProperty("Records")) {
            try {
                var url = event.Records[0].Sns.Message.replace(/"/g, '');
                url
                if (url.startsWith("https://")) {
                    browser = await chromium.puppeteer.launch({
                        args: chromium.args,
                        defaultViewport: chromium.defaultViewport,
                        executablePath: await chromium.executablePath,
                        headless: chromium.headless,
                    });

                    let page = await browser.newPage();
                    await page.goto(url, {
                        waitUntil: ["networkidle0", "load", "domcontentloaded"]
                    });
                    let keyName = "batch_" + url.split("batch_")[1].split(".")[0] + ".pdf";

                    let pdfStream = await page.pdf();
                    const s3Params = {
                        Bucket: process.env.BUCKET,
                        Key: keyName,
                        Body: pdfStream,
                        ContentType: "application/pdf",
                        ACL: "public-read",
                        
                    };
                    result = await S3.putObject(s3Params).promise();
                }

            }
            catch (error) {
                return context.fail(error);
            }
            finally {
                if (browser !== null) {
                    await browser.close();
                }
            }
        }

        return context.succeed(result);
    };

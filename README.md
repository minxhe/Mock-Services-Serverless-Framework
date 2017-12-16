# Mock-Services-Serverless-Framework
A service factory designed to improve the workflow of automations by mocking 3rd party services (eg. [Appboy](https://www.appboy.com/), [Paypal](https://www.paypal.com/)) using [Python 2.7](https://www.python.org/download/releases/2.7/), Serverless Framework, [AWS Lambda](https://aws.amazon.com/lambda/) and [DynamoDB](https://aws.amazon.com/dynamodb/).
### Overview:
#### Main idea: 
By modifying part of the request body sent to 3rd party service, to obtain the result you expect in order to effectly test your backend services. (Mostly edge cases or rare occuring cases)
#### Example:
##### To Test Error Handling on Payouts "PENDING" State of [Paypal Batch Payouts Endpoint](https://developer.paypal.com/docs/api/payments.payouts-batch/)
Mock reqeust body:
```
{
  "sender_batch_header": {
  "sender_batch_id": "PENDING",
  "email_subject": "You have a payout!"
  },
  "items": []
}
```
Mock reponse data: 
```
{
  "batch_header": {
    "sender_batch_header": {
      "sender_batch_id": "2014021801",
      "email_subject": "You have a payout!"
    },
    "payout_batch_id": "12345678",
    "batch_status": "PENDING"
  }
}
```

### Requirements:
  * [Serverless Framework](https://serverless.com/)
  ```
  npm install -g serverless
  ```
  * [AWS profile](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
### Deploy to AWS Stack
  * Clone the repository
  * Navigate to one of the services
  * Deploy with
  ```
  serverlss deploy --aws-profile <profile_name> (default is "default")
  ```
  * You should see your API endpoints at the end of the deployment
### Logs:
Go into the directory of a specific mock service
```
serverless logs -f <function_name> -t --aws-profile <profile_name> --stage-<stage_name>
```

# Automatically Tagging The New Created Resources via Lambda

## Driver

In essence, all the resources (specifically for EC2) will be tagged whenever they created via two different ways.

- If the EC2 instances created by [Morpheus](https://morpheus.tcb.rctops.com/) then they will be tagged via the same pipeline.
- However, if the EC2 instances are not created by [Morpheus](https://morpheus.tcb.rctops.com/) then they will be tagged by the separated script. For instance, all the EC2 instances for the DR drill or even real DR event that created by the separated scripts as well as their tags.

There is one thing that has not been covered: **if the EC2 instances are not created by the user account(s), the service account(s) instead** (ex: Rubrik Converter). Although we do know the most ideal way to make it in place is that to modify the source code, however, it cannot be achieved all the time (ex: Rubrik Support has confirmed that the custom tags cannot be attached to the Rubrik converter yet according to the feedback by November 2020).

Since all the resources have to be tagged with pre-defined MAP (Migration Acceleration Program) tags - `map-migrated` and `map-migrated-app`, otherwise, those resources would not have any discounts that we dealt with AWS. For this reason, we need an event-triggered pipeline to verify if those MAP relevant tags do not exist on any of the EC2 instances then attach them afterward. That is why Lambda comes up.

## Workflow

The below summary is excerpted by [Automatically Tag AWS EC2 Instances and Volumes](https://blog.doit-intl.com/automatically-tag-aws-ec2-instances-and-volumes-753dcaa7d7b0) and it certainly presents a clear view of the whole event-triggered pipeline. My Lambda function code refers to his [code](https://github.com/doitintl/ec2-auto-tag/blob/master/lambda_function.py) as well.

![auto-tagging](https://i.imgur.com/aAxL4xT.png)

1. A user creates an EC2 instance.
2. CloudTrail tracks that API call and shouts EventBridge.
![cloudtrail](https://i.imgur.com/9JHrI64.png)
3. EventBridge triggers the Lambda function code to attach all the required tags to that EC2 instance and its EBS volume(s) afterward.
![cloudwatch](https://i.imgur.com/hBEISRQ.png)

## References
- [Automatically Tag AWS EC2 Instances and Volumes](https://blog.doit-intl.com/automatically-tag-aws-ec2-instances-and-volumes-753dcaa7d7b0)
- [Automatically tag new AWS resources based on identity or role](https://aws.amazon.com/blogs/mt/auto-tag-aws-resources/)

:::info
###### tags: `Internal` `AWS` `Automation` `Lambda` `Python`
:::

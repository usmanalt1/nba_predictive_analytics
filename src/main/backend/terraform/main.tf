provider "aws" {
  region = "eu-west-2"
}

resource "aws_iam_user" "morning_analytics" {
  name = "morning_analytics"
}

output "iam_user_id" {
  value = aws_iam_user.morning_analytics.id
}

resource "aws_iam_policy" "access_policy" {
  name        = "AccessPolicy"
  description = "Allows morning_analytics user to main services"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action = "s3:*",
      Resource = "*"
    },
    {
      "Effect": "Allow",
      "Action": "rds:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "rds-db:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "cloudwatch:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "sqs:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "sns:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "autoscaling:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "elasticloadbalancing:*",
      "Resource": "*"
    }
    ]})
}



resource "aws_iam_user_policy_attachment" "access_policy" {
  user       = "morning_analytics"  # Replace with your IAM username
  policy_arn = aws_iam_policy.access_policy.arn
}
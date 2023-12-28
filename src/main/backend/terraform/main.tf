provider "aws" {
  region = "eu-west-2"
}

resource "aws_iam_user" "morning_analytics" {
  name = "morning_analytics"
}

output "iam_user_id" {
  value = aws_iam_user.morning_analytics.id
}

resource "aws_iam_policy" "s3_access_policy" {
  name        = "S3AccessPolicy"
  description = "Allows morning_analytics user to upload objects to S3"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      Resource = [
        "arn:aws:s3:::your-bucket-name",  
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }]
  })
}

resource "aws_iam_user_policy_attachment" "attach_s3_policy" {
  user       = "morning_analytics"  # Replace with your IAM username
  policy_arn = aws_iam_policy.s3_access_policy.arn
}
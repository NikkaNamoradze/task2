# Task 2 - S3 Bucket Policy Check & Creation

CLI program that checks if a bucket has a policy. If a policy exists, it prints it. Otherwise, it creates a public read policy for `/dev/*` and `/test/*` prefixes.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your AWS credentials in .env
```

## Usage

```bash
python main.py <bucket_name>
```

### Examples

```bash
# Check/create policy for a bucket
python main.py my-unique-bucket
```

## How it works

1. Initializes S3 client using credentials from `.env`
2. Attempts to retrieve the existing bucket policy
3. If policy exists — prints the current policy
4. If no policy — removes public access block and creates a new policy that grants public read (`s3:GetObject`) on:
   - `arn:aws:s3:::<bucket>/dev/*`
   - `arn:aws:s3:::<bucket>/test/*`

## Generated Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadDev",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<bucket>/dev/*"
    },
    {
      "Sid": "PublicReadTest",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<bucket>/test/*"
    }
  ]
}
```

# Task 2 - S3 Bucket Policy Check & Creation

CLI program that checks if a bucket has a policy. If a policy exists, it prints it. Otherwise, it creates a public read policy for `/dev/*` and `/test/*` prefixes.

## Setup

```bash
pip install boto3 python-dotenv
```

შექმენით `.env` ფაილი პროექტის root-ში:

```
aws_access_key_id=YOUR_ACCESS_KEY_ID
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
aws_session_token=YOUR_SESSION_TOKEN
aws_region_name=us-west-2
```

## Usage

```bash
python main.py <bucket_name>
```

## Testing

### წინაპირობა

Bucket უკვე უნდა არსებობდეს. შეგიძლიათ შექმნათ task1-ით ან AWS Console-დან.

### 1. Policy-ის შექმნა (policy არ არსებობს)

```bash
python main.py my-test-bucket-12345
```

მოსალოდნელი output:
```
No policy found. Creating public read policy for /dev/* and /test/*...
Policy created successfully for 'my-test-bucket-12345':
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadDev",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-test-bucket-12345/dev/*"
    },
    {
      "Sid": "PublicReadTest",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-test-bucket-12345/test/*"
    }
  ]
}
```

### 2. Policy უკვე არსებობს

გაუშვით იგივე ბრძანება მეორეჯერ:

```bash
python main.py my-test-bucket-12345
```

მოსალოდნელი output:
```
Bucket 'my-test-bucket-12345' already has a policy:
{
  ...
}
```

### 3. სრული ტესტი task1-თან ერთად

```bash
# ჯერ შევქმნათ bucket (task1)
cd ../task1
python main.py my-policy-test-bucket

# შემდეგ მივანიჭოთ policy (task2)
cd ../task2
python main.py my-policy-test-bucket

# გავუშვათ ხელახლა — უკვე არსებობს
python main.py my-policy-test-bucket
```

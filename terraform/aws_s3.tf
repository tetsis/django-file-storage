resource "aws_s3_bucket" "s3_main" {
    bucket = "${var.bucket_name}"
    acl = "private"
}

#AWS Settings
variable "access_key" {}
variable "secret_key" {}
variable "region" {}

#App Name
variable "app_name" {}

#Segment Settings
variable "root_segment" {}
variable "public_segment1" {}
variable "public_segment2" {}
variable "private_segment1" {}
variable "private_segment2" {}

#AZ Settings
variable "public_segment1_az" {}
variable "public_segment2_az" {}
variable "private_segment1_az" {}
variable "private_segment2_az" {}

#Security Group Settings
variable "ssh_allow_ip" {}

#KeyPair Settings
variable "my_public_key" {}

#DB Settings
variable "db_name" {}
variable "db_username" {}
variable "db_password" {}

#S3 Settings
variable "bucket_name" {}

#####################################
# EC2 Settings
#####################################
resource "aws_instance" "app_main" {
    ami           = "ami-0a2de1c3b415889d2"
    associate_public_ip_address = "true"
    instance_type = "t2.micro"
    key_name      = "${var.my_public_key}"
    subnet_id     = "${aws_subnet.vpc_main-public-subnet1.id}"
    vpc_security_group_ids = ["${aws_security_group.app_sg.id}"]

    tags = {
        Name = "${var.app_name} instance"
    }
}


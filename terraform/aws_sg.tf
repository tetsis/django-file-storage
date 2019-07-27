#####################################
# Security Group Settings
#####################################
resource "aws_security_group" "app_sg" {
    name = "app_sg"
    vpc_id = "${aws_vpc.vpc_main.id}"
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["${var.ssh_allow_ip}"]
    }
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["${var.ssh_allow_ip}"]
    }
    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["${var.ssh_allow_ip}"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    description = "allow 22/tcp, 80/tcp, 443/tcp"

    tags = {
        Name = "${var.app_name} app_sg"
    }
}

resource "aws_security_group" "db_sg" {
    name = "db_sg"
    vpc_id = "${aws_vpc.vpc_main.id}"
    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks = ["${var.public_segment1}", "${var.public_segment2}"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    description = "allow 5432/tcp (PostgreSQL) from public subnets"

    tags = {
        Name = "${var.app_name} db_sg"
    }
}

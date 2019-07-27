#####################################
# RDS Settings
#####################################
resource "aws_db_subnet_group" "rds_main" {
    name = "rds_main"
    description = "${var.app_name} MultiAZ"
    subnet_ids = ["${aws_subnet.vpc_main-private-subnet1.id}", "${aws_subnet.vpc_main-private-subnet2.id}"]

    tags = {
        Name = "${var.app_name} db_subnet_group"
    }
}

resource "aws_db_parameter_group" "rds_main" {
    name = "rds-main"
    family = "postgres9.6"
    description = "rds_main"
}

resource "aws_db_instance" "rds_main" {
    allocated_storage      = 20
    storage_type           = "gp2"
    engine                 = "postgres"
    engine_version         = "9.6"
    instance_class         = "db.t2.micro"
    name                   = "${var.db_name}"
    username               = "${var.db_username}"
    password               = "${var.db_password}"
    parameter_group_name   = "${aws_db_parameter_group.rds_main.name}"
    vpc_security_group_ids = ["${aws_security_group.db_sg.id}"]
    db_subnet_group_name   = "${aws_db_subnet_group.rds_main.name}"
}

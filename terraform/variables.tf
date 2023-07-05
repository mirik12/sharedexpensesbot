variable "region" {
  description = "AWS region"
}

variable "vpc_name" {
  description = "Name of the VPC"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
}

variable "availability_zones" {
  description = "Availability zones for VPC"
  type        = list(string)
}

variable "vpc_private_subnets" {
  description = "Private subnets for the VPC"
  type        = list(string)
}

variable "vpc_public_subnets" {
  description = "Public subnets for the VPC"
  type        = list(string)
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
}

variable "cluster_version" {
  description = "Kubernetes version"
}

variable "desired_nodes_capacity" {
  description = "Number of desired nodes in EKS node group"
}

variable "max_nodes_capacity" {
  description = "Maximum number of nodes in EKS node group"
}

variable "min_nodes_capacity" {
  description = "Minimum number of nodes in EKS node group"
}

variable "node_instance_type" {
  description = "Instance type of the EKS worker nodes"
}

variable "key_name" {
  description = "Name of the EC2 key pair"
}

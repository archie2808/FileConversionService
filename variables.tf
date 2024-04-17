
variable "vpc_id" {
  description = "The ID of the VPC where the EKS cluster will be deployed."
  type        = string
  default = "vpc-05a6869946d549a07"
}

variable "subnets" {
  description = "The list of subnet IDs where the EKS cluster will be deployed."
  type        = list(string)
}

variable "cluster_name" {
  description = "Name of cluster."
  type        = string
  default = ["subnet-12345abcde", "subnet-67890fghij"]
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "A list of public subnet CIDRs."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}
variable "kubernetes_version" {
    description = "The Kubernetes version."
    type        = string
    default     = "1.29"
}
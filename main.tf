
module "eks_cluster" {
  source = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  kubernetes_version = var.kubernetes_version
  subnets         = var.subnets
  vpc_id          = var.vpc_id

  node_groups = {
    my-node-group = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1

      instance_type = "t2.micro"
      #key_name      = var.key_name
    }
  }
  

}



module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "14.0.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  subnets         = module.vpc.private_subnets

  node_groups = {
    eks_nodes = {
      desired_capacity = var.desired_nodes_capacity
      max_capacity     = var.max_nodes_capacity
      min_capacity     = var.min_nodes_capacity

      instance_type = var.node_instance_type
      key_name      = var.key_name

      additional_tags = {
        Environment = "test"
        Name        = "eks-worker-node"
      }
    }
  }

  manage_aws_auth = true

  write_kubeconfig   = true
  config_output_path = "./"

  map_roles    = []
  map_users    = []
  map_accounts = []
}

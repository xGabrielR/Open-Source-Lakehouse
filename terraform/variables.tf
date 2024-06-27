variable "bucket_names" {
  type        = list(string)
  description = "Aws default buckets"
  default = [
    "landing",   # dms data store
    "bronze",    # bronze iceberg
    "silver",    # silver iceberg
    "gold",      # gold iceberg
    "analytics", # feature store and abt
    "scripts",   # scripts and features
    "artifacts", # mlflow artifacts
    "trino"      # default trino bucket
  ]
}

variable "prefix" {
  type        = string
  default     = "grc"
  description = "Default prefix"
}

locals {
  prefix = var.prefix
  common_tags = {
    Project     = "grc-lakehouse"
    Terraform   = true
    Environment = "dev"
  }
}

terraform {
  required_providers {
    minio = {
      source = "refaktory/minio"
    }
  }
}

provider "minio" {
  endpoint   = "localhost:9000"
  access_key = "adm_minio"
  secret_key = "adm_minio"
  ssl        = false
}

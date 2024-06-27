resource "minio_bucket" "bucket" {
  count = length(var.bucket_names)
  name  = "${var.prefix}-lh-${var.bucket_names[count.index]}"
}

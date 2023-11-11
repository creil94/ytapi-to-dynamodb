resource "docker_image" "lambda_image" {
  name = "lambda_image"
  build {
    context = "../."
    tag     = ["lambda_image:latest"]
  }
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "../functions/**") : filesha1(f)]))
  }
}
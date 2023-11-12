resource "docker_image" "lambda_image" {
  name = "${aws_ecr_repository.lambda-functions-ecr.repository_url}:latest"
  build {
    context = "../."
    platform = "linux/amd64"
  }

  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "../functions/**") : filesha1(f)]))
  }
}

resource "docker_registry_image" "lambda-image-remote" {
  name          = docker_image.lambda_image.name
  keep_remotely = true

  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "../functions/**") : filesha1(f)]))
  }
}
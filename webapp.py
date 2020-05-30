


docker_command = 'sudo docker stats --no-stream --no-trunc --format "{}"'.format(cls.COMMAND_FORMAT)
docker stats --no-stream \
  --format "{\"container\": \"{{ .Container }}\", \"memory\": { \"raw\": \"{{ .MemUsage }}\", \"percent\": \"{{ .MemPerc }}\"}, \"cpu\": \"{{ .CPUPerc }}\"}"

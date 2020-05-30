# -*- coding: utf-8 -*-
import os
import fire
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


cpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
supervisor_path = os.path.join(cpath, "supervisor")
if not os.path.exists(supervisor_path):
    os.makedirs(supervisor_path)


def gen_conf(path_prefix, project_name="metrics_exporter", port=5555, docker=False):
    deploy_path = path_prefix + "/" + project_name if not docker else "/metrics_exporter"

    supervisor_config = configparser.ConfigParser()

    supervisor_config.add_section("unix_http_server")
    supervisor_config.set("unix_http_server", "file", "/tmp/{}.sock".format(project_name))

    supervisor_config.add_section("supervisord")
    supervisor_config.set("supervisord", "pidfile", "/tmp/{}.pid".format(project_name))
    supervisor_config.set("supervisord", "nodaemon", "false")

    supervisor_config.add_section("rpcinterface:supervisor")
    supervisor_config.set("rpcinterface:supervisor", "supervisor.rpcinterface_factory", "supervisor.rpcinterface:make_main_rpcinterface")

    supervisor_config.add_section("supervisorctl")
    supervisor_config.set("supervisorctl", "serverurl", "unix:///tmp/{}.sock".format(project_name))

    program_name = "program:{}".format(project_name)
    supervisor_config.add_section(program_name)
    cmd = "{}/pyenv/bin/gunicorn".format(deploy_path) if not docker else "gunicorn"
    supervisor_config.set(program_name, "command",
                          "{} -w 1 -b 0.0.0.0:{} "
                          "--access-logfile {}/logs/access.log app.webapp:app".format(cmd, port, deploy_path))
    supervisor_config.set(program_name, "directory", deploy_path)
    supervisor_config.set(program_name, "redirect_stderr", "true")
    supervisor_config.set(program_name, "stdout_logfile", "{}/logs/supervisor.log".format(deploy_path))
    supervisor_config.set(program_name, "stdout_logfile_backups", 2)

    with open(os.path.join(supervisor_path, "supervisord.conf"), "w") as f:
        supervisor_config.write(f)


if __name__ == "__main__":
    fire.Fire()
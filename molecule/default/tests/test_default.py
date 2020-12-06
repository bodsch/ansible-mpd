import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    return ansible_vars


@pytest.mark.parametrize("dirs", [
    "/var/lib/mpd",
    "/run/mpd"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/mpd.conf",
    "/var/lib/mpd/tag_cache",
    "/var/lib/mpd/sticker.sql",
])
def test_files(host, files):
    f = host.file(files)
    assert f.is_file
    assert f.exists


def test_user(host):
    assert host.user("mpd").exists
    assert host.group("audio").exists
    assert "audio" in host.user("mpd").groups


def test_service(host):
    service = host.service("mpd")
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize("ports", [
    '0.0.0.0:6600',
])
def test_open_port(host, ports):

    for i in host.socket.get_listening_sockets():
        print(i)

    solr = host.socket("tcp://{}".format(ports))
    assert solr.is_listening

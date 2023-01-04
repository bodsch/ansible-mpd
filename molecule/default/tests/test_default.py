
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def pp_json(json_thing, sort=True, indents=2):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def base_directory():
    cwd = os.getcwd()

    if ('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


def read_ansible_yaml(file_name, role_name):
    ext_arr = ["yml", "yaml"]

    read_file = None

    for e in ext_arr:
        test_file = "{}.{}".format(file_name, e)
        if os.path.isfile(test_file):
            read_file = test_file
            break

    return "file={} name={}".format(read_file, role_name)


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution

    if distribution in ['debian', 'ubuntu']:
        os = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        os = "redhat"
    elif distribution in ['arch']:
        os = "archlinux"

    print(" -> {} / {}".format(distribution, os))

    file_defaults = read_ansible_yaml("{}/defaults/main".format(base_dir), "role_defaults")
    file_vars = read_ansible_yaml("{}/vars/main".format(base_dir), "role_vars")
    file_distibution = read_ansible_yaml("{}/vars/{}".format(base_dir, os), "role_distibution")
    file_molecule = read_ansible_yaml("{}/group_vars/all/vars".format(molecule_dir), "test_vars")

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


@pytest.mark.parametrize("dirs", [
    "/var/lib/mpd/playlists",
    "/var/lib/mpd",
    "/run/mpd",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/mpd.conf",
    "/var/lib/mpd/tag_cache",
    "/var/lib/mpd/sticker.sql",
    "/var/lib/mpd/playlists/gothic.m3u",
    "/var/lib/mpd/playlists/studio_bruessel.m3u"
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

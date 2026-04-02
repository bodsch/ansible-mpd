# coding: utf-8
from __future__ import annotations, unicode_literals

import os
import pytest

import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

# --- tests -----------------------------------------------------------------



@pytest.mark.parametrize(
    "dirs",
    [
        "/var/lib/mpd/playlists",
        "/var/lib/mpd",
        "/run/mpd",
    ],
)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory


@pytest.mark.parametrize(
    "files",
    [
        "/etc/mpd.conf",
        "/var/lib/mpd/tag_cache",
        "/var/lib/mpd/sticker.sql",
        "/var/lib/mpd/playlists/gothic.m3u",
        "/var/lib/mpd/playlists/studio_bruessel.m3u",
    ],
)
def test_files(host, files):
    f = host.file(files)
    assert f.is_file


def test_user(host):
    assert host.user("mpd").exists
    assert host.group("audio").exists
    assert "audio" in host.user("mpd").groups


def test_service(host):
    service = host.service("mpd")
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize(
    "ports",
    [
        "0.0.0.0:6600",
    ],
)
def test_open_port(host, ports):

    for i in host.socket.get_listening_sockets():
        print(i)

    srv = host.socket(f"tcp://{ports}")
    assert srv.is_listening

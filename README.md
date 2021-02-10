
Ansible role to setup mpd (Music Player Daemon)

The command line interface [mpc](https://www.musicpd.org/clients/mpc/) is only available on Debian based systems, sorry.

![Build](https://github.com/bodsch/ansible-mpd/workflows/Build/badge.svg)

## usage

```
mpd_outputs:
  - name: "Null Output"
    type: "null"

mpd_inputs:
  curl:
    verify_peer: "yes"
    verify_host: "yes"
    # proxy: "proxy.isp.com:8080"
    # proxy_user: "user"
    # proxy_password: "password"

mpd_database: {}
#  plugin: "proxy"
#  host: "other.mpd.host"
#  port: "6600"

mpd_name: Mediabox Player
mpd_restore_paused: true
mpd_auto_update: true
mpd_follow_inside_symlinks: true
mpd_follow_outside_symlinks: false

mpd_zeroconf:
  enabled: true
  name: "Music Player"

mpd_music_directory: /var/lib/mpd/music
mpd_playlist_directory: /var/lib/mpd/playlists

mpd_db_file: /var/lib/mpd/tag_cache
mpd_sticker_file: /var/lib/mpd/sticker.sql
mpd_state_file: /var/lib/mpd/state
mpd_pid_file: /run/mpd/pid

mpd_log_file: /var/log/mpd/mpd.log

# Available setting arguments are
# "default", "secure" or "verbose"
mpd_log_level: default

mpd_user: mpd

mpd_bind_to_address: '0.0.0.0'
mpd_port: 6600

mpd_radiostations: []

mpd_alarm_clock: {}
```

### Outputs

```
mpd_outputs:
  - name: "Null Output"
    type: "null"
  - name: "Pulse Output"
    type: "pulse"
  - name: "Alsa Output"
    type: "alsa"
    device: "hw:0,0"
    mixer_type: "hardware"   # optional
    mixer_device: "default"  # optional
    mixer_control: "PCM"     # optional
    mixer_index: "0"         # optional
```

### Inputs 

```
mpd_inputs:
  curl:
    enabled: true
    verify_peer: "yes"
    verify_host: "yes"
    # proxy: "proxy.isp.com:8080"
    # proxy_user: "user"
    # proxy_password: "password"
  qobuz:
    enabled: false
    app_id: "ID"
    # app_secret: "SECRET"
    # username: "USERNAME"
    # password: "PASSWORD"
    # format_id: "N"
  tidal:
    enabled: false
    token: "TOKEN"
    # username: "USERNAME"
    # password: "PASSWORD"
    # audioquality: "Q"
```

### Radiostations

```
mpd_radiostations:
  - name: "Vox Noctem"
    url: http://r2d2.voxnoctem.com:8000/voxnoctem.mp3
```

### alarm clock

```
mpd_used_cron_daemon: "{{ 'cron' if ansible_os_family | lower == 'debian' else 'cronie' }}"

mpd_alarm_clock:
  enable: true
  radiostation: 'Vox Noctem'
  cron_start:
    enable: true
    minute: 55
    hour: 5
    weekday: 1-5
  cron_stop:
    enable: true
    minute: 58
    hour: 6
```


## tests

for testing

```
tox -e py38-ansible29 -- molecule test
```

## Troubleshooting & Known issues



## License

Apache 2.0

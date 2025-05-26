# blink(1) Integration<a name="blink1-integration"></a>

<!-- mdformat-toc start --slug=github --maxlevel=3 --minlevel=2 -->

- [Installation](#installation)
- [Configuration](#configuration)
- [References](#references)
  - [Links to blink(1) resources](#links-to-blink1-resources)

<!-- mdformat-toc end -->

This integration sets up and uses a [blink(1)](https://blink1.thingm.com) USB status led for use within Home Assistant. The LED dongle can be directly connected to the Home Assistant Host's USB bus or to another computer running the blink(1) [blink1control](https://blink1.thingm.com/blink1control/), which can be [downloaded from GitHub](https://github.com/todbot/Blink1Control2) (via API access enabled).

______________________________________________________________________

## Installation<a name="installation"></a>

tbd

## Configuration<a name="configuration"></a>

tbd

## References<a name="references"></a>

### Links to blink(1) resources<a name="links-to-blink1-resources"></a>

- [URL API for blink(1) Applications](https://github.com/todbot/blink1/blob/main/docs/app-url-api.md)
- [Examples of the blink(1) application URL API](https://github.com/todbot/blink1/blob/main/docs/app-url-api-examples.md)
  - [blink(1) HID commands](https://github.com/todbot/blink1/blob/main/docs/blink1-hid-commands.md)

<!--

### Installation

Copy this folder to `<config_dir>/custom_components/blink1/`. Thanks to the work of Qu3uk you can now also add this repo to HACS for easy installation.


Add the following entry in your `configuration.yaml`:

```yaml
light:
  - platform: blink1_status 
```

### Remarks
- Use at your own risk. This is far from complete, but for me it works.
- Feel free to do anything with the code, for my work there is no license attached.
-->

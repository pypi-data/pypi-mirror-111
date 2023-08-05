# mondeja's pre-commit hooks

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]

## Example configuration

```yaml
- repo: https://github.com/mondeja/pre-commit-hooks
  rev: v1.3.0
  hooks:
    - id: dev-extras-required
    - id: root-editorconfig-required
    - id: cloudflare-nameservers
      args:
        - -domain=my-web.xyz
```

## Hooks

### **`add-pre-commit-hook`**

Add a pre-commit hook to your configuration file if is not already defined.

#### Parameters

- `-repo=URL` (*str*) Repository of the new hook.
- `-rev=VERSION` (*str*) Version of the new hook.
- `-hook=ID` (*str*) Identifier of the new hook.
 
### **`dev-extras-required`**

> - Doesn't support `setup.py` files. Please, [migrate your setup configuration
 to `setup.cfg` format][setup-py-upgrade-link].
> - Support for `pyproject.toml` files is limited to printing errors, automatic
 file rewriting is not performed.

Check if your development dependencies contains all other extras requirements.
If an extra requirement is defined in other extra group than your development
one, it will be added to your development extra dependencies group. If your
development group is not defined, it will be created.

This is useful if you want to execute `python -m pip install -e .[dev]` to
install all the optional requirements of the package, so if you add a new
requirement to another groups, it will be added to development requirements.

#### Parameters

- `-extra=NAME` (*str*): Name for your development requirements extra group
 (as default `dev`).
- `-setup-cfg=PATH` (*str*): Path to your `setup.cfg` file, mandatory if
 the extras requirements are defined in a `setup.cfg` file and this is located
 in another directory than the current one.
- `-pyproject-toml=PATH` (*str*): Path to your `pyproject.toml` file,
 mandatory if the extras requirements are defined in a `pyproject.toml` file
 and this is located in another directory than the current one.

### **`nameservers-endswith`**

Check that the nameservers of a domain ends with a string or raise an error.
You can use it to check if a site like Clouflare is managing a domain using
`-nameserver=cloudflare.com`.

#### Parameters

- `-domain=DOMAIN` (*str*): Domain name whose nameservers will be checked.
- `-nameserver=NAMESERVER` (*str*): String to end the domain name servers in.

### **`cloudflare-nameservers`**

Check that [Cloudflare][cloudflare-link] is handling the nameservers of a
domain.

#### Parameters

- `-domain=DOMAIN` (*str*): Domain name whose nameservers will be checked.

### **`root-editorconfig-required`**

Check if your repository has an `.editorconfig` file and if this has a `root`
directive defined as `true` before section headers.

### **`wavelint`**

Check if your WAVE files have the correct number of channels, frame rate,
durations...

#### Parameters

- `-nchannels=N` (*int*): Number of channels that your sounds must have.
- `-sample-width=N` (*int*): Number of bytes that your sounds must have.
- `-frame-rate=N` (*int*): Sampling frequency that your sounds must have.
- `-nframes=N` (*int*): Exact number of frames that your sounds must have.
- `-comptype=TYPE` (*str*): Compression type that your sounds must have.
- `-compname=NAME` (*int*): Compression that your sounds must have.
- `-min-duration=TIME` (*float*): Minimum duration in seconds that your
 sounds must have.
- `-max-duration=TIME` (*float*): Maximum duration in seconds that your
 sounds must have.

## More hooks

- [mondeja/pre-commit-po-hooks][pre-commit-po-hooks-link]

[pypi-link]: https://pypi.org/project/mondeja_pre_commit_hooks
[pypi-version-badge-link]: https://img.shields.io/pypi/v/mondeja_pre_commit_hooks
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/mondeja_pre_commit_hooks
[license-image]: https://img.shields.io/pypi/l/mondeja_pre_commit_hooks?color=light-green
[license-link]: https://github.com/mondeja/pre-commit-po-hooks/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/pre-commit-hooks/CI?logo=github&label=tests
[tests-link]: https://github.com/mondeja/pre-commit-hooks/actions?query=workflow%CI

[setup-py-upgrade-link]: https://github.com/asottile/setup-py-upgrade
[cloudflare-link]: https://cloudflare.com
[pre-commit-po-hooks-link]: https://github.com/mondeja/pre-commit-po-hooks

# apollo

apollo is a command line utility which helps you being healthy by reminding you to take breaks at fixed intervals of time.

## Installation
On Windows:
```powershell
pip install apollopy
```

On Linux/MacOS:
```bash
pip3 install apollopy
```

Or if you're using pipx:
```bash
pipx install apollopy
```

## Usage

### start
Starts the forever loop, reminds you to take eyes, water and exercise breaks after regular intervals of time.

Example:
```bash
$ apollo start
```


### config

Configures apollo reminder time.

On default:
```
eyes timeout = 15 mins
water timeout = 30 mins
exercise timeout = 45 mins
````

However, you can configure this behaviour using the `config` command.

The valid options for the `config` command are:
- `eyes-timeout`
- `water-timeout`
- `exercise-timeout`

The value of all these flags must be in seconds.

Example:
```bash
$ apollo config --eyes-timeout 1000
```


## Versioning

apollo releases follow semantic versioning, every release is in the *x.y.z* form, where:

- x is the MAJOR version and is incremented when a backwards incompatible change to apollo is made.
- y is the MINOR version and is incremented when a backwards compatible change to apollo is made, like changing dependencies or adding a new function, method, or features.
- z is the PATCH version and is incremented after making minor changes that don't affect apollo's public API or dependencies, like fixing a bug.

<br>

## Licensing

License © 2021-Present Shravan Asati

This repository is licensed under the BSD license. See [LICENSE](LICENSE) for details.
# pistachio
Pistachio aims to simplify reoccurring tasks when working with the file system.

## Developing

Hello World To install helloworld, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

## Install

You can install pistachio by running the following command.

```bash
$ pip install pistachio
```

## Usage

To use pistachio you can inport the module by running the following commands.

```python
>>> import pistachio
```

### Exists

You can confirm if a directory, file or symbolic link exists using the following method.

```python
>>> pistachio.exists('README.md')
True

# Kamo CLI
Kamo Commandline Tool

The Kamo tool is a simple user-facing CLI tool for communicating with the Kamo backend and Knode backend rest services.

## Getting started

This tool is being rapidly developed and it is recommended that you install it in development mode.

```bash
$ pip install -e .
```

Once the tool is installed you need to add a profile and create or set a tenant. e.g.
```bash
$ kamo profile add kamo
> kamo.io

$ kamo tenants list

$ kamo tenants create testtenant

$ kamo tenants set testtenant
```

Test that everything works:

```bash
$ kamo version
$ kamo jobs list --all

```

## Advanced usage

For all commands you can use the `-o json` flag to produce json output which is handy when doing automation or using the jq tool to do further processing.

For example, to get a list on all objects you might run:
```bash
$ kamo -ojson db objects list | jq
```

When debugging or inspecting the restful api it can be useful to use the `-v info` og `-v debug` flags to get further information about what the tool is doing.

Try these for example to see how the cli tool gets objects from the kamo db
```bash
$ kamo -vinfo db objects list --num 1
$ kamo -vdebug db objects list --num 1
```

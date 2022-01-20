# Synology package example

For more information, please refer [Synology package developer guide](https://help.synology.com/developer-guide/) and [Synology dev center](https://www.synology.com/en-global/support/developer#tool)

# How to pack the example package


## Get the package scripts

```
git clone https://github.com/SynologyOpenSource/pkgscripts-ng
cd pkgscripts-ng
```

## Select the target platform and DSM version

Assume you are going to develop package compatible with DSM7.0
```
git checkout DSM7.0
```

Find your platform name by listing all available platforms supported by DSM7.0
```
./EnvDeploy -l
```

## Deploy environment

Assume your platform is geminilake, and target DSM version is DSM 7.0. Deploy your development environment.
```
./EnvDeploy -v 7.0 -p geminilake
```

## Clone this repo

Clone this repo to your build machine
```
mkdir -p ../source
cd ../source
git clone <path-to-this-repo>
```

## Select the example you need

```
cp -a <path-to-this-repo>/<repo-you-need> ./
```

## Pack the package

```
cd ../pkgscripts-ng
./PkgCreate.py -v 7.0 -p geminilake -c <repo-you-need>
```

## Collect the package

```
ls ../result_spk
```




Format: 3.0 (quilt)
Source: xenadmin
Version: 0
Binary: xenadmin
Maintainer: Ilya Stolyarov <ila.embsys@gmail.com>
Architecture: any
Standards-Version: 3.7.2
Build-Depends:  debhelper,
                mono-xbuild,
                dotnet-sdk-8.0,
                git
DEBTRANSFORM-TAR: xenadmin-20240501.296e729+mono.tar.gz
DEBTRANSFORM-FILES:
    nuget_packages.tgz
    microsoft.netframework.referenceassemblies.1.0.3.nupkg
    microsoft.netframework.referenceassemblies.net48.1.0.3.nupkg

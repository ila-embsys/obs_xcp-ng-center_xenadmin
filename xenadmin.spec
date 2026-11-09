# Archive name with saved nuget packages
%define nuget_pkgs nuget_packages

Name:           xenadmin
Version:        0
Release:        0
Summary:        XCP-ng Center is a management tool for XCP-ng environments
License:        GPL-2.0
URL:            https://github.com/ila-embsys/xenadmin.git
Source0:        %{name}-%{version}.tar.gz
Source1:        %{nuget_pkgs}.tgz
BuildRequires:  msbuild
BuildRequires:  git
BuildRequires:  google-roboto-fonts

%description
XCP-ng Center is a management tool for XCP-ng environments which enables users
to manage and monitor XCP-ng hosts and resource pools, and to deploy, monitor,
manage and migrate virtual machines.

Disclaimer:
The official graphical client for XCP-ng is Xen Orchestra, which gets support
from a team of several developers. XCP-ng Center is maintained by community
members on their free time and hosted by the XCP-ng project.

/!\ EOL-Notice /!\ Community-maintained only /!\ 

%prep
%setup
mkdir -p %{nuget_pkgs}
tar -xf %{SOURCE1} -C %{nuget_pkgs}
msbuild -t:restore -p:RestorePackagesPath=%{nuget_pkgs}

%build
msbuild -p:Configuration=Release

mkdir -p %{_builddir}%{_bindir}

LIBDIR="%{_libdir}" \
APPLICATION="%{name}" \
EXECUTABLE="XCP-ng Center" \
envsubst < %{_sourcedir}/mono-app-exec.template > %{_builddir}%{_bindir}/%{name}

%install
install -Dm 755 %{_builddir}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}
cd XenAdmin/bin/Release/net48
find . -type f ! -path '*.pdb' -exec \
    install -Dm 644 "{}" "%{buildroot}%{_libdir}/%{name}/{}" \;

%files
%dir %{_libdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/%{name}/*

%changelog

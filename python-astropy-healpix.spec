%global srcname astropy-healpix
%global modname astropy_healpix
%global sum HEALPix for Astropy

Name:           python-%{srcname}
Version:        0.2
Release:        1%{?dist}
Summary:        %{sum}

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python3-astropy
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
# BuildRequires for tests, healpy only available on 64 bit architectures,
# thus these tests are skipped on 32 bit
%ifnarch %{ix86} %{arm}
BuildRequires:  python3-healpy
%endif
BuildRequires:  python3-hypothesis
BuildRequires:  python3-matplotlib
BuildRequires:  python3-pytest

%description
This is a BSD-licensed Python package for HEALPix, which is based on the C
HEALPix code written by Dustin Lang originally in astrometry.net, and was
added here with a Cython wrapper and expanded with a Python interface.


%package -n python3-%{srcname}
Summary:        %{sum}
Requires:       python3-astropy
Requires:       python3-matplotlib
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{description}


%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pushd %{buildroot}/%{python3_sitearch}
py.test-%{python3_version} %{modname}
popd
# Hypothesis tests creates some files in sitearch... we remove them now
rm -rf %{buildroot}%{python3_sitearch}/.hypothesis

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python3-%{srcname}
%license LICENSE.md
%doc CHANGES.rst README.rst
%{python3_sitearch}/%{modname}
%{python3_sitearch}/%{modname}*egg-info

%changelog
* Sat Mar 17 2018 Christian Dersch <lupinix@mailbox.org> - 0.2-1
- initial package


%global srcname astropy-healpix
%global modname astropy_healpix
%global sum HEALPix for Astropy

Name:           python-%{srcname}
Version:        0.3.1
Release:        2%{?dist}
Summary:        %{sum}

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  gcc
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
# Delete pre-cythonized files, we do that by ourself to use Fedora Cython
find . -name *.pyx -print0 | sed "s/pyx/c/g" | xargs -0 rm
# Force Cython re-run
echo "cython_version = 'unknown'" > astropy_healpix/cython_version.py

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
rm -rf %{buildroot}%{python3_sitearch}/.pytest_cache

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python3-%{srcname}
%license LICENSE.md
%doc README.rst
%{python3_sitearch}/%{modname}
%{python3_sitearch}/%{modname}*egg-info

%changelog
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Christian Dersch <lupinix.fedora@gmail.com> - 0.3.1-1
- new version

* Tue Oct 02 2018 Christian Dersch <lupinix@fedoraproject.org> - 0.2.1-1
- new version

* Sun Jul 15 2018 Christian Dersch <lupinix@fedoraproject.org> - 0.2-6
- BuildRequires: gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Christian Dersch <lupinix@mailbox.org> - 0.2-4
- Use PyPI tar and delete the Cythonized code

* Sat Jun 30 2018 Christian Dersch <lupinix@mailbox.org> - 0.2-3
- Use GitHub tar instead of PyPI one (as GitHub one is not Cythonized)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2-2
- Rebuilt for Python 3.7

* Sat Mar 17 2018 Christian Dersch <lupinix@mailbox.org> - 0.2-1
- initial package


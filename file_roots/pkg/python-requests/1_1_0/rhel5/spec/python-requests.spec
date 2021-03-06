%global __python2 /usr/bin/python2.6
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")

%global srcname requests

Name:           python-%{srcname}
Version:        1.1.0
Release:        5%{?dist}
Summary:        HTTP library, written in Python, for human beings

Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/requests
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
# Explicitly use the system certificates in openssl.
# https://bugzilla.redhat.com/show_bug.cgi?id=904614
# https://bugzilla.redhat.com/show_bug.cgi?id=1124060
Patch0:         python-requests-system-cert-bundle-el5.patch
# Unbundle python-charade (a fork of python-chardet).
# https://bugzilla.redhat.com/show_bug.cgi?id=904623
Patch1:         python-requests-system-chardet-not-charade.patch
# Unbundle python-charade (a fork of python-urllib3).
# https://bugzilla.redhat.com/show_bug.cgi?id=904623
Patch2:         python-requests-system-urllib3.patch

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python26-devel
BuildRequires:  python26-distribute
BuildRequires:  python26-chardet
BuildRequires:  python26-ordereddict
BuildRequires:  python26-urllib3

Requires:       openssl
Requires:       python26
Requires:       python26-chardet
Requires:       python26-ordereddict
Requires:       python26-urllib3

%description
Most existing Python modules for sending HTTP requests are extremely verbose
and cumbersome. Python's built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

%package -n python26-%{srcname}
Group:          Development/Languages
Summary:        HTTP library, written in Python, for human beings
Requires:       python26
Requires:       python26-chardet
Requires:       python26-ordereddict
Requires:       python26-urllib3

%description -n python26-%{srcname}
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python's built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

%prep
%setup -q -n requests-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

# Unbundle the certificate bundle from mozilla.
rm -rf requests/cacert.pem

%build
%{__python2} setup.py build

# Unbundle chardet.  Patch1 switches usage to system chardet.
rm -rf build/lib/requests/packages/charade

# Unbundle urllib3.  Patch1 switches usage to system urllib3.
rm -rf build/lib/requests/packages

%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%files -n python26-%{srcname}
%defattr(-,root,root,-)
%doc NOTICE LICENSE README.rst HISTORY.rst
%{python2_sitelib}/*.egg-info
%dir %{python2_sitelib}/requests
%{python2_sitelib}/requests/*

%changelog
* Wed Jul 30 2014 Erik Johnson <erik@saltstack.com> - 1.1.0-5
- Initial EL5 build

* Tue Jun 11 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-4
- Correct a rhel conditional on python-ordereddict

* Thu Feb 28 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-3
- Unbundled python-urllib3.  Using system python-urllib3 now.
- Conditionally include python-ordereddict for el6.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-2
- Unbundled python-charade/chardet.  Using system python-chardet now.
- Removed deprecated comments and actions against oauthlib unbundling.
  Those are no longer necessary in 1.1.0.
- Added links to bz tickets over Patch declarations.

* Tue Feb 26 2013 Ralph Bean <rbean@redhat.com> - 1.1.0-1
- Latest upstream.
- Relicense to ASL 2.0 with upstream.
- Removed cookie handling patch (fixed in upstream tarball).
- Updated cert unbundling patch to match upstream.
- Added check section, but left it commented out for koji.

* Fri Feb  8 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.14.1-4
- Let brp_python_bytecompile run again, take care of the non-python{2,3} modules
  by removing them from the python{,3}-requests package that they did not belong
  in.
- Use the certificates in the ca-certificates package instead of the bundled one
  + https://bugzilla.redhat.com/show_bug.cgi?id=904614
- Fix a problem with cookie handling
  + https://bugzilla.redhat.com/show_bug.cgi?id=906924

* Thu Jan 31 2013 Ralph Bean <rbean@redhat.com> 0.14.1-3
- Introduced backport patch to support better cookie handling.

* Mon Jan 28 2013 Ralph Bean <rbean@redhat.com> 0.14.1-2
- Merged latest rawhide into el6.

* Wed Oct 22 2012 Arun S A G <sagarun@gmail.com>  0.14.1-1
- Updated to latest upstream release

* Sun Jun 10 2012 Arun S A G <sagarun@gmail.com> 0.13.1-1
- Updated to latest upstream release 0.13.1
- Use system provided ca-certificates
- No more async requests use grrequests https://github.com/kennethreitz/grequests
- Remove gevent as it is no longer required by requests

* Sun Apr 09 2012 Arun S A G <sagarun@gmail.com> 0.11.1-2
- Fix rhbz#808912

* Sun Apr 01 2012 Arun S A G <sagarun@gmail.com> 0.11.1-1
- Updated to upstream release 0.11.1

* Thu Mar 29 2012 Arun S A G <sagarun@gmail.com> 0.10.6-3
- Support building package for EL6

* Tue Mar 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.6-2
- +python3-requests pkg

* Sat Mar 3 2012 Arun SAG <sagarun@gmail.com> - 0.10.6-1
- Updated to new upstream version

* Sat Jan 21 2012 Arun SAG <sagarun@gmail.com> - 0.9.3-1
- Updated to new upstream version 0.9.3
- Include python-gevent as a dependency for requests.async
- Clean up shebangs in requests/setup.py,test_requests.py and test_requests_ext.py

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Arun SAG <sagarun@gmail.com> - 0.8.2-1
- New upstream version
- keep alive support
- complete removal of cookiejar and urllib2

* Thu Nov 10 2011 Arun SAG <sagarun@gmail.com> - 0.7.6-1
- Updated to new upstream release 0.7.6

* Thu Oct 20 2011 Arun SAG <sagarun@gmail.com> - 0.6.6-1
- Updated to version 0.6.6

* Fri Aug 26 2011 Arun SAG <sagarun@gmail.com> - 0.6.1-1
- Updated to version 0.6.1

* Sat Aug 20 2011 Arun SAG <sagarun@gmail.com> - 0.6.0-1
- Updated to latest version 0.6.0

* Mon Aug 15 2011 Arun SAG <sagarun@gmail.com> - 0.5.1-2
- Remove OPT_FLAGS from build section since it is a noarch package
- Fix use of mixed tabs and space
- Remove extra space around the word cumbersome in description

* Sun Aug 14 2011 Arun SAG <sagarun@gmail.com> - 0.5.1-1
- Initial package

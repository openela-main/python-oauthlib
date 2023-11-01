%global modname oauthlib

Name:               python-oauthlib
Version:            3.1.1
Release:            5%{?dist}
Summary:            An implementation of the OAuth request-signing logic

License:            BSD
URL:                https://github.com/oauthlib/oauthlib

Source0:            https://github.com/oauthlib/oauthlib/archive/v%{version}/%{modname}-%{version}.tar.gz
Patch0001:          0001-Rip-out-RSA-SHA1.patch
Patch0002:          0002-Rip-out-the-rest-of-RSA.patch
Patch0003:          0003-IPV6-regex-redirect_uri.patch
Patch0004:          0004-IPV6-parsing-signature.patch

BuildArch:          noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without
assuming a specific HTTP request object or web framework. Use it to graft
OAuth client support onto your favorite HTTP library, or provider support
onto your favourite web framework. If you're a maintainer of such a
library, write a thin veneer on top of OAuthLib and get OAuth support for
very little effort.

%package -n python3-oauthlib
Summary:            An implementation of the OAuth request-signing logic
%{?python_provide:%python_provide python3-oauthlib}

Obsoletes:          python3-oauthlib+signedtoken < 3.1.0-2

BuildRequires:      python3-devel
BuildRequires:      python3-setuptools

BuildRequires:      python3-pytest
BuildRequires:      python3-cryptography >= 1.4.0

%description -n python3-oauthlib
OAuthLib is a generic utility which implements the logic of OAuth without
assuming a specific HTTP request object or web framework. Use it to graft
OAuth client support onto your favorite HTTP library, or provider support
onto your favourite web framework. If you're a maintainer of such a
library, write a thin veneer on top of OAuthLib and get OAuth support for
very little effort.

%prep
%autosetup -n %{modname}-%{version} -p1

# python-unittest2 is now provided by "python" package and python-unittest is retired
#  adapt setup.py to reflect this fact downstream
sed -i "s/'unittest2', //" setup.py

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info

%build
%py3_build

%install
%py3_install

%check
echo 'import pytest; __getattr__ = lambda _: pytest.skip("this test needs jwt")' > jwt.py
%pytest -rs --ignore tests/oauth2/rfc6749/clients/test_service_application.py \
            --ignore tests/oauth2/rfc6749/clients/test_web_application.py \
            --ignore tests/oauth2/rfc6749/clients/test_mobile_application.py \
            --ignore tests/oauth2/rfc6749/clients/test_legacy_application.py \
            --ignore tests/oauth2/rfc6749/clients/test_backend_application.py \
            --ignore tests/oauth2/rfc6749/test_parameters.py
rm jwt.py

%files -n python3-oauthlib
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}-*

%changelog
* Thu Nov 10 2022 TomasHalman <thalman@redhat.com> - 3.1.1-5
- RFC5849 oauth1 signature base_string_uri doesn't parse IPv6 addresses
  Resolves: rhbz#2133805

* Mon Oct 24 2022 TomasHalman <thalman@redhat.com> - 3.1.1-4
- Resolves: rhbz#2133805 - fix for CVE-2022-36087

* Tue Aug 9 2022 TomasHalman <thalman@redhat.com> - 3.1.1-3
- Remove RSA support
- Remove build dependency on blinker
  Resolves: rhbz#1984046 - python-oauthlib depends on jwt for RSA

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 3.1.1-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Jun 28 2021 Jakub Hrozek <jhrozek@redhat.com> - 3.1.1-1
- Resolves: rhbz#1935433 - python-oauthlib implements and/or uses the
                           deprecated SHA1 algorithm by default

* Mon May 31 2021 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-2
- Remove the python3-oauthlib+signedtoken package
- When building, skip tests that require jwt
- Resolves: rhbz#1966407 - Drop python-jwt dependency from python-oauthlib

* Tue May 25 2021 Jakub Hrozek <jhrozek@redhat.com> - 3.1.0-1
- Resolves: rhbz#1922352 - python-oauthlib requires python-mock
- Update to upstream 3.1.0
- Gets rid of obsolete python-nose dependency
- Nuke the python2/python3 conditionals, let's only support python3

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 3.0.2-10
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-7
- Add oauthlib[signedtoken] subpackage

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019  <jdennis@redhat.com> - 3.0.2-1
- Update to upstream 3.0.2
- Resolves: rhbz#1730033

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug  3 2018  <jdennis@redhat.com> - 2.1.0-1
- upgrade to latest upstream 2.1.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018  <jdennis@redhat.com> - 2.0.1-10
- Restore use of bcond for python conditionals

* Tue Jul 10 2018  <jdennis@redhat.com> - 2.0.1-9
- Unify spec file between Fedora and RHEL

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-8
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.7.19-5
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 17 2017 John Dennis <jdennis@redhat.com> - 2.0.1-3
- fix dependency on python2-jwt, should be python-jwt

* Thu Apr 13 2017 Dennis Gilmore <dennis@ausil.us> - 2.0.1-2
- add spaces around the >= for Requires

* Thu Mar 16 2017 John Dennis <jdennis@redhat.com> - 2.0.1-1
- Upgrade to upstream 2.0.1
- port from jwt to jwcrypto (conditional build)
- bring into alignment with rhel spec file

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.0.3-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Ralph Bean <rbean@redhat.com> - 1.0.3-2
- Modernize python macros.

* Sun Apr 10 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.3-1
- Update to 1.0.3
- Add python2 provides (fixes bug #1313235 and #1314349)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-5.20150520git514cad7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4.20150520git514cad7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3.20150520git514cad7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 0.7.2-2.20150520git514cad7
- new version, from a git checkout
- Replace our patch with a sed statement.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 11 2014 Ralph Bean <rbean@redhat.com> - 0.6.0-4
- Use forward-compat python-crypto2.6 package for el6.

* Tue Jan 21 2014 Ralph Bean <rbean@redhat.com> - 0.6.0-3
- Compat macros for el6.

* Fri Nov 01 2013 Ralph Bean <rbean@redhat.com> - 0.6.0-2
- Modernized python2 rpmmacros.

* Thu Oct 31 2013 Ralph Bean <rbean@redhat.com> - 0.6.0-1
- Initial package for Fedora

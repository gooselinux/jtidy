# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

Summary:        HTML syntax checker and pretty printer
Name:           jtidy
Version:        1.0
Release:        0.4.r7dev.1.7%{?dist}
Epoch:          2
License:        BSD
URL:            http://jtidy.sourceforge.net/
Source0:        http://download.sf.net/jtidy/jtidy-04aug2000r7-dev.zip
Source1:        %{name}.jtidy.script
Patch0:         %{name}.noapis.patch
Patch1:         %{name}-source14.patch
Requires:       jaxp_parser_impl
Requires:       xml-commons-apis
Requires:       jpackage-utils
BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:       xml-commons-apis
Group:          Text Processing/Markup/HTML
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a DOM
parser for real-world HTML.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
# for /bin/rm and /bin/ln
Requires(post):   coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%package scripts
Summary:        Utility scripts for %{name}
Group:          Text Processing/Markup/HTML
Requires:       jpackage-utils >= 0:1.5
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description scripts
Utility scripts for %{name}.

%prep
%setup -q -n %{name}-04aug2000r7-dev
%patch0 -p0
%patch1 -p0
# remove all binary libs and javadocs
find . -name "*.jar" -exec %__rm -f {} \;
# correct silly permissions
%__chmod -R go=u-w *

%build
export CLASSPATH=$(build-classpath xml-commons-apis)
%ant jar javadoc

%install
%__rm -rf %{buildroot}

# jar
%__mkdir_p %{buildroot}%{_javadir}
%__cp -ap build/Tidy.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
# jar versioning
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do \
%__ln_s ${jar} `echo $jar| %__sed "s|-%{version}||g"`; done)

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
%__cp -ap doc/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %__ln_s %{name}-%{version} %{name})

# shell script
%__mkdir_p %{buildroot}%{_bindir}
%__cp -ap %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# ant.d
%__mkdir_p %{buildroot}%{_sysconfdir}/ant.d
%__cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
jtidy xml-commons-apis
EOF

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%__rm -rf %{buildroot}

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE NOTES doc/devel
%{_javadir}/*
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/*

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*

%changelog
* Thu Jan 28 2010 Deepak Bhole <dbhole@redhat.com> - 2:1.0-0.4.r7dev.1.7
- Fix license

* Wed Jan 27 2010 Deepak Bhole <dbhole@redhat.com> - 2:1.0-0.4.r7dev.1.6
- Disable AOT

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2:1.0-0.4.r7dev.1.5
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.4.r7dev.1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Deepak Bhole <dbhole@redhat.com> - 2:1.0-0.3.r7dev.1.4
- Add patch to set source to 1.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.3.r7dev.1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.0-0.2.r7dev.1.3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:1.0-0.2.r7dev.1jpp.2
- Autorebuild for GCC 4.3

* Fri Mar 16 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 2:1.0-0.1.r7dev.1jpp.2
- Remove gnu-crypto build requirement.

* Thu Feb 15 2007 Andrew Overholt <overholt@redhat.com> 2:1.0-0.1.r7dev.1jpp.1
- Don't remove JAXP APIs because we don't ship that version of
  xml-commons-apis anymore.

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> 1:1.0-0.20000804r7dev.8jpp.1
- Import

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> 1:1.0-0.20000804r7dev.8jpp
- Fix duplicate requires and missing build requires for xml-commons-apis

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> 1:1.0-0.20000804r7dev.7jpp
- Add gcj_support option

* Thu Jun 01 2006 Fernando Nasser <fnasser@redhat.org> 1:1.0-0.20000804r7dev.6jpp
- First JPP 1.7 build

* Tue Feb 22 2005 David Walluck <david@jpackage.org> 1:1.0-0.20000804r7dev.5jpp
- add ant conf
- own non-versioned javadoc symlink
- Requires: xml-commons-apis
- use build-classpath
- macros

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 1:1.0-0.20000804r7dev.4jpp
- Rebuild with ant-1.6.2

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-0.20000804r7dev.3jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-0.20000804r7dev.2jpp
- Rebuild for JPackage 1.5.
- Fix Group tags.
- Include non-versioned javadoc symlink.
- Scripts subpackage.

* Fri Aug 30 2002 Ville Skyttä <ville.skytta at iki.fi> 1:1.0-0.20000804r7dev.1jpp
- Change version to 1.0, put revision to release, add Epoch.
- Don't use included DOM and SAX, require jaxp_parser_impl.
- Add non-versioned jar symlink.
- Add shell script.
- Vendor, Distribution tags.

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 20000804-0.r7dev.5jpp
- versioned dir for javadoc
- no dependencies for javadoc package
- section macro

* Mon Dec 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 20000804-0.r7dev.4jpp
- new versioning scheme
- jar name is now jtidy.jar
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r7-dev-3jpp
-  new jpp extension
-  compiled with xalan2

* Mon Nov 19 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r7-dev-2jpp
-  fixed changelog
-  fixed license

* Mon Nov 19 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r7-dev-1jpp
-  r7dev

* Mon Nov 19 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r6-1jpp
-  first release

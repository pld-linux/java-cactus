# TODO
# - use system jars, not download with maven
# - http://jakarta.apache.org/cactus/participating/howto_build.html
%define		base_name cactus
Summary:	Cactus unit test framework for server-side Java code
Summary(pl.UTF-8):	Cactus - szkielet testów jednostkowych dla kodu w Javie po stronie serwera
Name:		java-%{base_name}
Version:	1.8.1
Release:	0.1
Epoch:		0
License:	Apache
Group:		Development/Libraries
Obsoletes:	jakarta-cactus
Source0:	http://www.apache.org/dist/jakarta/cactus/sources/cactus-%{version}-src.tar.bz2
# Source0-md5:	60c020a348100610a0d565c374146c2a
URL:		http://jakarta.apache.org/cactus/
BuildRequires:	antlr
BuildRequires:	aspectj
#BuildRequires:	checkstyle
BuildRequires:	httpunit
BuildRequires:	j2sdk >= 1.3
BuildRequires:	jakarta-commons-beanutils
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-logging
#BuildRequires:	jakarta-taglibs-standard
BuildRequires:	java-commons-httpclient
BuildRequires:	java-log4j
BuildRequires:	java-servletapi5
BuildRequires:	java-xerces
BuildRequires:	jaxp_transform_impl
#BuildRequires:	jetty4
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
BuildRequires:	maven >= 2.0
#BuildRequires:	mockobjects
#BuildRequires:	nekohtml
#BuildRequires:	regexp
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
#BuildRequires:	servletapi3
BuildRequires:	tomcat-jasper
BuildRequires:	xml-commons-apis
Requires:	antlr
Requires:	aspectj
Requires:	checkstyle
Requires:	httpunit
Requires:	j2sdkee-1.2-sun
Requires:	j2sdkee-1.3-sun
Requires:	jakarta-commons-beanutils
Requires:	jakarta-commons-collections
Requires:	jakarta-commons-logging
Requires:	jakarta-taglibs-standard
Requires:	jasper4
Requires:	java-commons-httpclient
Requires:	java-log4j
Requires:	java-xerces
Requires:	jetty4
Requires:	mockobjects
Requires:	nekohtml
Requires:	regexp
Requires:	servletapi3
Requires:	servletapi4
Requires:	xml-commons-apis
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cactus is a simple test framework for unit testing server-side Java
code (Servlets, EJBs, Tag Libs, Filters, ...). The intent of Cactus is
to lower the cost of writing tests for server-side code. It uses JUnit
and extends it. Cactus implements an in-container strategy.

%description -l pl.UTF-8
Cactus to prosty szkielet testów do testowania jednostkowego kodu w
Javie działającego po stronie serwera (serwletów, EJB, Tag Lib,
filtrów...). Celem Cactusa jest obniżenie kosztu pisania testów kodu
serwerowego. Wykorzystuje i rozszerza JUnit, implementuje strategię
wewnątrzkontenerową.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja Javadoc do pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do pakietu %{name}.

%package manual
Summary:	Docs for %{name}
Summary(pl.UTF-8):	Dokumentacja do pakietu %{name}
Group:		Documentation

%description manual
Docs for %{name}.

%description manual -l pl.UTF-8
Dokumentacja do pakietu %{name}.

%prep
%setup -q -n cactus-%{version}-src
#%{__sed} -i -e '/clover\.enable/d' build.xml

%build
mvn assembly:assembly -N
# TODO: figure out how to skip tarball build
rm -rf cactus-%{version}-bin
tar jxf target/cactus-%{version}-bin.tar.bz2
mv cactus-%{version}-bin dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}/cactus

cp -a dist/lib/*.jar $RPM_BUILD_ROOT%{_javadir}/cactus

%if 0
# jars
install -d $RPM_BUILD_ROOT%{_javadir}/cactus-12
cp -p framework/dist-12/lib/cactus-%{version}.jar \
         $RPM_BUILD_ROOT%{_javadir}/cactus-12/jakarta-cactus-%{version}.jar
cp -p integration/ant/dist-12/lib/cactus-ant-%{version}.jar \
         $RPM_BUILD_ROOT%{_javadir}/cactus-12/jakarta-cactus-ant-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/cactus-12 && for jar in %{name}*-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir}/cactus-12 && for jar in %{base_name}*-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

install -dm 755 $RPM_BUILD_ROOT%{_javadir}/cactus-13
cp -p framework/dist-13/lib/cactus-%{version}.jar \
         $RPM_BUILD_ROOT%{_javadir}/cactus-13/jakarta-cactus-%{version}.jar
cp -p integration/ant/dist-13/lib/cactus-ant-%{version}.jar \
         $RPM_BUILD_ROOT%{_javadir}/cactus-13/jakarta-cactus-ant-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/cactus-13 && for jar in %{name}*-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir}/cactus-13 && for jar in %{base_name}*-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr framework/web $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr documentation/dist/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
rm -rf documentation/dist/doc/api

# manual
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp LICENSE.cactus $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr documentation/dist/doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%dir %{_javadir}/cactus
%{_javadir}/cactus/*.jar

%if 0
%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}
%endif

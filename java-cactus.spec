%define		base_name cactus
%include	/usr/lib/rpm/macros.java
Summary:	Cactus unit test framework for server-side Java code
Summary(pl.UTF-8):	Cactus - szkielet testów jednostkowych dla kodu w Javie po stronie serwera
Name:		java-%{base_name}
Version:	1.7.2
Release:	0.1
Epoch:		0
License:	Apache
Group:		Development/Libraries
Obsoletes:	jakarta-cactus
Source0:	http://www.apache.org/dist/jakarta/cactus/source/jakarta-cactus-src-%{version}.zip
# Source0-md5:	251c65b55e42b723d7b99c87a4b204d2
#Source1:	cactus-missing-testinput.tar.gz
#Patch0: cactus-checkstyle.patch
#Patch1: cactus-noeclipse-build_xml.patch
URL:		http://jakarta.apache.org/cactus/
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	ant-nodeps >= 0:1.6
BuildRequires:	ant-trax >= 0:1.6
BuildRequires:	antlr
#BuildRequires:	aspectj
#BuildRequires:	checkstyle
BuildRequires:	httpunit
BuildRequires:	j2sdk >= 1.3
BuildRequires:	jakarta-commons-beanutils
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-logging
#BuildRequires:	jakarta-taglibs-standard
#BuildRequires:	jasper4
BuildRequires:	java-commons-httpclient
BuildRequires:	java-log4j
BuildRequires:	java-servletapi5
BuildRequires:	java-xerces
BuildRequires:	jaxp_transform_impl
#BuildRequires:	jetty4
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
#BuildRequires:	mockobjects
#BuildRequires:	nekohtml
#BuildRequires:	regexp
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
#BuildRequires:	servletapi3
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
%setup -q -n jakarta-cactus-src-%{version}
#gzip -dc %{SOURCE1} | tar -xf -
%{__sed} -i -e '/clover\.enable/d' build.xml

%build
cat >> build.properties <<EOF
aspectjrt.jar=$(build-classpath aspectjrt)
aspectj-tools.jar=$(build-classpath aspectjtools)
commons.httpclient.jar=$(build-classpath commons-httpclient)
commons.logging.jar=$(build-classpath commons-logging)
httpunit.jar=$(build-classpath httpunit)
j2ee.12.jar=$(build-classpath j2ee-1.2)
j2ee.13.jar=$(build-classpath j2ee-1.3)
junit.jar=$(build-classpath junit)
mockobjects.jar=$(build-classpath mockobjects-core)
log4j.jar=$(build-classpath log4j)
xmlapis.jar=$(build-classpath xml-commons-apis)
servlet.22.jar=$(build-classpath servletapi3)
servlet.23.jar=$(build-classpath servletapi4)
nekohtml.jar=$(build-classpath nekohtml)
jstl.jar=$(build-classpath taglibs-core)
standard.jar=$(build-classpath jakarta-taglibs-standard)
xerces.jar=$(build-classpath xerces-j2)
jetty.jar=$(build-classpath jetty4)
jasper-compiler.jar=$(build-classpath jasper4-compiler)
jasper-runtime.jar=$(build-classpath jasper4-runtime)
cactus.port=9992
EOF

if grep '=$' build.properties; then
	: Some .jar could not be found
	exit 1
fi

export OPT_JAR_LIST="ant/ant-nodeps ant/ant-junit junit ant/ant-trax jaxp_transform_impl aspectjtools"
%ant -Dbuild.sysclasspath=first

%install
rm -rf $RPM_BUILD_ROOT

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

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}/LICENSE.cactus
%{_datadir}/%{name}-%{version}
%{_javadir}/*

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}

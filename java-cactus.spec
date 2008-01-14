%define base_name cactus
Summary:	Cactus unit test framework for server-side Java code
Summary(pl.UTF-8):	Cactus - szkielet testów jednostkowych dla kodu w Javie po stronie serwera
Name:		jakarta-%{base_name}
Version:	1.7.2
Release:	0.1
Epoch:		0
License:	Apache
Group:		Development/Libraries
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
BuildRequires:	aspectj
#BuildRequires:	checkstyle
BuildRequires:	httpunit
BuildRequires:	j2sdk >= 1.3
BuildRequires:	jakarta-commons-beanutils
BuildRequires:	jakarta-commons-collections
BuildRequires:	jakarta-commons-httpclient
BuildRequires:	jakarta-commons-logging
#BuildRequires:	jakarta-taglibs-standard
#BuildRequires:	jasper4
BuildRequires:	jaxp_transform_impl
#BuildRequires:	jetty4
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
BuildRequires:	logging-log4j
#BuildRequires:	mockobjects
#BuildRequires:	nekohtml
#BuildRequires:	regexp
BuildRequires:	rpmbuild(macros) >= 1.300
#BuildRequires:	servletapi3
BuildRequires:	servletapi4
BuildRequires:	xerces-j
BuildRequires:	xml-commons-apis
Requires:	antlr
Requires:	aspectj
Requires:	checkstyle
Requires:	httpunit
Requires:	j2sdkee-1.2-sun
Requires:	j2sdkee-1.3-sun
Requires:	jakarta-commons-beanutils
Requires:	jakarta-commons-collections
Requires:	jakarta-commons-httpclient
Requires:	jakarta-commons-logging
Requires:	jakarta-taglibs-standard
Requires:	jasper4
Requires:	jetty4
Requires:	log4j
Requires:	mockobjects
Requires:	nekohtml
Requires:	regexp
Requires:	servletapi3
Requires:	servletapi4
Requires:	xerces-j2
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
%setup -q -n %{name}-src-%{version}
#gzip -dc %{SOURCE1} | tar -xf -

%build
sed -e '/clover\.enable/d' build.xml > tempf
cp tempf build.xml
rm tempf
echo aspectjrt.jar = $(build-classpath aspectjrt) >> build.properties
echo aspectj-tools.jar = $(build-classpath aspectjtools) >> build.properties
echo commons.httpclient.jar = $(build-classpath commons-httpclient) >> build.properties
echo commons.logging.jar = $(build-classpath commons-logging) >> build.properties
echo httpunit.jar = $(build-classpath httpunit) >> build.properties
echo j2ee.12.jar = $(build-classpath j2ee-1.2) >> build.properties
echo j2ee.13.jar = $(build-classpath j2ee-1.3) >> build.properties
echo junit.jar = $(build-classpath junit) >> build.properties
echo mockobjects.jar = $(build-classpath mockobjects-core) >> build.properties
echo log4j.jar = $(build-classpath log4j) >> build.properties
echo xmlapis.jar = $(build-classpath xml-commons-apis) >> build.properties
echo servlet.22.jar = $(build-classpath servletapi3) >> build.properties
echo servlet.23.jar = $(build-classpath servletapi4) >> build.properties
echo nekohtml.jar = $(build-classpath nekohtml) >> build.properties
echo jstl.jar = $(build-classpath taglibs-core) >> build.properties
echo standard.jar = $(build-classpath jakarta-taglibs-standard) >> build.properties
echo xerces.jar = $(build-classpath xerces-j2) >> build.properties
echo jetty.jar = $(build-classpath jetty4) >> build.properties
echo jasper-compiler.jar = $(build-classpath jasper4-compiler) >> build.properties
echo jasper-runtime.jar = $(build-classpath jasper4-runtime) >> build.properties
echo cactus.port = 9992 >> build.properties

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

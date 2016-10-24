Name     : jdk-py4j
Version  : 0.10.2.1
Release  : 1
URL      : https://github.com/bartdag/py4j/archive/0.10.2.1/py4j-0.10.2.1.tar.gz
Source0  : https://github.com/bartdag/py4j/archive/0.10.2.1/py4j-0.10.2.1.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : BSD-2-Clause BSD-3-Clause
BuildRequires : apache-ant
BuildRequires : apache-maven
BuildRequires : javapackages-tools
BuildRequires : jdk-aether
BuildRequires : jdk-aopalliance
BuildRequires : jdk-atinject
BuildRequires : jdk-cdi-api
BuildRequires : jdk-commons-cli
BuildRequires : jdk-commons-codec
BuildRequires : jdk-commons-io
BuildRequires : jdk-commons-lang
BuildRequires : jdk-commons-lang3
BuildRequires : jdk-commons-logging
BuildRequires : jdk-guava
BuildRequires : jdk-guice
BuildRequires : jdk-hamcrest
BuildRequires : jdk-httpcomponents-client
BuildRequires : jdk-httpcomponents-core
BuildRequires : jdk-jsoup
BuildRequires : jdk-jsr-305
BuildRequires : jdk-junit4
BuildRequires : jdk-objectweb-asm
BuildRequires : jdk-plexus-cipher
BuildRequires : jdk-plexus-classworlds
BuildRequires : jdk-plexus-containers
BuildRequires : jdk-plexus-interpolation
BuildRequires : jdk-plexus-sec-dispatcher
BuildRequires : jdk-plexus-utils
BuildRequires : jdk-sisu
BuildRequires : jdk-slf4j
BuildRequires : jdk-sonatype-oss-parent
BuildRequires : jdk-wagon
BuildRequires : lxml
BuildRequires : openjdk-dev
BuildRequires : pbr
BuildRequires : pip
BuildRequires : python-dev
BuildRequires : python3
BuildRequires : python3-dev
BuildRequires : setuptools
BuildRequires : six
BuildRequires : xmvn
Patch0    : py4j-0.8.3-add-hamcrest-in-classpath.patch
Patch1    : py4j-0.10.2.1-Base64-java8.patch
Patch2    : py4j-Base64-java7.patch

%description
Py4J
====
Py4J enables Python programs running in a Python interpreter to dynamically
access Java objects in a Java Virtual Machine. Methods are called as if the
Java objects resided in the Python interpreter and Java collections can be
accessed through standard Python collection methods. Py4J also enables Java
programs to call back Python objects.

%prep
%setup -q -n py4j-0.10.2.1
find . -name \*.jar -print -delete

sed -i -r "s|(version=).*|\1|" py4j-java/ant.properties
sed -i "s|'.*'|''|" py4j-python/src/py4j/version.py
sed -i "s|1\.6|1.8|g" py4j-java/build.xml

%patch0 -p0
sed -i "s|junit-.*\.jar|$(build-classpath junit)|g" py4j-java/ant.properties
sed -i -r "s|(<javadoc.*classpath=)\"\"|\1\"$(build-classpath junit)\"|" py4j-java/build.xml

rm py4j-java/src/main/java/py4j/Base64.java
rm py4j-java/src/test/java/py4j/Base64Test.java
%patch1 -p1

mkdir py4j-java/notest
sed -i -r 's|(<src path=")(test)"/>|\1no\2"/>|' py4j-java/build.xml
sed -i "s|py4j\.tests||" py4j-python/setup.py

sed -i "/data_files/d" py4j-python/setup.py

%build
pushd py4j-java
ant jar
popd

%install
python3 /usr/share/java-utils/mvn_artifact.py py4j-java/pom.xml py4j-java/py4j.jar

xmvn-install  -R .xmvn-reactor -n py4j -d %{buildroot}

%files
%defattr(-,root,root,-)
/usr/share/java/py4j/py4j.jar
/usr/share/maven-metadata/py4j.xml
/usr/share/maven-poms/py4j/py4j.pom

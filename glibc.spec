### RPM external glibc 2.17-292.el7
## NOCOMPILER

%global official_version %(echo "%{realversion}" | cut -d'-' -f1)

%define branch cms/%{realversion}
%define tag 172733198ec31463bf19f6b96b29ee3cd4e7625d
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/glibc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

Flags="-fasynchronous-unwind-tables -DNDEBUG -g -O3"
Opts=""
%ifarch x86_64
%ifos Linux
Flags="-mtune=generic ${Flags}"
Opts="--build=x86_64-redhat-linux --host=x86_64-redhat-linux"
%endif
%endif

rm -rf ../%{n}-build
mkdir ../%{n}-build
cd ../%{n}-build
../%{n}-%{realversion}/configure \
  CC=gcc \
  CXX=g++ \
  CFLAGS="${Flags}" \
  --prefix=/usr \
  --enable-add-ons=nptl,c_stubs,libidn \
  --without-cvs \
  --enable-kernel=2.6.18 \
  --with-headers=/usr/include \
  --enable-bind-now \
  --with-tls \
  --with-__thread \
  $Opts \
  --enable-multi-arch \
  --disable-profile \
  --enable-experimental-malloc

make %{makeprocesses}

%install
cd ../%{n}-build
make install install_root=%{i}

# Remove everything except dynamic loader. All changes are contained
# within the loader.
find %{i} ! -type d | grep -Z -v 'ld-%{official_version}' | xargs rm -f
find %{i} -empty -type d -delete

mv %{i}/lib64/ld-%{official_version}.so %{i}/lib64/ld.so

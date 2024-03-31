%define		crypto_gitref	02fe68051a7aafe7a26c2d94916cd17975eede5f
%define		mbedtls_gitref	f71e2878084126737cc39083e1e15afc459bd93d
Summary:	Core implementation of an open-source secure key
Summary(pl.UTF-8):	Podstawowa implementacja bezpiecznego klucza o otwartych źródłach
Name:		canokey-core
Version:	2.0.1
Release:	0.1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/canokeys/canokey-core/tags
Source0:	https://github.com/canokeys/canokey-core/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3796481418c30996b6abf8df2e594f53
Source1:	https://github.com/canokeys/canokey-crypto/archive/%{crypto_gitref}/canokey-crypto-%{crypto_gitref}.tar.gz
# Source1-md5:	50fedd10a71a8618c8434ee50de2b40d
# private mbedtls is patched for MBEDTLS_ECP_DP_ED25519 support
Source2:	https://github.com/ARMmbed/mbedtls/archive/%{mbedtls_gitref}/mbedtls-%{mbedtls_gitref}.tar.gz
# Source2-md5:	80fe94ab2e3eb4213d00ba0473dbe71c
Patch0:		%{name}-system-libs.patch
URL:		https://github.com/canokeys/canokey-core/
BuildRequires:	cmake >= 3.7
BuildRequires:	gcc >= 6:4.7
BuildRequires:	littlefs-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tinycbor-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Core implementations of an open-source secure key, with supports of:
* U2F / FIDO2 with ed25519 and HMAC-secret
* OpenPGP Card V3.4
* PIV (NIST SP 800-73-4)
* HOTP / TOTP
* NDEF

%description -l pl.UTF-8
Podstawowa implementacja bezpiecznego klucza o otwartych źródłach, z
obsługą:
* U2F / FIDO2 z ed25519 i HMAC-secret
* OpenPGP Card V3.4
* PIV (NIST SP 800-73-4)
* HOTP / TOTP
* NDEF

%package devel
Summary:	Header files for canokey-core library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki canokey-core
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for canokey-core library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki canokey-core.

%prep
%setup -q
%patch0 -p1

%{__tar} xf %{SOURCE1} -C canokey-crypto --strip-components=1
%{__tar} xf %{SOURCE2} -C canokey-crypto/mbedtls --strip-components=1

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/canokey-{core,crypto}}

install build/libcanokey-core.so build/canokey-crypto/libcanokey-crypto.so $RPM_BUILD_ROOT%{_libdir}

cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}/canokey-core
cp -p canokey-crypto/include/*.h $RPM_BUILD_ROOT%{_includedir}/canokey-crypto

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libcanokey-core.so
%attr(755,root,root) %{_libdir}/libcanokey-crypto.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/canokey-core
%{_includedir}/canokey-crypto

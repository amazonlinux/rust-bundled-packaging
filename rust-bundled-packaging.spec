Name:           rust-bundled-packaging
Version:        1
Release:        1%{?dist}
Summary:        RPM macros for packaging Rust binaries

License:        MIT
URL:            https://github.com/awslabs/rust-bundled-packaging
Source0:        macros.rust
Source1:        macros.cargo
Source2:        cargo.attr
Source10:       LICENSE
Source11:       README.md

BuildArch:      noarch
Requires:       rpm-build findutils jq rust cargo

%description
RPM macros for packaging Rust bin crates that bundle dependent crates into the
source RPM.


%prep
mkdir -p %{name}-%{version}
cp %{SOURCE10} %{SOURCE11} .


%build


%install
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -pm 0644 %{SOURCE0} %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d
mkdir -p %{buildroot}%{_fileattrsdir}
install -pm 0644 %{SOURCE2} %{buildroot}%{_fileattrsdir}


%files
%doc README.md
%license LICENSE
%{_rpmconfigdir}/macros.d/macros.rust
%{_rpmconfigdir}/macros.d/macros.cargo
%{_fileattrsdir}/cargo.attr


%changelog
* Thu Nov 15 2018 iliana weller <iweller@amazon.com> - 1-1
- Initial release

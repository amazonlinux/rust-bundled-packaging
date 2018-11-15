# rust-bundled-packaging

RPM packaging utilities building [Rust](https://www.rust-lang.org/) bin crates.

This is a fork of the [Fedora Rust SIG](https://fedoraproject.org/wiki/SIGs/Rust)'s [rust2rpm].

This code is made available under the MIT license.

## Usage

Ensure your main source has a Cargo.lock, or generate one by unpacking it and running `cargo generate-lockfile` and add it as an additional source.

### `%cargo_bundle_crates`

Use the `%cargo_bundle_crates` macro to add source lines for crates from [crates.io][https://crates.io]. Usage:

* `-l N`: SourceN is the Cargo.lock.
* `-t N`: SourceN is a tarball that contains the Cargo.lock.
* `-n DIRNAME` (only with `-t`): The Cargo.lock is under the directory DIRNAME in the tarball. This defaults to `%{name}-%{version}`.

Example:

```
Source0:        https://github.com/BurntSushi/ripgrep/archive/%{version}/%{name}-%{version}.tar.gz
%cargo_bundle_crates -t 0
```

### `%cargo_prep`, `%cargo_build`, `%cargo_install`, `%cargo_test`

Use these macros in your `%prep`, `%build`, `%install`, and `%test` sections, respectively.

`%cargo_prep` is to be run after `%setup` and unpacks sources under `$PWD/.registry`. If you have patches to dependency crates, you will need to apply them after `%cargo_prep`.

Do not add additional arguments to these macros, as it will not do what you expect. Provide additional arguments to `cargo` by defining `%cargo_args`:

```
%global cargo_args --features blah

%build
%cargo_build
```

### `%{_cargometadir}/%{name}.json`

In order to generate automatic `bundled(crate(name)) = version` provides, `%cargo_install` writes the output of `cargo metadata --format-version 1` to `%{_cargometadir/%{name}.json`. You will need to list this in your `%files` section; we recommend marking it as `%doc` so users can opt out of installation with RPM's `--nodocs` flag.

```
%files
%license LICENSE
%doc README.md
%doc %{_cargometadir}/%{name}.json
```

## Rationale

Fedora's packaging doctrine requires that source code of packages in statically-compiled languages such as Go or Rust must be distributed as separate `devel` packages that serve only to be used in `BuildRequires` for packages that build binaries, such as Docker or ripgrep.

In practice, this depends on functionality added in RPM 4.14 (support for `with`, `without`, and `unless` rich dependency operators), as different binaries will depend on different versions of these libraries that might be maintained in parallel. Amazon Linux 2 will remain on RPM 4.11 and so we are unable to utilize this.

We also do not believe the presence of these `devel` packages is useful to Amazon Linux customers, and find the approach of using a separate source RPM for each upstream dependency to be more cumbersome than other options for carrying patches for dependencies across multiple packages.

## Disadvantages to this approach

Patches to library crates have to be maintained in all bin crates. (The bin crates all have to be rebuilt in that case regardless, however.) This will most commonly be seen with `sys` crates (library crates for C library functions) that have incorrect logic for finding system libraries.

[rust2rpm]: https://pagure.io/fedora-rust/rust2rpm

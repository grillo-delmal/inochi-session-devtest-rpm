%define inochi_session_ver 0.8.4
%define inochi_session_dist 0
%define inochi_session_short cc0e3a4

%define inochi_session_suffix ^%{inochi_session_dist}.git%{inochi_session_short}

Name:           inochi-session-nightly
Version:        %{inochi_session_ver}%{?inochi_session_suffix:}
Release:        %autorelease
Summary:        Tool to use Inochi2D puppets

# Bundled lib licenses
##   bindbc-loader licenses: BSL-1.0
##   bindbc-lua licenses: BSL-1.0
##   bindbc-sdl licenses: BSL-1.0
##   ddbus licenses: MIT
##   diet-ng licenses: MIT
##   dportals licenses: BSD-2-Clause
##   dunit licenses: MIT
##   eventcore licenses: MIT
##   facetrack-d licenses: BSD-2-Clause
##   fghj licenses: BSL-1.0
##   i18n-d licenses: BSD-2-Clause
##   i2d-imgui licenses: BSL-1.0 and MIT
##   i2d-opengl licenses: BSL-1.0
##   imagefmt licenses: BSD-2-Clause
##   inmath licenses: BSD-2-Clause
##   inochi2d licenses: BSD-2-Clause
##   inui licenses: BSD-2-Clause
##   lumars licenses: MIT
##   mir-algorithm licenses: Apache-2.0
##   mir-core licenses: Apache-2.0
##   mir-linux-kernel licenses: BSL-1.0
##   openssl licenses: OpenSSL
##   silly licenses: ISC
##   stdx-allocator licenses: BSD-2-Clause
##   taggedalgebraic licenses: BSD-2-Clause
##   tinyfiledialogs licenses: Zlib
##   vibe-container licenses: MIT
##   vibe-core licenses: MIT
##   vibe-d licenses: MIT
##   vmc-d licenses: BSD-2-Clause
License:        BSD-2-Clause and Apache-2.0 and BSL-1.0 and ISC and MIT and OpenSSL and Zlib

URL:            https://github.com/grillo-delmal/inochi-session-nightly

Source0:        https://github.com/grillo-delmal/inochi-session-nightly/releases/download/nightly/inochi-session-source.zip
Source1:        inochi-session-nightly.desktop
Source2:        inochi-session-nightly.appdata.xml
Source3:        dub.selections.json
Source4:        icon.png

# dlang
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

#bindbc-lua reqs
BuildRequires:       luajit-devel

#dportals reqs
BuildRequires:       dbus-devel

#i2d-imgui reqs
BuildRequires:       cmake
BuildRequires:       gcc
BuildRequires:       gcc-c++
BuildRequires:       freetype-devel
BuildRequires:       SDL2-devel

#openssl reqs
BuildRequires:       openssl-devel

Requires:       hicolor-icon-theme

#bindbc-lua deps
Requires:       luajit

#dportals deps
Requires:       dbus

#i2d-imgui deps
Requires:       libstdc++
Requires:       freetype
Requires:       SDL2

#openssl deps
Requires:       openssl


%description
Inochi2D is a framework for realtime 2D puppet animation which can be used for VTubing, 
game development and digital animation. 
Inochi Session is a tool that lets you use Inochi2D puppets as tracked avatars.
This is an unbranded build, unsupported by the official project.
This is a nightly build of Inochi Session!
Inochi Session may crash unexpectedly and you will likely encounter bugs.
Make sure to save and back up your work often!


%prep
%setup -c

jq "map(.path = ([\"$(pwd)\"] + (.path | split(\"/\"))[-4:] | join(\"/\")) )" <<<$(<.dub/packages/local-packages.json) > .dub/packages/local-packages.linux.json
rm .dub/packages/local-packages.json
mv .dub/packages/local-packages.linux.json .dub/packages/local-packages.json
dub add-local .flatpak-dub/semver/*/semver
dub add-local .flatpak-dub/gitver/*/gitver


%build
export DFLAGS="%{_d_optflags} -L-rpath=%{_libdir}/inochi-session-nightly/"

# Build metadata
dub build --skip-registry=all --compiler=ldc2 --config=meta

# Build the project, with its main file included, without unittests
dub build --skip-registry=all --compiler=ldc2 --config=barebones --build=debug


%install
install -d ${RPM_BUILD_ROOT}%{_libdir}/inochi-session-nightly
install -p ./out/cimgui.so ${RPM_BUILD_ROOT}%{_libdir}/inochi-session-nightly/cimgui.so

install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/inochi-session ${RPM_BUILD_ROOT}%{_bindir}/inochi-session-nightly

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_datadir}/applications/inochi-session-nightly.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/inochi-session-nightly.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 %SOURCE2 ${RPM_BUILD_ROOT}%{_metainfodir}/inochi-session-nightly.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/inochi-session-nightly.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/inochi-session-nightly.png

install -d ${RPM_BUILD_ROOT}%{_datadir}/inochi-session-nightly/
install -p -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_datadir}/inochi-session-nightly/dub.selections.json


%files
%license LICENSE
%{_bindir}/inochi-session-nightly
%{_libdir}/inochi-session-nightly/*
%{_metainfodir}/inochi-session-nightly.appdata.xml
%{_datadir}/applications/inochi-session-nightly.desktop
%{_datadir}/icons/hicolor/256x256/apps/inochi-session-nightly.png
%{_datadir}/inochi-session-nightly/dub.selections.json

%changelog
%autochangelog

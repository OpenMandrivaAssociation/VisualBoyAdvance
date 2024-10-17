%define name	VisualBoyAdvance
%define version 1.8.0
%define rel 1
%define release %mkrel %{rel}

%define build_gtk 1

Name:		%{name}
Summary:	A GBA/GB/GBC emulator
Version:	%{version}
Release:	%{release}
Group:		Emulators
Source:		visualboyadvance-%{version}.tar.gz
Patch:		06_old_2xSaImmx_asm.dpatch
Patch1:		02_amd64_build_fix.dpatch
Patch2:		visualboyadvance-1.7.2-deprecatedsigc++.patch
Url:		https://vba.ngemu.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot 
License:	GPLv2+
BuildRequires:	nasm
%if %build_gtk
BuildRequires:	gtkmm2.4-devel
BuildRequires:	libglademm2.4-devel
%endif
BuildRequires:	libSDL-devel >= 1.2.2
BuildRequires:  libpng-devel
BuildRequires:	zlib-devel
BuildRequires:  flex

%description
VisualBoyAdvance is a GPL emulator for the Game Boy, the Game Boy color
and the Game Boy Advance.

You might also want to try VisualBoyAdvance fork - VBA-M (vbam).

NO ROMS IN THIS PACKAGE !

%prep
%setup -q
%patch -p1
%patch1 -p1
%patch2

%build
%define Werror_cflags %nil
export LDFLAGS=-lz
# SDL version
%configure2_5x --without-profiling --disable-dev
%make
%if %{build_gtk}
# GTK GUI version
%configure2_5x --without-profiling --disable-dev \
  --disable-sdl \
%if %mdkversion > 1000
 --enable-gtk=2.4
%else
 --enable-gtk
%endif
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -m 755 ./src/sdl/%{name} %{buildroot}%{_bindir}
%if %{build_gtk}
%find_lang vba-%{version}
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=Gameboy Advance Emulator
Exec=gvba
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Emulator;GTK;
EOF

install -m 644 -D src/gtk/images/vba-64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -m 644 -D src/gtk/images/stock-vba-wm-48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -m 644 -D src/gtk/images/stock-vba-wm-32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m 644 -D src/gtk/images/stock-vba-wm-16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%endif

%clean
rm -rf %{buildroot}

%if %{build_gtk}
%if %mdvver < 200900
%post
%update_icon_cache hicolor
%postun
%clean_icon_cache hicolor
%endif

%files -f vba-%{version}.lang
%else
%files
%endif
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README INSTALL
%config(noreplace) %{_sysconfdir}/VisualBoyAdvance.cfg
%{_bindir}/%{name}
%if %{build_gtk}
%{_bindir}/gvba
%{_datadir}/applications/mandriva*
%{_datadir}/VisualBoyAdvance/vba-64.png
%{_datadir}/VisualBoyAdvance/vba.glade
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%endif


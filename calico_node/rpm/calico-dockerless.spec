%global __os_install_post %{nil}

Name:          calico-dockerless
Version:       0.10.0
Release:	   1%{?dist}
Summary:	   Calico without Docker.
License:	   APv2
URL:		   http://www.projectcalico.org/

Source0:       %{name}-confd-templates.tar.gz
Source1:       %{name}-confd.service
Source2:       %{name}.service
Source3:       calicoctl
Source4:       confd
Source5:       calico-environment
Source6:       %{name}-bird.service
Source7:       bird


Requires:      calico-felix

%description
Calico for Baremetal


%prep
%setup -n confd-files

###########################################
%install

# Service Files
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/

# Binaries
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE7} %{buildroot}%{_bindir}/


# confd configurations
mkdir -p %{buildroot}%{_sysconfdir}/calico/confd/config/
mv conf.d %{buildroot}%{_sysconfdir}/calico/confd/
mv templates %{buildroot}%{_sysconfdir}/calico/confd/
install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/calico/

############################################
%files

%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-confd.service
%{_unitdir}/%{name}-bird.service
%{_bindir}/calicoctl
%{_bindir}/confd
%{_bindir}/bird
%{_sysconfdir}/calico/calico-environment
%{_sysconfdir}/calico/confd/conf.d/bird.toml.toml
%{_sysconfdir}/calico/confd/conf.d/bird6.toml.toml
%{_sysconfdir}/calico/confd/conf.d/bird6_ipam.toml
%{_sysconfdir}/calico/confd/conf.d/bird_ipam.toml
%{_sysconfdir}/calico/confd/templates/bird.cfg.mesh.template
%{_sysconfdir}/calico/confd/templates/bird.cfg.no-mesh.template
%{_sysconfdir}/calico/confd/templates/bird.toml.template
%{_sysconfdir}/calico/confd/templates/bird6.cfg.mesh.template
%{_sysconfdir}/calico/confd/templates/bird6.cfg.no-mesh.template
%{_sysconfdir}/calico/confd/templates/bird6.toml.template
%{_sysconfdir}/calico/confd/templates/bird6_aggr.toml.template
%{_sysconfdir}/calico/confd/templates/bird6_ipam.cfg.template
%{_sysconfdir}/calico/confd/templates/bird_aggr.cfg.template
%{_sysconfdir}/calico/confd/templates/bird_aggr.toml.template
%{_sysconfdir}/calico/confd/templates/bird_ipam.cfg.template

%dir %{_sysconfdir}/calico/confd/config

#############################################
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog

%clean
rm -rf %{buildroot}%{_sysconfdir}/calico
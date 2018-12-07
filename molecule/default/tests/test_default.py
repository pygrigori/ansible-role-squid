import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def get_squid_name(host):
    if host.system_info.codename == 'trusty':
        return 'squid3'
    else:
        return 'squid'


def test_pkg_installed(host):
    package_name = get_squid_name(host)
    package = host.package(package_name)

    assert package.is_installed


def test_service_is_enabled(host):
    service_name = get_squid_name(host)
    service = host.service(service_name)

    assert service.is_enabled


def test_config_exists(host):
    squid_name = get_squid_name(host)
    file = host.file('/etc/%s/squid.conf' % squid_name)

    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'


def test_config_is_valid(host):
    squid_name = get_squid_name(host)
    cmd = host.run('%s -k parse' % squid_name)

    assert not cmd.rc

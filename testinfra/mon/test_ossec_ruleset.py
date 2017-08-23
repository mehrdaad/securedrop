import re


alert_level_regex = re.compile(r"Level: '(\d+)'")


def test_grsec_denied_rwx_mapping_produces_alert(Command, Sudo):
    """Check that a denied RWX mmaping produces an OSSEC alert"""
    test_alert = ("Feb 10 23:34:40 app kernel: [  124.188641] grsec: denied "
                  "RWX mmap of <anonymous mapping> by /usr/sbin/apache2"
                  "[apache2:1328] uid/euid:33/33 gid/egid:33/33, parent "
                  "/usr/sbin/apache2[apache2:1309] uid/euid:0/0 gid/egid:0/0")

    with Sudo():
        c = Command('echo "{}" | /var/ossec/bin/ossec-logtest'.format(
                test_alert))

        # Level 7 alert should be triggered by rule 100101
        assert "Alert to be generated" in c.stderr
        alert_level = alert_level_regex.findall(c.stderr)[0]
        assert alert_level == "7"


def test_overloaded_tor_guard_does_not_produce_alert(Command, Sudo):
    """Check that using an overloaded guard does not produce an OSSEC alert"""
    test_alert = ("Aug 16 21:54:44 app-staging Tor[26695]: [warn] Your Guard "
                  "<name> (<fingerprint>) is failing a very large amount of "
                  "circuits. Most likely this means the Tor network is "
                  "overloaded, but it could also mean an attack against you "
                  "or potentially the guard itself.")

    with Sudo():
        c = Command('echo "{}" | /var/ossec/bin/ossec-logtest'.format(
                test_alert))

        assert "Alert to be generated" not in c.stderr
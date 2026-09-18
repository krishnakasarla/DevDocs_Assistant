> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# IP Binding in Self-Managed Deployments

## Overview

MongoDB binaries, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos), bind to localhost by default. If the [`net.ipv6`](/docs/manual/reference/configuration-options#mongodb-setting-net.ipv6) configuration file setting or the `--ipv6` command line option is set for the binary, the binary additionally binds to the localhost IPv6 address.

## Considerations

**Warning:**

Make sure that your [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances are only accessible on trusted networks. If your system has more than one network interface, bind MongoDB programs to the private or internal network interface.

If the [`net.ipv6`](/docs/manual/reference/configuration-options#mongodb-setting-net.ipv6) configuration file setting or the `--ipv6` command line option is set for the binary, the binary additionally binds to the localhost IPv6 address.

To bind to all IPv4 addresses, you can specify the bind ip address of `0.0.0.0`. To bind to all IPv4 and IPv6 addresses, you can specify the bind ip address of `::,0.0.0.0` or alternatively, use the new [`net.bindIpAll`](/docs/manual/reference/configuration-options#mongodb-setting-net.bindIpAll) setting or the new command-line option `--bind_ip_all`.

**See also:**

- [Firewalls](/docs/manual/core/security-hardening#std-label-security-firewalls)

- [Security Considerations](/docs/manual/administration/configuration#std-label-configuration-security)

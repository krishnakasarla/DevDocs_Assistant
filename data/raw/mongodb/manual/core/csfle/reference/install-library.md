> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Install and Configure a CSFLE Query Analysis Component

MongoDB uses the Automatic Encryption Shared Library (recommended) or the `mongocryptd` executable process to translate queries into encrypted queries, and to encrypt or decrypt data.

## Before You Begin

To use CSFLE with automatic encryption, you must first choose the query analysis component you want MongoDB to use to encrypt the fields.

- [crypt\_shared](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-shared-lib), the recommended CSFLE library.

- [mongocryptd](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-mongocryptd), which is included in MongoDB Enterprise Server installations.

The `libmongocrypt` library and MongoDB drivers require the Automatic Encryption Shared Library or `mongocryptd` to interpret encrypted queries. For more information, see [Install libmongocrypt for CSFLE.](/docs/manual/core/csfle/reference/libmongocrypt#std-label-csfle-reference-libmongocrypt)

### Automatic Encryption Shared Library

The Automatic Encryption Shared Library is a **dynamic library** that enables your client application to perform automatic encryption. A dynamic library is a set of functionality accessed by an application at runtime rather than compile time. The Automatic Encryption Shared Library performs the following tasks:

- Reads the encryption schema to determine which fields to encrypt or decrypt

- Prevents your application from executing unsupported operations on encrypted fields

The Automatic Encryption Shared Library *does not* do any of the following:

- Perform data encryption or decryption

- Access the encryption key material

- Listen for data over the network

The Automatic Encryption Shared Library is a preferred alternative to `mongocryptd` and does not require you to spawn another process to perform automatic encryption.

**Note:**

While we recommend using the Automatic Encryption Shared Library, `mongocryptd` is still supported.

To learn more about automatic encryption, see [CSFLE Features.](/docs/manual/core/csfle/features#std-label-csfle-features)

### mongocryptd

`mongocryptd` is installed with [MongoDB Enterprise Server.](https://www.mongodb.com/try/download/enterprise)

When you create a CSFLE-enabled MongoDB client, the `mongocryptd` process starts automatically by default.

The `mongocryptd` process:

- Uses the specified automatic encryption rules to mark fields in read and write operations for encryption.

- Prevents unsupported operations from executing on encrypted fields.

- Parses the encryption schema specified for the database connection. Automatic encryption rules use a strict subset of JSON schema syntax. If the rules contain invalid automatic encryption syntax or any [`schema validation`](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema) syntax, `mongocryptd` returns an error.

`mongocryptd` only performs the previous functions, and doesn't perform any of the following:

- `mongocryptd` doesn't perform encryption or decryption

- `mongocryptd` doesn't access any encryption key material

- `mongocryptd` doesn't listen over the network

To perform field encryption and automatic decryption, the drivers use the Apache-licensed [libmongocrypt](https://github.com/mongodb/libmongocrypt) library.

The official MongoDB drivers require access to the `mongocryptd` process on the client host machine. These clients search for the `mongocryptd` process in the system `PATH` by default.

## Steps

Select the query analysis component you want to use and follow the steps to install and configure a CSFLE query analysis component.

1. Download the Automatic Encryption Shared Library

   Download the Automatic Encryption Shared Library from the [MongoDB Download Center](https://www.mongodb.com/try/download/enterprise) by selecting the version and platform, then the library:

   1. In the Version dropdown, select the version labeled as "current."

   2. In the Platform dropdown, select your platform.

   3. In the Package dropdown, select `crypt_shared`.

   4. Click Download.

   **Tip:**

   To view an expanded list of available releases and packages, see [MongoDB Enterprise Downloads.](https://www.mongodb.com/download-center/enterprise/releases)

2. Configure Automatic Encryption Shared Library

   You can configure how your driver searches for the Automatic Encryption Shared Library through the following parameters:

   | Name | Description |
   | --- | --- |
   | `cryptSharedLibPath` | Specifies the absolute path to the Automatic Encryption Shared Library package, `crypt_shared`. **Default**: `undefined` |
   | `cryptSharedLibRequired` | Specifies if the driver must use the Automatic Encryption Shared Library. If `true`, the driver raises an error if the Automatic Encryption Shared Library is unavailable. If `false`, the driver performs the following sequence of actions: Attempts to use the Automatic Encryption Shared Library.; If the Automatic Encryption Shared Library is unavailable, the driver attempts to spawn and connect to `mongocryptd`. **Default**: `false` |

   To view an example demonstrating how to configure these parameters, see the [Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)

1) Install mongocryptd

   **For supported Linux Operating Systems:** To install the Server package, follow the [install on Linux tutorial](/docs/manual/administration/install-enterprise-linux#std-label-install-enterprise-linux) and install the `mongodb-enterprise` server package. Alternatively, specify `mongodb-enterprise-cryptd` instead to install only the `mongocryptd` binary. The package manager installs the binaries to a location in the system PATH.

   **For OSX:** To install the Server package, follow the [install on MacOS tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-os-x#std-label-install-enterprise-macos). The package manager installs binaries to a location in the system PATH.

   **For Windows:** To install the Server package, follow the [install on Windows tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-windows#std-label-install-enterprise-windows). You must add the `mongocryptd` package to your system PATH after installation. Follow the documented best practices for your Windows installation to add the `mongocryptd` binary to the system PATH.

   **To install from an official tarball / ZIP archive:** To install from an official archive, follow the documented best practices for your operating system to add the `mongocryptd` binary to your system PATH.

2) Configure mongocryptd

   If the driver has access to the `mongocryptd` process, it spawns the process by default. Your application must have write permissions on the working directory to create the `mongocryptd.pid` file.

   **Important: Start on Boot**

   If possible, start `mongocryptd` on boot, rather than launching it on demand.

   Configure how the driver starts `mongocryptd` through the following parameters:

   | Name | Description |
   | --- | --- |
   | port | The port from which `mongocryptd` listens for messages.*Default*: `27020` |
   | idleShutdownTimeoutSecs | Number of idle seconds the `mongocryptd` process waits before exiting.*Default*: `60` |
   | mongocryptdURI | The URI on which to run the `mongocryptd` process.*Default*: `"mongodb://localhost:27020"` |
   | mongocryptdBypassSpawn | When `true`, prevents the driver from automatically spawning `mongocryptd`.*Default*: `false` |
   | mongocryptdSpawnPath | The full path to `mongocryptd`.*Default*: Defaults to empty string and spawns from the system path. |

   If a `mongocryptd` process is already running on the port specified by the driver, the driver may log a warning and continue without spawning a new process. Any settings specified by the driver only apply once the existing process exits and a new encrypted client attempts to connect.

### Example

The following code-snippet sets the listening port configuration of `mongocryptd`:

```javascript
autoEncryption: {
  ...
  extraOptions: {
    mongocryptdSpawnArgs: ["--port", "30000"],
    mongocryptdURI: 'mongodb://localhost:30000',
  }
```

**Note:**

In the NodeJS driver, the `mongocryptdURI` must match the listening port.

The following code-snippet sets the default timeout configuration of `mongocryptd`:

```javascript
autoEncryption: {
  ...
  extraOptions: {
    mongocryptdSpawnArgs: ["--idleShutdownTimeoutSecs", "75"]
  }
```

1. Install mongocryptd

   **For supported Linux Operating Systems:** To install the Server package, follow the [install on Linux tutorial](/docs/manual/administration/install-enterprise-linux#std-label-install-enterprise-linux) and install the `mongodb-enterprise` server package. Alternatively, specify `mongodb-enterprise-cryptd` instead to install only the `mongocryptd` binary. The package manager installs the binaries to a location in the system PATH.

   **For OSX:** To install the Server package, follow the [install on MacOS tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-os-x#std-label-install-enterprise-macos). The package manager installs binaries to a location in the system PATH.

   **For Windows:** To install the Server package, follow the [install on Windows tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-windows#std-label-install-enterprise-windows). You must add the `mongocryptd` package to your system PATH after installation. Follow the documented best practices for your Windows installation to add the `mongocryptd` binary to the system PATH.

   **To install from an official tarball / ZIP archive:** To install from an official archive, follow the documented best practices for your operating system to add the `mongocryptd` binary to your system PATH.

2. Configure mongocryptd

   If the driver has access to the `mongocryptd` process, it spawns the process by default. Your application must have write permissions on the working directory to create the `mongocryptd.pid` file.

   **Important: Start on Boot**

   If possible, start `mongocryptd` on boot, rather than launching it on demand.

   Configure how the driver starts `mongocryptd` through the following parameters:

   | Name | Description |
   | --- | --- |
   | port | The port from which `mongocryptd` listens for messages.*Default*: `27020` |
   | idleShutdownTimeoutSecs | Number of idle seconds the `mongocryptd` process waits before exiting.*Default*: `60` |
   | mongocryptdURI | The URI on which to run the `mongocryptd` process.*Default*: `"mongodb://localhost:27020"` |
   | mongocryptdBypassSpawn | When `true`, prevents the driver from automatically spawning `mongocryptd`.*Default*: `false` |
   | mongocryptdSpawnPath | The full path to `mongocryptd`.*Default*: Defaults to empty string and spawns from the system path. |

   If a `mongocryptd` process is already running on the port specified by the driver, the driver may log a warning and continue without spawning a new process. Any settings specified by the driver only apply once the existing process exits and a new encrypted client attempts to connect.

### Example

The following code-snippet sets the listening port configuration of `mongocryptd`:

```java
List<String> spawnArgs = new ArrayList<String>();
spawnArgs.add("--port=30000");

Map<String, Object> extraOpts = new HashMap<String, Object>();
extraOpts.put("mongocryptdSpawnArgs", spawnArgs);

AutoEncryptionSettings autoEncryptionSettings = AutoEncryptionSettings.builder()
    ...
    .extraOptions(extraOpts);
```

The following code-snippet sets the default timeout configuration of `mongocryptd`:

```java
List<String> spawnArgs = new ArrayList<String>();
spawnArgs.add("--idleShutdownTimeoutSecs")
    .add("60");

Map<String, Object> extraOpts = new HashMap<String, Object>();
extraOpts.put("mongocryptdSpawnArgs", spawnArgs);

AutoEncryptionSettings autoEncryptionSettings = AutoEncryptionSettings.builder()
    ...
    .extraOptions(extraOpts);
```

1. Install mongocryptd

   **For supported Linux Operating Systems:** To install the Server package, follow the [install on Linux tutorial](/docs/manual/administration/install-enterprise-linux#std-label-install-enterprise-linux) and install the `mongodb-enterprise` server package. Alternatively, specify `mongodb-enterprise-cryptd` instead to install only the `mongocryptd` binary. The package manager installs the binaries to a location in the system PATH.

   **For OSX:** To install the Server package, follow the [install on MacOS tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-os-x#std-label-install-enterprise-macos). The package manager installs binaries to a location in the system PATH.

   **For Windows:** To install the Server package, follow the [install on Windows tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-windows#std-label-install-enterprise-windows). You must add the `mongocryptd` package to your system PATH after installation. Follow the documented best practices for your Windows installation to add the `mongocryptd` binary to the system PATH.

   **To install from an official tarball / ZIP archive:** To install from an official archive, follow the documented best practices for your operating system to add the `mongocryptd` binary to your system PATH.

2. Configure mongocryptd

   If the driver has access to the `mongocryptd` process, it spawns the process by default. Your application must have write permissions on the working directory to create the `mongocryptd.pid` file.

   **Important: Start on Boot**

   If possible, start `mongocryptd` on boot, rather than launching it on demand.

   Configure how the driver starts `mongocryptd` through the following parameters:

   | Name | Description |
   | --- | --- |
   | port | The port from which `mongocryptd` listens for messages.*Default*: `27020` |
   | idleShutdownTimeoutSecs | Number of idle seconds the `mongocryptd` process waits before exiting.*Default*: `60` |
   | mongocryptdURI | The URI on which to run the `mongocryptd` process.*Default*: `"mongodb://localhost:27020"` |
   | mongocryptdBypassSpawn | When `true`, prevents the driver from automatically spawning `mongocryptd`.*Default*: `false` |
   | mongocryptdSpawnPath | The full path to `mongocryptd`.*Default*: Defaults to empty string and spawns from the system path. |

   If a `mongocryptd` process is already running on the port specified by the driver, the driver may log a warning and continue without spawning a new process. Any settings specified by the driver only apply once the existing process exits and a new encrypted client attempts to connect.

### Example

The following code-snippet sets the listening port configuration of `mongocryptd`:

```python
auto_encryption_opts = AutoEncryptionOpts(mongocryptd_spawn_args=['--port=30000'])
```

The following code-snippet sets the default timeout configuration of `mongocryptd`:

```python
auto_encryption_opts = AutoEncryptionOpts(mongocryptd_spawn_args=['--idleShutdownTimeoutSecs=75'])
```

1. Install mongocryptd

   **For supported Linux Operating Systems:** To install the Server package, follow the [install on Linux tutorial](/docs/manual/administration/install-enterprise-linux#std-label-install-enterprise-linux) and install the `mongodb-enterprise` server package. Alternatively, specify `mongodb-enterprise-cryptd` instead to install only the `mongocryptd` binary. The package manager installs the binaries to a location in the system PATH.

   **For OSX:** To install the Server package, follow the [install on MacOS tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-os-x#std-label-install-enterprise-macos). The package manager installs binaries to a location in the system PATH.

   **For Windows:** To install the Server package, follow the [install on Windows tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-windows#std-label-install-enterprise-windows). You must add the `mongocryptd` package to your system PATH after installation. Follow the documented best practices for your Windows installation to add the `mongocryptd` binary to the system PATH.

   **To install from an official tarball / ZIP archive:** To install from an official archive, follow the documented best practices for your operating system to add the `mongocryptd` binary to your system PATH.

2. Configure mongocryptd

   If the driver has access to the `mongocryptd` process, it spawns the process by default. Your application must have write permissions on the working directory to create the `mongocryptd.pid` file.

   **Important: Start on Boot**

   If possible, start `mongocryptd` on boot, rather than launching it on demand.

   Configure how the driver starts `mongocryptd` through the following parameters:

   | Name | Description |
   | --- | --- |
   | port | The port from which `mongocryptd` listens for messages.*Default*: `27020` |
   | idleShutdownTimeoutSecs | Number of idle seconds the `mongocryptd` process waits before exiting.*Default*: `60` |
   | mongocryptdURI | The URI on which to run the `mongocryptd` process.*Default*: `"mongodb://localhost:27020"` |
   | mongocryptdBypassSpawn | When `true`, prevents the driver from automatically spawning `mongocryptd`.*Default*: `false` |
   | mongocryptdSpawnPath | The full path to `mongocryptd`.*Default*: Defaults to empty string and spawns from the system path. |

   If a `mongocryptd` process is already running on the port specified by the driver, the driver may log a warning and continue without spawning a new process. Any settings specified by the driver only apply once the existing process exits and a new encrypted client attempts to connect.

The following code-snippet sets the listening port configuration of `mongocryptd`:

```csharp
var extraOptions = new Dictionary<string, object>()
{
    { "mongocryptdSpawnArgs", new [] { "--port=30000" } },
};
autoEncryptionOptions.With(extraOptions: extraOptions);
```

The following code-snippet sets the default timeout configuration of `mongocryptd`:

```csharp
var extraOptions = new Dictionary<string, object>()
{
    { "idleShutdownTimeoutSecs", 60 },
};
autoEncryptionOptions.With(extraOptions: extraOptions);
```

1. Install mongocryptd

   **For supported Linux Operating Systems:** To install the Server package, follow the [install on Linux tutorial](/docs/manual/administration/install-enterprise-linux#std-label-install-enterprise-linux) and install the `mongodb-enterprise` server package. Alternatively, specify `mongodb-enterprise-cryptd` instead to install only the `mongocryptd` binary. The package manager installs the binaries to a location in the system PATH.

   **For OSX:** To install the Server package, follow the [install on MacOS tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-os-x#std-label-install-enterprise-macos). The package manager installs binaries to a location in the system PATH.

   **For Windows:** To install the Server package, follow the [install on Windows tutorial](/docs/manual/tutorial/install-mongodb-enterprise-on-windows#std-label-install-enterprise-windows). You must add the `mongocryptd` package to your system PATH after installation. Follow the documented best practices for your Windows installation to add the `mongocryptd` binary to the system PATH.

   **To install from an official tarball / ZIP archive:** To install from an official archive, follow the documented best practices for your operating system to add the `mongocryptd` binary to your system PATH.

2. Configure mongocryptd

   If the driver has access to the `mongocryptd` process, it spawns the process by default. Your application must have write permissions on the working directory to create the `mongocryptd.pid` file.

   **Important: Start on Boot**

   If possible, start `mongocryptd` on boot, rather than launching it on demand.

   Configure how the driver starts `mongocryptd` through the following parameters:

   | Name | Description |
   | --- | --- |
   | port | The port from which `mongocryptd` listens for messages.*Default*: `27020` |
   | idleShutdownTimeoutSecs | Number of idle seconds the `mongocryptd` process waits before exiting.*Default*: `60` |
   | mongocryptdURI | The URI on which to run the `mongocryptd` process.*Default*: `"mongodb://localhost:27020"` |
   | mongocryptdBypassSpawn | When `true`, prevents the driver from automatically spawning `mongocryptd`.*Default*: `false` |
   | mongocryptdSpawnPath | The full path to `mongocryptd`.*Default*: Defaults to empty string and spawns from the system path. |

   If a `mongocryptd` process is already running on the port specified by the driver, the driver may log a warning and continue without spawning a new process. Any settings specified by the driver only apply once the existing process exits and a new encrypted client attempts to connect.

The following code-snippet sets the listening port configuration of `mongocryptd`:

```go
extraOptions := map[string]interface{}{
    "mongocryptdSpawnArgs": []string{
        "--port=30000",
    },
}
```

The following code-snippet sets the default timeout configuration of `mongocryptd`:

```go
extraOptions := map[string]interface{}{
    "mongocryptdSpawnArgs": []string{
        "--idleShutdownTimeoutSecs=75",
    },
}
```

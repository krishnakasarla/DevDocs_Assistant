> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Install a Queryable Encryption Compatible Driver and Dependencies

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

To enable Queryable Encryption in your development environment, start by installing a compatible driver and dependencies. Some drivers are packaged with the `libmongocrypt` library, while for others you must install it separately.

## Steps

Select your operating system and driver language for installation steps.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Amazon Linux:

   Create a repository file for the `libmongocrypt` package

   Replace `<linux-version>` in the URL with the following, depending on which version of Amazon Linux you are using:

   - Amazon Linux 2023: `amazon/2023`

   - Amazon Linux 2: `amazon/2013.03`

   - Amazon Linux: `amazon/2`

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/<linux-version>/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Debian:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://packages.debian.org/source/sid/extrepo) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/debian <release>/libmongocrypt/1.17 main" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Red Hat Enterprise Linux:

   Create a repository file for the `libmongocrypt` package

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/redhat/$releasever/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Suse:

   Import the public key used to sign the package repositories

   ```sh
   sudo rpm --import https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Add the repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (e.g. "12" or "15").

   ```sh
   sudo zypper addrepo --gpgcheck "https://libmongocrypt.s3.amazonaws.com/zypper/suse/<release>/libmongocrypt/1.17/x86_64" libmongocrypt
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo zypper -n install libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Ubuntu:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://manpages.ubuntu.com/manpages/focal/man1/extrepo.1p.html) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc
   | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources:

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/ubuntu <release>/libmongocrypt/1.17 universe" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on macOS:

   Install `libmongocrypt` using Homebrew

   ```sh
   brew install mongodb/brew/libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.24.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Windows:

   Download libmongocrypt

   Click [here](https://github.com/mongodb/libmongocrypt/releases/latest) to see the latest `libmongocrypt` release.

   Use `gpg` to verify the signature

   The public key for `libmongocrypt` is available at [https://pgp.mongodb.com](https://pgp.mongodb.com/)

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Amazon Linux:

   Create a repository file for the `libmongocrypt` package

   Replace `<linux-version>` in the URL with the following, depending on which version of Amazon Linux you are using:

   - Amazon Linux 2023: `amazon/2023`

   - Amazon Linux 2: `amazon/2013.03`

   - Amazon Linux: `amazon/2`

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/<linux-version>/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Debian:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://packages.debian.org/source/sid/extrepo) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/debian <release>/libmongocrypt/1.17 main" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Red Hat Enterprise Linux:

   Create a repository file for the `libmongocrypt` package

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/redhat/$releasever/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Suse:

   Import the public key used to sign the package repositories

   ```sh
   sudo rpm --import https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Add the repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (e.g. "12" or "15").

   ```sh
   sudo zypper addrepo --gpgcheck "https://libmongocrypt.s3.amazonaws.com/zypper/suse/<release>/libmongocrypt/1.17/x86_64" libmongocrypt
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo zypper -n install libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Ubuntu:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://manpages.ubuntu.com/manpages/focal/man1/extrepo.1p.html) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc
   | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources:

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/ubuntu <release>/libmongocrypt/1.17 universe" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on macOS:

   Install `libmongocrypt` using Homebrew

   ```sh
   brew install mongodb/brew/libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 3.8.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Windows:

   Download libmongocrypt

   Click [here](https://github.com/mongodb/libmongocrypt/releases/latest) to see the latest `libmongocrypt` release.

   Use `gpg` to verify the signature

   The public key for `libmongocrypt` is available at [https://pgp.mongodb.com](https://pgp.mongodb.com/)

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2) For driver versions 3.0 or later, install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Amazon Linux:

   Create a repository file for the `libmongocrypt` package

   Replace `<linux-version>` in the URL with the following, depending on which version of Amazon Linux you are using:

   - Amazon Linux 2023: `amazon/2023`

   - Amazon Linux 2: `amazon/2013.03`

   - Amazon Linux: `amazon/2`

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/<linux-version>/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

   Set the `LIBMONGOCRYPT_PATH` environment variable to the absolute path of the `libmongocrypt` file.

3) For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

4) For driver versions 3.4.3 or earlier on 64-bit Linux, add the following XML to your `.csproj` file.

   Replace `<MongoDriverEncryptionVersion>` with the installed version of the `MongoDB.Driver.Encryption` package:

   ```xml
   <PropertyGroup>
      <!-- replace the version here with your package version -->
      <MongoDriverEncryptionVersion>3.4.2</MongoDriverEncryptionVersion>
      <MongoDriverEncryptionPath>$(NuGetPackageRoot)mongodb.driver.encryption\$(MongoDriverEncryptionVersion)</MongoDriverEncryptionPath>
   </PropertyGroup>
   <PropertyGroup>
      <!-- Suppresses the duplicate file error -->
      <ErrorOnDuplicatePublishOutputFiles>false</ErrorOnDuplicatePublishOutputFiles>
   </PropertyGroup>
   <!-- Ensures the correct library after build or publish -->
   <Target Name="EnsureCorrectMongoEncryption" AfterTargets="Build;Publish" Condition="'$(RuntimeIdentifier)' != ''">
      <!-- Determine paths based on current operation -->
      <PropertyGroup>
            <_TargetDir Condition="Exists('$(PublishDir)')">$(PublishDir)</_TargetDir>
            <_TargetDir Condition="'$(_TargetDir)' == ''">$(OutputPath)</_TargetDir>
      </PropertyGroup>
      <!-- Copy the correct library based on runtime identifier (RID) -->
      <ItemGroup>
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/x64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-x64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/arm64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-arm64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/alpine/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-musl-arm64'" />
      </ItemGroup>
      <!-- Copy with overwrite -->
      <Copy SourceFiles="@(_CorrectMongoLib)"
            DestinationFolder="$(_TargetDir)"
            Condition="'@(_CorrectMongoLib)' != ''"
            OverwriteReadOnlyFiles="true" />
      <Message Text="Fixed MongoDB encryption library for $(RuntimeIdentifier)"
                  Condition="'@(_CorrectMongoLib)' != ''" />
   </Target>
   ```

5) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2. For driver versions 3.0 or later, install libmongocrypt 1.8.0 or later.

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Debian:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://packages.debian.org/source/sid/extrepo) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/debian <release>/libmongocrypt/1.17 main" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

   Set the `LIBMONGOCRYPT_PATH` environment variable to the absolute path of the `libmongocrypt` file.

   For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

3. For driver versions 3.4.3 or earlier on 64-bit Linux, add the following XML to your `.csproj` file.

   Replace `<MongoDriverEncryptionVersion>` with the installed version of the `MongoDB.Driver.Encryption` package:

   ```xml
   <PropertyGroup>
      <!-- replace the version here with your package version -->
      <MongoDriverEncryptionVersion>3.4.2</MongoDriverEncryptionVersion>
      <MongoDriverEncryptionPath>$(NuGetPackageRoot)mongodb.driver.encryption\$(MongoDriverEncryptionVersion)</MongoDriverEncryptionPath>
   </PropertyGroup>
   <PropertyGroup>
      <!-- Suppresses the duplicate file error -->
      <ErrorOnDuplicatePublishOutputFiles>false</ErrorOnDuplicatePublishOutputFiles>
   </PropertyGroup>
   <!-- Ensures the correct library after build or publish -->
   <Target Name="EnsureCorrectMongoEncryption" AfterTargets="Build;Publish" Condition="'$(RuntimeIdentifier)' != ''">
      <!-- Determine paths based on current operation -->
      <PropertyGroup>
            <_TargetDir Condition="Exists('$(PublishDir)')">$(PublishDir)</_TargetDir>
            <_TargetDir Condition="'$(_TargetDir)' == ''">$(OutputPath)</_TargetDir>
      </PropertyGroup>
      <!-- Copy the correct library based on runtime identifier (RID) -->
      <ItemGroup>
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/x64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-x64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/arm64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-arm64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/alpine/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-musl-arm64'" />
      </ItemGroup>
      <!-- Copy with overwrite -->
      <Copy SourceFiles="@(_CorrectMongoLib)"
            DestinationFolder="$(_TargetDir)"
            Condition="'@(_CorrectMongoLib)' != ''"
            OverwriteReadOnlyFiles="true" />
      <Message Text="Fixed MongoDB encryption library for $(RuntimeIdentifier)"
                  Condition="'@(_CorrectMongoLib)' != ''" />
   </Target>
   ```

4. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2) For driver versions 3.0 or later, install libmongocrypt 1.8.0 or later.

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Red Hat Enterprise Linux:

   Create a repository file for the `libmongocrypt` package

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/redhat/$releasever/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

   Set the `LIBMONGOCRYPT_PATH` environment variable to the absolute path of the `libmongocrypt` file.

   For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

3) For driver versions 3.4.3 or earlier on 64-bit Linux, add the following XML to your `.csproj` file.

   Replace `<MongoDriverEncryptionVersion>` with the installed version of the `MongoDB.Driver.Encryption` package:

   ```xml
   <PropertyGroup>
      <!-- replace the version here with your package version -->
      <MongoDriverEncryptionVersion>3.4.2</MongoDriverEncryptionVersion>
      <MongoDriverEncryptionPath>$(NuGetPackageRoot)mongodb.driver.encryption\$(MongoDriverEncryptionVersion)</MongoDriverEncryptionPath>
   </PropertyGroup>
   <PropertyGroup>
      <!-- Suppresses the duplicate file error -->
      <ErrorOnDuplicatePublishOutputFiles>false</ErrorOnDuplicatePublishOutputFiles>
   </PropertyGroup>
   <!-- Ensures the correct library after build or publish -->
   <Target Name="EnsureCorrectMongoEncryption" AfterTargets="Build;Publish" Condition="'$(RuntimeIdentifier)' != ''">
      <!-- Determine paths based on current operation -->
      <PropertyGroup>
            <_TargetDir Condition="Exists('$(PublishDir)')">$(PublishDir)</_TargetDir>
            <_TargetDir Condition="'$(_TargetDir)' == ''">$(OutputPath)</_TargetDir>
      </PropertyGroup>
      <!-- Copy the correct library based on runtime identifier (RID) -->
      <ItemGroup>
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/x64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-x64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/arm64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-arm64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/alpine/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-musl-arm64'" />
      </ItemGroup>
      <!-- Copy with overwrite -->
      <Copy SourceFiles="@(_CorrectMongoLib)"
            DestinationFolder="$(_TargetDir)"
            Condition="'@(_CorrectMongoLib)' != ''"
            OverwriteReadOnlyFiles="true" />
      <Message Text="Fixed MongoDB encryption library for $(RuntimeIdentifier)"
                  Condition="'@(_CorrectMongoLib)' != ''" />
   </Target>
   ```

4) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2. For driver versions 3.0 or later, install libmongocrypt 1.8.0 or later.

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Suse:

   Import the public key used to sign the package repositories

   ```sh
   sudo rpm --import https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Add the repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (e.g. "12" or "15").

   ```sh
   sudo zypper addrepo --gpgcheck "https://libmongocrypt.s3.amazonaws.com/zypper/suse/<release>/libmongocrypt/1.17/x86_64" libmongocrypt
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo zypper -n install libmongocrypt
   ```

   Set the `LIBMONGOCRYPT_PATH` environment variable to the absolute path of the `libmongocrypt` file.

3. For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

4. For driver versions 3.4.3 or earlier on 64-bit Linux, add the following XML to your `.csproj` file.

   Replace `<MongoDriverEncryptionVersion>` with the installed version of the `MongoDB.Driver.Encryption` package:

   ```xml
   <PropertyGroup>
      <!-- replace the version here with your package version -->
      <MongoDriverEncryptionVersion>3.4.2</MongoDriverEncryptionVersion>
      <MongoDriverEncryptionPath>$(NuGetPackageRoot)mongodb.driver.encryption\$(MongoDriverEncryptionVersion)</MongoDriverEncryptionPath>
   </PropertyGroup>
   <PropertyGroup>
      <!-- Suppresses the duplicate file error -->
      <ErrorOnDuplicatePublishOutputFiles>false</ErrorOnDuplicatePublishOutputFiles>
   </PropertyGroup>
   <!-- Ensures the correct library after build or publish -->
   <Target Name="EnsureCorrectMongoEncryption" AfterTargets="Build;Publish" Condition="'$(RuntimeIdentifier)' != ''">
      <!-- Determine paths based on current operation -->
      <PropertyGroup>
            <_TargetDir Condition="Exists('$(PublishDir)')">$(PublishDir)</_TargetDir>
            <_TargetDir Condition="'$(_TargetDir)' == ''">$(OutputPath)</_TargetDir>
      </PropertyGroup>
      <!-- Copy the correct library based on runtime identifier (RID) -->
      <ItemGroup>
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/x64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-x64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/arm64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-arm64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/alpine/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-musl-arm64'" />
      </ItemGroup>
      <!-- Copy with overwrite -->
      <Copy SourceFiles="@(_CorrectMongoLib)"
            DestinationFolder="$(_TargetDir)"
            Condition="'@(_CorrectMongoLib)' != ''"
            OverwriteReadOnlyFiles="true" />
      <Message Text="Fixed MongoDB encryption library for $(RuntimeIdentifier)"
                  Condition="'@(_CorrectMongoLib)' != ''" />
   </Target>
   ```

5. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2) For driver versions 3.0 or later, install libmongocrypt 1.8.0 or later.

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Ubuntu:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://manpages.ubuntu.com/manpages/focal/man1/extrepo.1p.html) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc
   | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources:

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/ubuntu <release>/libmongocrypt/1.17 universe" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

   Set the `LIBMONGOCRYPT_PATH` environment variable to the absolute path of the `libmongocrypt` file.

3) For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

4) For driver versions 3.4.3 or earlier on 64-bit Linux, add the following XML to your `.csproj` file.

   Replace `<MongoDriverEncryptionVersion>` with the installed version of the `MongoDB.Driver.Encryption` package:

   ```xml
   <PropertyGroup>
      <!-- replace the version here with your package version -->
      <MongoDriverEncryptionVersion>3.4.2</MongoDriverEncryptionVersion>
      <MongoDriverEncryptionPath>$(NuGetPackageRoot)mongodb.driver.encryption\$(MongoDriverEncryptionVersion)</MongoDriverEncryptionPath>
   </PropertyGroup>
   <PropertyGroup>
      <!-- Suppresses the duplicate file error -->
      <ErrorOnDuplicatePublishOutputFiles>false</ErrorOnDuplicatePublishOutputFiles>
   </PropertyGroup>
   <!-- Ensures the correct library after build or publish -->
   <Target Name="EnsureCorrectMongoEncryption" AfterTargets="Build;Publish" Condition="'$(RuntimeIdentifier)' != ''">
      <!-- Determine paths based on current operation -->
      <PropertyGroup>
            <_TargetDir Condition="Exists('$(PublishDir)')">$(PublishDir)</_TargetDir>
            <_TargetDir Condition="'$(_TargetDir)' == ''">$(OutputPath)</_TargetDir>
      </PropertyGroup>
      <!-- Copy the correct library based on runtime identifier (RID) -->
      <ItemGroup>
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/x64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-x64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/arm64/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-arm64'" />
            <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/alpine/libmongocrypt.so"
                              Condition="'$(RuntimeIdentifier)' == 'linux-musl-arm64'" />
      </ItemGroup>
      <!-- Copy with overwrite -->
      <Copy SourceFiles="@(_CorrectMongoLib)"
            DestinationFolder="$(_TargetDir)"
            Condition="'@(_CorrectMongoLib)' != ''"
            OverwriteReadOnlyFiles="true" />
      <Message Text="Fixed MongoDB encryption library for $(RuntimeIdentifier)"
                  Condition="'@(_CorrectMongoLib)' != ''" />
   </Target>
   ```

5) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2. For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install version 2.20.0 or later.

2) For driver versions 3.0 or later, install the `MongoDB.Driver.Encryption` package

   Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Amazon Linux:

   Create a repository file for the `libmongocrypt` package

   Replace `<linux-version>` in the URL with the following, depending on which version of Amazon Linux you are using:

   - Amazon Linux 2023: `amazon/2023`

   - Amazon Linux 2: `amazon/2013.03`

   - Amazon Linux: `amazon/2`

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/<linux-version>/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Debian:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://packages.debian.org/source/sid/extrepo) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/debian <release>/libmongocrypt/1.17 main" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Red Hat Enterprise Linux:

   Create a repository file for the `libmongocrypt` package

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/redhat/$releasever/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Suse:

   Import the public key used to sign the package repositories

   ```sh
   sudo rpm --import https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Add the repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (e.g. "12" or "15").

   ```sh
   sudo zypper addrepo --gpgcheck "https://libmongocrypt.s3.amazonaws.com/zypper/suse/<release>/libmongocrypt/1.17/x86_64" libmongocrypt
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo zypper -n install libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Ubuntu:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://manpages.ubuntu.com/manpages/focal/man1/extrepo.1p.html) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc
   | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources:

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/ubuntu <release>/libmongocrypt/1.17 universe" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on macOS:

   Install `libmongocrypt` using Homebrew

   ```sh
   brew install mongodb/brew/libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 1.12 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Windows:

   Download libmongocrypt

   Click [here](https://github.com/mongodb/libmongocrypt/releases/latest) to see the latest `libmongocrypt` release.

   Use `gpg` to verify the signature

   The public key for `libmongocrypt` is available at [https://pgp.mongodb.com](https://pgp.mongodb.com/)

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/languages/java/reactive-streams-driver/current/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2) Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2. Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2) Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2. Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2) Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2. Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install version 5.5.0 or later.

2) Install the `mongodb-client-encryption` package

   Install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later. If you're using Node.js driver version 6.0 or later, you must also use `mongodb-client-encryption` 6.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install version 1.16 or later.

2. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2) Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2. Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2) Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2. Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2) Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2. Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install version 4.4 or later.

2) Install the `pymongocrypt` package

   Install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2. Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2) Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2. Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2) Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2. Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2) Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install version 2.19 or later.

2. Install the `libmongocrypt-helper` package

   Install [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Amazon Linux:

   Create a repository file for the `libmongocrypt` package

   Replace `<linux-version>` in the URL with the following, depending on which version of Amazon Linux you are using:

   - Amazon Linux 2023: `amazon/2023`

   - Amazon Linux 2: `amazon/2013.03`

   - Amazon Linux: `amazon/2`

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/<linux-version>/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Debian:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://packages.debian.org/source/sid/extrepo) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/debian <release>/libmongocrypt/1.17 main" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Red Hat Enterprise Linux:

   Create a repository file for the `libmongocrypt` package

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/redhat/$releasever/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Suse:

   Import the public key used to sign the package repositories

   ```sh
   sudo rpm --import https://pgp.mongodb.com/libmongocrypt.asc
   ```

   Add the repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (e.g. "12" or "15").

   ```sh
   sudo zypper addrepo --gpgcheck "https://libmongocrypt.s3.amazonaws.com/zypper/suse/<release>/libmongocrypt/1.17/x86_64" libmongocrypt
   ```

   Install the `libmongocrypt` package

   ```sh
   sudo zypper -n install libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Ubuntu:

   Configure the repository

   **Note:**

   If you are using the [extrepo](https://manpages.ubuntu.com/manpages/focal/man1/extrepo.1p.html) repository manager, you can view and enable the `libmongocrypt` repository by running the commands:

   ```sh
   extrepo search libmongocrypt
   sudo extrepo enable libmongocrypt
   ```

   To configure the repository manually:

   Import the public key used to sign the package repositories:

   ```sh
   sudo sh -c 'curl -s --location https://pgp.mongodb.com/libmongocrypt.asc
   | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'
   ```

   Add the MongoDB repository to your package sources:

   **Important:**

   Change `<release>` in the following shell command to your platform release (for example "xenial" or "buster").

   ```sh
   echo "deb https://libmongocrypt.s3.amazonaws.com/apt/ubuntu <release>/libmongocrypt/1.17 universe" | sudo tee /etc/apt/sources.list.d/libmongocrypt.list
   ```

   Update the package cache

   ```sh
   sudo apt-get update
   ```

   Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on macOS:

   Install `libmongocrypt` using Homebrew

   ```sh
   brew install mongodb/brew/libmongocrypt
   ```

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

1. Install a compatible driver version

   To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install version 2.4.0 or later.

2. Install libmongocrypt 1.8.0 or later

   The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

   **Warning:**

   Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

   To install on Windows:

   Download libmongocrypt

   Click [here](https://github.com/mongodb/libmongocrypt/releases/latest) to see the latest `libmongocrypt` release.

   Use `gpg` to verify the signature

   The public key for `libmongocrypt` is available at [https://pgp.mongodb.com](https://pgp.mongodb.com/)

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1. Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2. Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3. Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

1) Install a compatible driver version

   To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install version 4.10.0 or later.

2) Install the `mongodb-crypt` package

   Install [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

3) Start a MongoDB Atlas Cluster or Enterprise instance.

   See [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) to learn about starting a MongoDB instance.

## Next Steps

Once you have installed your driver dependencies, [install and configure a query analysis component](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library) to continue setting up your deployment and development environment.

> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Install libmongocrypt for CSFLE

## Overview

Learn how to install `libmongocrypt`, a [core component](/docs/manual/core/csfle/reference/encryption-components#std-label-csfle-reference-encryption-components) of Client-Side Field Level Encryption.

The `libmongocrypt` library performs encryption and decryption, and manages communication between the driver and the Key Management System (KMS (Key Management System)).

**Warning:**

Do not build `libmongocrypt` from source. Install and verify the package by following the steps on this page.

## Steps

Select your operating system for installation steps.

To install on macOS:

1. Install `libmongocrypt` using Homebrew

   ```sh
   brew install mongodb/brew/libmongocrypt
   ```

To install on Windows:

1. Download libmongocrypt

   Click [here](https://github.com/mongodb/libmongocrypt/releases/latest) to see the latest `libmongocrypt` release.

2. Use `gpg` to verify the signature

   The public key for `libmongocrypt` is available at [https://pgp.mongodb.com](https://pgp.mongodb.com/)

To install on Amazon Linux:

1. Create a repository file for the `libmongocrypt` package

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

2. Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

To install on Debian:

1. Configure the repository

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

2. Update the package cache

   ```sh
   sudo apt-get update
   ```

3. Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

To install on Red Hat Enterprise Linux:

1. Create a repository file for the `libmongocrypt` package

   ```sh
   [libmongocrypt]
   name=libmongocrypt repository
   baseurl=https://libmongocrypt.s3.amazonaws.com/yum/redhat/$releasever/libmongocrypt/1.17/x86_64
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/libmongocrypt.asc
   ```

2. Install the `libmongocrypt` package

   ```sh
   sudo yum install -y libmongocrypt
   ```

To install on Suse:

1. Import the public key used to sign the package repositories

   ```sh
   sudo rpm --import https://pgp.mongodb.com/libmongocrypt.asc
   ```

2. Add the repository to your package sources

   **Important:**

   Change `<release>` in the following shell command to your platform release (e.g. "12" or "15").

   ```sh
   sudo zypper addrepo --gpgcheck "https://libmongocrypt.s3.amazonaws.com/zypper/suse/<release>/libmongocrypt/1.17/x86_64" libmongocrypt
   ```

3. Install the `libmongocrypt` package

   ```sh
   sudo zypper -n install libmongocrypt
   ```

To install on Ubuntu:

1. Configure the repository

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

2. Update the package cache

   ```sh
   sudo apt-get update
   ```

3. Install `libmongocrypt`

   ```sh
   sudo apt-get install -y libmongocrypt-dev
   ```

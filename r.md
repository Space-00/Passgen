# MITM-DomainFronting

First of all, this method is not going to revive your config and provide full internet access; rather, it makes some specific services directly accessible (without needing a server or even a worker).

At the moment (1405/1/31), using this method only provides access to Google services (meet, drive, ...) and some sites behind Vercel (vercel.com, ...) and some sites behind Fastly (reddit, github, ...).

Some services like YouTube videos have their own specific service, and some services like Gemini have blocked Iranian IPs, so not all Google services are accessible.

As soon as any other service becomes accessible with this method, I will update accordingly.

This method is usable on Windows, Linux, Mac, and Android (no root required).

///

I initially wrote this project [here](https://github.com/patterniha/MMDF), and then with the efforts made [here](https://github.com/XTLS/Xray-core/issues/4348), we added it to Xray-core, meaning you can now use this method with a simple v2ray config.

The method works, as its name suggests, by first spoofing the identity of the original server to receive unencrypted data from the browser, then sending it to the original server with a fake SNI.

The initial setup of the method takes a few lengthy steps, but after setup, a simple on/off switch is enough to enable/disable the method.

## Setup on Windows

1. First, download and extract the latest version of v2rayN (v2rayN-windows-64.zip) from [https://github.com/2dust/v2rayN/releases](https://github.com/2dust/v2rayN/releases).

2. Now you need a personal certificate. For this, move the file `certificate-generator.bat` to the folder `v2rayN-windows-64\bin` and run it there. Wait a moment, then two files `mycert.crt` and `mycert.key` will be created.

**Warning: Be sure to use your own personal certificate and never use someone else's certificate (crt). Also, never give your private key (key) file to anyone.**

3. Now you must introduce the generated certificate (crt) as a trusted root certificate to the operating system (for system-wide trust) or to a specific browser.

To introduce to the OS: right-click on `mycert.crt`, select "Install certificate", choose "Local Machine", then on the next page select "Place all certificates in the following store", browse to "Trusted Root Certification Authorities", and confirm.

For a browser, for example Chrome, follow these steps:
Settings -> Privacy and security -> Security -> Manage certificates -> Manage imported certificates from Windows -> Trusted Root Certification Authorities -> Import -> Select `mycert.crt` file -> Place all certificates in the following store -> Select "Trusted Root Certification Authorities".

4. Run v2rayN and from the "Configuration" menu, click on "Add a custom configuration". Choose a custom name, import the `MITM-DomainFronting.json` config file. Set "core type" to "xray" and make sure "socks port" is left empty.

5. Select the config and choose "Set system proxy". You're done. Now you can use this method on the browser where you installed the certificate (or on the whole system if you introduced the certificate to the OS).

## Setup on Android

1. First, download and install the latest version of v2rayNG from [https://github.com/2dust/v2rayNG/releases](https://github.com/2dust/v2rayNG/releases).

2. Now you need a personal certificate. You can transfer the `mycert.crt` and `mycert.key` files you created on Windows to your phone and use them. Alternatively, for example, you can directly use the site  
[https://regery.com/en/security/ssl-tools/self-signed-certificate-generator](https://regery.com/en/security/ssl-tools/self-signed-certificate-generator)  
to generate a certificate with a custom name and download both the crt and key files. In this case, rename the crt file to `mycert.crt` and the key file to `mycert.key`.

**Warning: Be sure to use your own personal certificate and never use someone else's certificate (crt). Also, never give your private key (key) file to anyone.**

3. In the v2rayNG app, go to the "Asset files" section and add both `mycert.crt` and `mycert.key`.

4. Now you must install the certificate (crt) as a trusted root certificate on the Android OS. Follow these steps:

Setting -> Security and privacy -> More security settings -> Install from device storage -> CA Certificate -> Install anyway -> Select the `mycert.crt` file on your storage.

If this step is done successfully, you can view the installed certificate under:
Setting -> Security and privacy -> More security settings -> View security certificates -> User.

Note: these steps may vary slightly on different phones.

5. Import the `MITM-DomainFronting.json` config via "import from locally" in v2rayNG and run it. Also make sure that "Enable Hev TUN FEATURE" is active in v2rayNG settings.

6. You're done. Now you can use this method on the Chrome browser (and all Chromium-based browsers in general).

If you are using Firefox, you need to perform these extra steps:
Firefox browser -> Settings -> About Firefox -> Tap the Firefox logo five times -> Navigate to Settings -> Secret Settings -> Toggle "Use third party CA certificates".

Note: for non-rooted Android, you can only use this method through browsers; standalone apps usually do not support this method.

# Warnings and Tips

1. **I emphasize again: do not take certificate (crt) files from anyone and do not give your private key (key) file to anyone. Simply put, do not give or take these two files; create and use them personally.**

2. For non-rooted Android, this method can only be used on browsers, and standalone apps usually do not support it. Therefore, to use Google Meet, Google Drive, etc., you must use the browser.

3. A lot of effort has been put into this program, from writing the initial Python code to adding it to the Xray core. I hope I am not forgotten; big tasks are still ahead...

USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424

USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o

@patterniha

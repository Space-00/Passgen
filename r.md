# MITM-DomainFronting

<div dir="rtl">

First of all, this method is not going to make your configuration live and provide full access to the internet, but rather it will make some specific services directly accessible (without the need for a server or even a worker).

Currently (1405/1/31) implementing this method only provides access to Google services (meet, drive, ...) and some sites behind vercel including (vercel.com, ...) and some sites behind fastly including (reddit, github, ...)

Some services like YouTube videos have their own service and some services like gemini have also banned Iranian IPs, so not all Google services are available.

I will make the necessary update as soon as any other service is available with this method.

This method can be implemented on Windows, Linux, Mac and Android (without the need for root).

///
I first wrote this project in
[here][https://github.com/patterniha/MMDF]
and then with the efforts made in
[here][https://github.com/XTLS/Xray-core/issues/4348]
we added it to Xray-core, which means that now you can use this method with a simple v2ray configuration.

How the method works, as its name suggests, first it fakes the identity of the main server to receive unencrypted data from the browser, then it sends it to the main server with a fake SNI.

The initial setup of the method has a few long steps, but after completing the settings, only a simple on/off is required to enable/disable the method.

## Setup on Windows

1. First, download and extract the latest version of the 
v2rayN program

2. Now you need a personal certificate. To do this, move the 
certificate-generator.bat
file to the 
v2rayN-windows-64\bin
folder and run it there. Wait a while, then two files 
mycert.crt
and 
mycert.key
will be created.

**Warning: Be sure to use your personal certificate and do not use anyone else's certificate (crt) under any circumstances, and do not give your private key file (key) to anyone.

3. Now you need to introduce the created certificate (crt) as a trusted root certificate to the operating system (for verification on the entire system) or to a specific browser.

To introduce it to the operating system, you need to right-click on mycert.crt and select install certificate, then select the local machine option. On the next page, 
place all certificates in the following store 
Trusted Root Certification Authorities
Select and confirm
For the browser, for example Chrome, you need to follow the steps below
Settings -> Privacy and security -> Security -> Manage certificates -> Manage imported certificates from Windows -> Trusted Root Certification Authorities -> Import -> Select mycert.crt file -> Place all certificates in the following store -> Select "Trusted Root Certification Authorities"
4. Run the v2rayN software and click on 
add a custom configuration
from the configuration section. Now choose a desired name and enter the 
MITM-DomainFronting.json
config file. 
Be sure to leave the 
core type 
on xray and the socks port empty.

5. Select the config and select set system proxy. 
That's it. Now you can use this method on the browser where you entered the certificate (or the entire system if you introduced the certificate to the operating system).

## Setup on Android

1. First, download and install the latest version of the v2rayNG program from 
https://github.com/2dust/v2rayNG/releases

2. Now you need a personal certificate. To do this, you can transfer the same files 
mycert.crt, mycert.key
that you created in Windows to your phone and use them. Or, for example, you can download them directly from the site.

https://regery.com/en/security/ssl-tools/self-signed-certificate-generator

با یک نام دلخواه سرتیفیکیت بسازید و هر دو فایل crt و key را دانلود کنید
در این صورت باید نام فایل crt را به mycert.crt و نام فایل key را به mycert.key تغییر دهید

**هشدار: حتما از سرتیفیکیت شخصی خود استفاده کنید و به هیچ عنوان از سرتیفیکیت (crt) دیگران استفاده نکنید و همچنین فایل پرایویت‌کی (key) خود را به هیچ شخصی ندهید**

۳. در برنامه v2rayNG و در قسمت Asset files هر دو فایل
mycert.crt, mycert.key
را وارد کنید

۴. حال باید سرتیفیک (crt) را به عنوان یک trusted root certificate به سیستم عامل اندروید معرفی کنید برای این کار مراحل زیر را طی کنید:

Setting -> Security and privacy -> More security settings -> Install from device storage -> CA Certificate -> Install anyway -> Select mycert.crt file on your storage.

اگر با موفقیت این قسمت انجام شود میتوانید سرتیفیکیت وارد شده را در قسمت

Setting -> Security and privacy -> More security settings -> View security certificates -> User.

مشاهده کنید، دقت کنید که این مراحل ممکن است بر روی گوشی های مختلف کمی متفاوت باشد

۵. کانفیگ 
MITM-DomainFronting.json 
را از طریق
import from locally
وارد برنامهv2rayNG کنید و اجرا کنید
همچنین دقت کنید که Enable Hev TUN FEATURE در تنظیمات v2rayNG فعال باشد

۶. کار تمام است اکنون میتوانید بر روی مرورگر کروم (و به طور کلی تمامی مرورگرهای مبتنی بر کرومیوم) از این متد استفاده کنید

و در صورتی که از مرورگر فایرفاکس استفاده میکنید باید مراحل اضافه زیر را طی کنید

firefox browser -> Settings -> About Firefox -> Tap the Firefox logo five times -> Navigate to Settings -> Secret Settings -> Toggle "Use third party CA certificates"

دقت کنید برای اندروید غیر روت فقط از طریق مرورگرها میتوانید ازین متد استفاده کنید و برنامه های مستقل امکان استفاده از این متد را معمولا ندارند.


# هشدار ها و نکات

۱. **باز هم تاکید میکنم فایل سرتیفیکیت (crt) را از کسی نگیرید و فایل پرایویت‌کی (key) را به هیچ شخصی ندهید به طور ساده این دو فایل را نه به کسی بدهید و نه از کسی بگیرید و خودتان به صورت شخصی ایجاد و از آن استفاده کنید**


۲. برای اندروید غیر روت ازین متد فقط میتوانید بر روی مرورگرها استفاده کنید و اپ های مستقل معمولا از این متد پشتیبانی نمیکنند

 بنابراین برای استفاده از google meet و یا google drive و ... باید از مرورگر استفاده کنید.
 
۳. زحمت زیادی برای برای این برنامه کشیده شده از نوشتن کد پایتون اولیه تا اضافه کردن آن به هسته xray امیدوارم حمایت از بنده فراموش نشه همچنان کارهای بزرگی در پیش هست ...

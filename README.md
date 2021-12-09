# MagnusBilling API
PHP wrapper for the MagnusBilling API. <a href="https://www.magnusbilling.org" title="Magnusbilling. The best opensource of the world" alt="Magnusbilling. The best opensource of the world" />https://www.magnusbilling.org</a>


[![Total Downloads](https://poser.pugx.org/magnussolution/magnusbilling-api/downloads)](https://packagist.org/packages/magnussolution/magnusbilling-api)
[![License](https://poser.pugx.org/magnussolution/magnusbilling-api/license)](https://packagist.org/packages/magnussolution/magnusbilling-api)
<span class="badge-ehereum"><a href="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=0x74b1a21084e6226e65a679d65d6e8a4c8bf0b3de" title="Donate once-off to this project using Ethereum"><img src="https://img.shields.io/badge/ethereum-donate-blue.svg" alt="Ethereum donate button" /></a></span>
<span class="badge-bitcoin"><a href="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=1CUfiWYMSf7gDYH5w54ukqzFv2NRcY97ff" title="Donate once-off to this project using Bitcoin"><img src="https://img.shields.io/badge/bitcoin-donate-yellow.svg" alt="Bitcoin donate button" /></a></span>


Requirements
------------
The minimum requirement by MagnusBilling API is that your Web server supports PHP 5.4.

Installation
------------
To install MagnusBilling API package you can run this simple command
```
composer require magnussolution/magnusbilling-api
```


Usage
-----
```javascript

require_once "vendor/autoload.php";

use magnusbilling\api\magnusBilling;

$magnusBilling             = new MagnusBilling('API KEY', 'SECRET KEY');
$magnusBilling->public_url = "http://1.1.1.1/mbilling"; // Your MagnusBilling URL

//read data from user module
$result = $magnusBilling->read('user');

```

[Read the wiki to more detais.](https://github.com/magnussolution/magnusbilling-api-php/wiki)


Donate
-----
You can support this project by continuously donations to
 * BTC wallet: `1CUfiWYMSf7gDYH5w54ukqzFv2NRcY97ff`
 * ETH wallet: ` 0x74b1a21084e6226e65a679d65d6e8a4c8bf0b3de`

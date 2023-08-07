<?php
require_once "vendor/autoload.php";

use magnusbilling\api\magnusBilling;

$magnusBilling = new MagnusBilling('API_KEY', 'SECRET_KEY');

// Your MagnusBilling URL
$magnusBilling->public_url = "http://x.x.x.x/mbilling";

$result = $magnusBilling->releaseDID('343434');

print_r($result);

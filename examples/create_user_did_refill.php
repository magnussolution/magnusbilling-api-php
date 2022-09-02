<?php
require_once "vendor/autoload.php";

use magnusbilling\api\magnusBilling;

$magnusBilling = new MagnusBilling('API_KEY', 'SECRET_KEY');

// Your MagnusBilling URL
$magnusBilling->public_url = "http://x.x.x.x/mbilling";

$result = $magnusBilling->createUser([
    'username'  => 'marcos',
    'password'  => 'password',
    'active'    => '1',
    'firstname' => 'my name',
    'password'  => 'new_password',
    'email'     => '',
    'id_group'  => 3, //DEFAULT: GROUP USER
    'id_plan'   => 8, //DEFAULT: GET THE FIRST PLAN THAT YOU SET TO USE IN SIGNUP
    'credit'    => 0, //DEFAULT: GET THE CREDIT FROM THE PLAN
]);

$id_user = $result['data']['id'];

$magnusBilling->setFilter('id_user', $id_user, 'eq', 'numeric');
$resultSip = $magnusBilling->read('sip', 1);

$id_sip = $resultSip['rows'][0]['id'];

//Send especific data
$result = $magnusBilling->create('did', [
    'did'      => '552140040001',
    'id_user'  => $id_user,
    'reserved' => 1,

]);

$id_did = $result['rows'][0]['id'];

$result = $magnusBilling->buyDID($id_did, $id_user);

$result = $magnusBilling->create('refill', [
    'id_user'     => $id_user,
    'credit'      => 10,
    'payment'     => 1,
    'description' => 'Insert 10 credit from API',
]);

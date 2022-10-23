<?php

$secretKey = "d1191496464bf1e52777";

class User {
    public $isAdmin = false;
    public $login = "";

    public function __construct($login, $is_admin) {
        $this->login = $login;
        $this->isAdmin = $is_admin;
    }
}

$user = new User("some", true);
$serialized = serialize($user);

echo @openssl_encrypt($serialized, "aes-128-cbc", $secretKey);

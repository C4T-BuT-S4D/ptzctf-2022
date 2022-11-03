<?php

class User {
    public $isAdmin = false;
    public $login = "";

    public function __construct($login, $is_admin) {
        $this->login = $login;
        $this->isAdmin = $is_admin;
    }
}

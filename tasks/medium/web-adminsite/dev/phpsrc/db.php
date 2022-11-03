<?php

require_once "user.php";

class DB {
    protected $users;

    public function __construct() {
        $users_file = getenv("USERS_FILE");
        if ($users_file == "") {
            $users_file = "/users.json";
        }
        $this->users = json_decode(file_get_contents($users_file), true);
    }

    function getUser($login, $password) {
        foreach ($this->users as $u) {
            if ($u['login'] === $login && $u['password'] == $password) {
                return new User($u["login"], $u["is_admin"]);
            }
        }
        return null;
    }
}
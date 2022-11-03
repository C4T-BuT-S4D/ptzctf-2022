<?php

require_once "user.php";


class Session {
    const ENCRYPTION_KEY = "d1191496464bf1e52777";

    public static function get_user() {
        $cookieVal = $_COOKIE["my-session"] ?? "";
        if ($cookieVal == "") {
            return null;
        }

        $decrypted = @openssl_decrypt($cookieVal, "aes-128-cbc", self::ENCRYPTION_KEY);
        if (!$decrypted) {
            return null;
        }
        
        return unserialize($decrypted) ?? null;
    }

    public static function save_user($user) {
        $serialized = serialize($user);
        $encrypted = @openssl_encrypt($serialized, "aes-128-cbc", self::ENCRYPTION_KEY);
        setcookie("my-session", $encrypted);
    }
}



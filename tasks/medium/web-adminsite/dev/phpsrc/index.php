<?php

require_once "session.php";

$user = Session::get_user();

if ($user == null) {
    header("Location: /login.php");
    die();
}

echo "<h4>You are logged in as '{$user->login}' </h3>";

if ($user->isAdmin === true) {
    echo "Your flag is " . getenv('FLAG');
    die();
}


echo "<p>There is no flag for you. Sorry for that. </p>";
die();
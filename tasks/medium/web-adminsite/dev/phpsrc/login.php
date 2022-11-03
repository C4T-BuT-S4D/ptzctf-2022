<?php

require_once "db.php";
require_once "session.php";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $login = $_POST["login"];
    $password = $_POST["password"];
    
    $db = new DB();
    
    $u = $db->getUser($login, $password);
    
    if ($u === null) {
        die("No such user;");
    }
    
    Session::save_user($u);
    
    header('Location: /index.php');    
}

?>

<html>
   <body>

   <p>Please, login</p>

      <form action="" method="POST">
        <label>
            Login:
            <input type="text" name="login">
        </label>
        
        <br>
        <br>

        <label>
            Password:
             <input type="text" name="password">
        </label>
        
        <br>
        <input type="submit" value = "login"/>
      </form>
      
   </body>
</html>
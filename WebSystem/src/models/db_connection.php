<?php

# Dados de login do banco de dados
$host = 'localhost';
$users = 'root';
$db_password = 'root';

# Conexão com banco de dados de usuarios do sistema
function netmon_users_db_connection(){
    global $host, $users, $db_password;
    $db_name = 'netmon_users';
    $conn = new mysqli($host, $users, $db_password, $db_name);
    if ($conn->connect_error){
        echo("Conexão com o db " . $db_name . " falhou: " . $conn->connect_error);
        header('Location: ../../views/public/error.php');
    }else{
        echo "Conectado com sucesso!";
        return $conn;
    }
}

?>
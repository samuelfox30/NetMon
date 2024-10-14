<?php

if (isset($_GET['token'])) {

    # Realizando a conexão com banco de dados
    require_once '../db_connection.php';
    $conn = netmon_users_db_connection();
    $token = $_GET['token'];

    $sql = "SELECT * FROM usuarios WHERE token = ? AND is_active = 0";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $token);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 1) {
        $sql_update = "UPDATE usuarios SET is_active = 1 WHERE token = ?";
        $stmt_update = $conn->prepare($sql_update);
        $stmt_update->bind_param("s", $token);
        
        if ($stmt_update->execute()) {
            echo "<h1 class='mensagem'>Email verificado com sucesso! Sua conta foi ativada.</h1>";
        } else {
            echo "<h1 class='mensagem'>Erro ao verificar o e-mail.</h1>";
        }
    }else{
        header("Location: ../../../../index.php");
    }
}

?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verificar email</title>
</head>
<body>
    Um email de verificação foi enviado para seu email.
</body>
</html>
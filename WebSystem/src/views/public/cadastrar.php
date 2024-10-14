<?php

if (isset($_GET['erros'])) {
    $erros = urldecode($_GET['erros']);
    echo "<div class='erro'>$erros</div>";
}
if (isset($_GET['email_ja_cadastrado'])) {
    $email_ja_cadastrado = urldecode($_GET['email_ja_cadastrado']);
    echo "<div class='email_ja_cadastrado'>$email_ja_cadastrado</div>";
}

?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastrar</title>

    <!-- Importando CSS File -->
    <link rel="stylesheet" href="../../styles/css/cadastrar.css">
    <link rel="stylesheet" href="../../styles/css/global.css">

</head>
<body>
    <form action="../../models/public/cadastrar_usuario.php" method="post" novalidate>
        <br>
        <input type="text" name="name" id="name" placeholder="Digite seu nome:" maxlength="50">
        <br>
        <input type="email" name="email" id="email" placeholder="Digite seu e-mail:" maxlength="50">
        <br>
        <input type="password" name="password" id="password" placeholder="Digite sua senha:" minlength="8" maxlength="20">
        <br>
        <input type="submit" name="submit" id="submit" value="Enviar">   
    </form>
</body>
</html>
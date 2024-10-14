<?php

if (isset($_POST['submit'])) {

    /* ------------------------------ Captura de dados ------------------------------ */
    $name = $_POST['name'];
    $email = $_POST['email'];
    $password = $_POST['password'];

    /* ------------------------------ Tratamento dos dados ------------------------------ */
    $erros = [];
    # Verifica se tem algum campo vazio
    if(empty($name) || empty($email) || empty($password)) {
        $erros[] = "Preencha todos os campos";
    }else{
        # Verifica tamanho do texto do campo nome
        if(strlen($name)<2 || strlen($name)>50){
            $erros[] = "Os nome deve ter entre 2 e 50 caracteres";
        }
        # Verifica tamanho do email
        if (strlen($email) < 5 || strlen($email) > 50) {
            $erros[] = "O e-mail deve ter entre 5 e 50 caracteres";
        }
        # Verifica formatação do e-mail
        if(!filter_var($email, FILTER_VALIDATE_EMAIL)){
            $erros[] = "Preencha o e-mail corretamente";
        }
        # Verifica o tamanho da senha
        if (strlen($password) < 8 || strlen($password) > 20) {
            $erros[] = "A senha deve ter entre 8 e 20 caracteres";
        }
    }
    # Se houver erros, as informações do erro são retornadas
    if(!empty($erros)){
        # Formata o texto de erro para poder ser passado em uma url 
        $erro_string = urlencode(implode(", ", $erros));
        # Manda os erros para a pagina de cadastro
        header("Location: ../../views/public/cadastrar.php?erros=$erro_string");
    # Se não houver erros...
    }else{
        /* ------------------------------ Conecta com banco de dados ------------------------------ */
        require_once '../db_connection.php';
        $conn = netmon_users_db_connection();

        /* ------------------------------ Verifica se e-mail já está cadastrado ------------------------------ */
        $sql_v_e = "SELECT * FROM usuarios WHERE email = ?";
        $stmt_v_e = $conn->prepare($sql_v_e);
        $stmt_v_e->bind_param("s", $email);
        $stmt_v_e->execute();
        $result_v_e = $stmt_v_e->get_result();

        if ($result_v_e->num_rows > 0) {
            // Se o e-mail já estiver cadastrado
            $mensagem_ja_cadastrado = "Esse e-mail já está cadastrado no sistema";
            header("Location: ../../views/public/cadastrar.php?email_ja_cadastrado=$mensagem_ja_cadastrado");
        } else {
            // E-mail não está cadastrado, prosseguir com o registro
            /* ------------------------------ Adiciona os dados no banco de dados ------------------------------ */
            $token_generated = bin2hex(random_bytes(32));
            $stmt = $conn->prepare("INSERT INTO usuarios (nome, email, senha, token) VALUES (?, ?, ?, ?)");
            $stmt->bind_param("ssss", $name, $email, $password, $token_generated);
            // Executa a consulta
            if ($stmt->execute()) {
                $verification_link = "https://localhost/NetMon/WebSystem/src/models/public/verificar_email.php?token=$token_generated";
                $to = $email;
                $subject = "Verificação de Email";
                $message = "Clique no link abaixo para verificar seu email: \n\n$verification_link";
                $headers = "From: no-reply@netmonproject.com.br";
        
                // Função de envio de email (assumindo que seu servidor suporte)
                if (mail($to, $subject, $message, $headers)) {
                    header('Location: ../../views/public/verificar_email.php');
                } else {
                    echo "Erro ao enviar email.";
                }
            } else {
                echo "Erro ao executar informações do banco de dados: " . $stmt->error;
            }
            # Fecha conexão
            $stmt->close();
            $conn->close();

            /* ------------------------------ Verifica e-mail ------------------------------ */
            
        }
    }

}else{

    header('Location: ../../views/public/cadastrar.php');

}



?>
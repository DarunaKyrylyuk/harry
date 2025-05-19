<?php
$host = "localhost"; // або IP
$user = "root";      // ім’я користувача MySQL
$pass = "";          // пароль
$db = "harry_blog";  // назва БД

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Помилка підключення: " . $conn->connect_error);
}

$name = $_POST['name'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_BCRYPT);

$sql = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("sss", $name, $email, $password);

if ($stmt->execute()) {
    echo "Успішна реєстрація!";
} else {
    echo "Помилка: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>

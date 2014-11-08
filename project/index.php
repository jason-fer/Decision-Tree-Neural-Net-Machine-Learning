<h3>JSON Insert For ML</h3>
<?php 

	$pdo = new PDO('mysql:dbname=machine_learning;host=127.0.0.1', 'root', '');

	// $user_vals = [
	// 	':email' => $email,
	// 	':first' => $first_name,
	// 	':last' => $last_name,
	// 	':password' => $password,
	// 	':temp_password' => Text::random(),
	// 	':temp_password_date' => date('c', strtotime('+7 days')),
	// 	':role' => 'client',
	// 	':last_login' => $time,
	// 	':last_activity_date' => $time,
	// 	':token' => \Bonafide::instance('token')->hash(Arr::get($vals, 'email').$time, null, strlen($email)),
	// 	':last_ip' => \Arr::get($_SERVER, 'REMOTE_ADDR'),
	// ];

	// $sql = "
	// 	INSERT INTO users
	// 	(email, first, last, password, temp_password, temp_password_date, role, last_login, last_activity_date, token, last_ip)
	// 	VALUES(:email, :first, :last, :password, :temp_password, :temp_password_date, :role, :last_login, :last_activity_date, :token, :last_ip)
	// ";

	// // Create user entry
	// $db = static::pdo();
	// $p = $db->prepare($sql);
	// $rs = $p->execute($user_vals);


?>

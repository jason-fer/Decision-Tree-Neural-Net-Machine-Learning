<?php 

	echo '<h3>JSON Insert For ML</h3>';

	$pdo = new PDO('mysql:dbname=machine_learning;host=127.0.0.1', 'root', '');

	$business_vals = [
		':business_id' => $val['business_id'],
		':name' => $val['name'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
		':xxx' => $val['xxx'],
	];

	$business_insert = "
		INSERT INTO `machine_learning`.`business` 
		       (`id`, `type`, `business_id`, `name`, `neighborhoods`, `full_address`, `city`, `state`, `latitude`, `longitude`, `stars`, `review_count`, `categories`, `open`, `hours`, `attributes`) 
		VALUES (NULL, 'business', ':business_id', ':name', 'xxx', 'xxx', 'xxx', 'xxx', '99.9', '99.9', '3', '20', 'xxx', 'True', 'xxx', 'xxx')";

	$checkin_insert = "
		INSERT INTO `machine_learning`.`check-in` 
		       (`id`, `type`, `business_id`, `checkin_info`) 
		VALUES (NULL, 'checkin', '123', 'xxx')";

	$review_insert = "
		INSERT INTO `machine_learning`.`review` 
		       (`id`, `type`, `business_id`, `user_id`, `stars`, `text`, `date`, `votes`) 
		VALUES (NULL, 'review', 'xxx', 'xxx', '3.2', 'xxx', '2014-11-04 00:00:00', '3')";

	$tip_insert = "
		INSERT INTO `machine_learning`.`tip` 
		       (`id`, `type`, `text`, `business_id`, `user_id`, `date`, `likes`) 
		VALUES (NULL, 'tip', 'xxx', 'xxx', 'xxx', '2014-11-24 00:00:00', '3')";

	$user_insert = "
		INSERT INTO `machine_learning`.`user` 
		       (`id`, `user_id`, `type`, `name`, `review_count`, `average_stars`, `votes`, `friends`, `elite`, `yelping_since`, `compliments`, `fans`) 
		VALUES (NULL, 'xxx', 'user', 'xxx', '4', '3.2', 'xxx', 'xxx', '2.2', '2014-11-03 00:00:00', 'xxx', '5')";

	// Create user entry
	// $db = static::pdo();
	// $p = $db->prepare($sql);
	// $rs = $p->execute($user_vals);

?>
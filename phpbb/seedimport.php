<?php
define('IN_PHPBB', true);
$phpbb_root_path = '/opt/bitnami/phpbb/'; // Change this to your phpBB root path
$phpEx = substr(strrchr(__FILE__, '.'), 1);
include($phpbb_root_path . 'common.' . $phpEx);
include($phpbb_root_path . 'includes/functions_user.' . $phpEx);

// Start session management
$user->session_begin();
$auth->acl($user->data);
$user->setup();

// Open the CSV file
$csv = fopen('/opt/bitnami/phpbb/phpbb_export.csv', 'r');

// Loop through each row of data
$import_num = 1;
while (($data = fgetcsv($csv)) !== false) {
  $username = $data[0];
  $email = $data[1];
  $password = $data[2];
  $timestamp = $data[3];

  // Check if the user already exists
  $sql = 'SELECT user_id FROM ' . USERS_TABLE . " WHERE username_clean = '" . $db->sql_escape(utf8_clean_string($username)) . "'";
  $result = $db->sql_query($sql);
  $existing_user = $db->sql_fetchrow($result);
  $db->sql_freeresult($result);

  if (!$existing_user) {
    // Create the new user
    $user_row = array(
      'username' => $username,
      'user_password' => phpbb_hash($password),
      'user_email' => $email,
      'group_id' => 2, // Change this to the group ID you want the user to belong to
      'user_type' => USER_NORMAL,
      'user_regdate' => $timestamp, // time(),
      'user_lastvisit' => 0,
      'user_lastmark' => 0,
      'user_lastpost_time' => 0,
      'user_lastpage' => '',
      'user_posts' => 0,
      'user_timezone' => 0,
      'user_lang' => 'en',
      'user_dateformat' => $user->data['user_dateformat'],
      'user_inactive_reason' => 0,
      'user_inactive_time' => 0,
      'user_actkey' => '',
      'user_ip' => $user->ip,
      'user_new' => 1,
    );
    $user_id = user_add($user_row);

    // Log the user in
    $result = $auth->login($username, $password);

    if ($result['status'] == LOGIN_SUCCESS) {
      echo "[Entry #$import_num] User $username created and logged in successfully.\n";
    } else {
      echo "[Entry #$import_num] Error creating user $username: " . $result['error_msg'] . "\n";
    }
  } else {
    echo "[Entry #$import_num] User $username already exists, skipping...\n";
  }
  $import_num++;
}

// Close the CSV file
fclose($csv);

// End session management
$user->session_kill();
$user->session_begin();
?>
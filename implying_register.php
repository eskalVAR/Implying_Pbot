<?php

function get_client_ip() {
    $ipaddress = '';
    if (getenv('HTTP_CLIENT_IP'))
        $ipaddress = getenv('HTTP_CLIENT_IP');
    else if(getenv('HTTP_X_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_X_FORWARDED_FOR');
    else if(getenv('HTTP_X_FORWARDED'))
        $ipaddress = getenv('HTTP_X_FORWARDED');
    else if(getenv('HTTP_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_FORWARDED_FOR');
    else if(getenv('HTTP_FORWARDED'))
       $ipaddress = getenv('HTTP_FORWARDED');
    else if(getenv('REMOTE_ADDR'))
        $ipaddress = getenv('REMOTE_ADDR');
    else
        $ipaddress = 'UNKNOWN';
    return $ipaddress;
}

$conn = mysqli_connect("localhost", "root", "PASSWORD", "pbot");
$error = false;
$discord_id = mysqli_real_escape_string($conn,$_GET['id']);

if (isset($_POST['name'])) {
    $name = mysqli_real_escape_string($conn,$_POST['name']);
}

if (isset($_POST['email'])) {
    $email = mysqli_real_escape_string($conn,$_POST['email']);
}

if (isset($_POST['reason_join'])) {
    $reason2join = mysqli_real_escape_string($conn,$_POST['reason_join']);
}

if (isset($_POST['in_group'])) {
    $in_fbgroup = mysqli_real_escape_string($conn,$_POST['in_group']);
}

$ip_addr = get_client_ip();

$query_result = $conn->query("SELECT discord_name FROM members_uwu WHERE discord_id=$discord_id AND in_server=1");
$result_array = mysqli_fetch_assoc($query_result);
$discord_name = implode($result_array);

if(empty($name) && empty($email) && empty($reason_join) && empty($in_group) && empty($rule_agree) === true){
    $error = true;
}
elseif(isset($_POST['rule_agree']) && $_POST['rule_agree'] === 'yes'){
    $query = "UPDATE members_uwu SET verified=1, real_name='$name', email='$email', reason_join='$reason2join', in_group='$in_fbgroup', ip_addr='$ip_addr' WHERE discord_id='$discord_id' AND in_server=1";
    $submit_result = $conn->query($query) or trigger_error(mysql_error()." ".$query);
    header("Location:/succ.html");
}
else{
    $rule_error = true;
}
?>

<html >
<head>
  <meta charset="UTF-8">
  <title>/>p/ Registration</title>


      <link rel="stylesheet" href="css/style.css">
      <style type="text/css">
      .reason_join {
}
      </style>
</head>

<body>
  <div id="login-box">
  <div class="left">
    <h1>Welcome <?= $discord_name ?></h1>
<form method="POST">
    <input type="text" name="name" placeholder="Name" />
    <input type="text" name="email" placeholder="E-mail" />
    <input name="reason_join" type="text" class="reason_join" placeholder="Reason for joining" /><br>
    Are you from the FB group ? <br>
    <input type="radio" name="in_group" value="yes" checked>Yes<br>
    <input type="radio" name="in_group" value="no">No<br><br>
    <input type="checkbox" name="rule_agree" value="yes"> I agree to uphold the />p/ constitution at all times<br>

    <input type="submit" name="signup_submit" value="Sign me up" /><br><br>
    <?php if($error = true){?> <font color="red">Please fill in all the fields!</font><br> <?php } ?>
<?php  if($rule_error = true){?> <font color="red">You have to agree with the constitution!</font><br> <?php } ?>
  </div>
</form>
  <div class="right">
<center><h2><b>/>p/ Constitution</b></h2></center>
<b>Art 1:</b> The group is all about />p/ itself and everything else.<br>
<b>Art 2:</b> Your behaviour here must be reasonable, no: spam, virus links, doxxing members, intentional drama, etc.<br>
<b>Art 3:</b> You can advertise your own Game/Project/Group/Page, but you need to do the other way around. <br>
<b>Art 4:</b> Bannable Offenses:<br>
>> Blocking Mods/Admins<br>
>> Epilepsy-triggering GIFs<br>
>> Selling products of any kind<br>
>> Trying to get around our filters will result in a kick/ban<br>
<b>Art 5:</b> Mod applications:<br>
If you wish to become a mod, you either cant or you just have to show your worth on general conversations. Also, mod applications open every now and then.<br>
<b>Art 6:</b> Each moderator is different. It's up to their discretion to handle situations.<br>
<b>Art 7:</b> Follow the correct usage of each channel. You can guide yourself through the descriptions of them.<br>

  </div>
</div>
</body>
</html>

<?php
require_once 'Mobile_Detect.php';
$detect = new Mobile_Detect;

if($detect->isMobile() && !$detect->isTablet()){
    include("register_phone.php");
}
elseif($detect->isTablet()){
    include("register_tablet.php");
}
else{
    include("register_desktop.php");
}

 ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <?php wp_head();?>

</head>
<body class="<?php body_class(); ?>">
<header>


<?php 
$args = array ('theme_location' => 'header-menu',);
wp_nav_menu ($args); 

?>
</header>

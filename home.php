<?php

// index.php


get_header();

// basic wordpress query

$postsargs = array(

    'post_type' => 'post',
    'post_status' => 'publish',
    'posts_per_page' => 3,

);
$posts = new WP_Query( $postsargs );

$moviesargs = array(

    'post_type' => 'movie',
    'post_status' => 'publish',
    'posts_per_page' => 3,

);
$movies = new WP_Query( $moviesargs );

$seriesargs = array(

    'post_type' => 'series',
    'post_status' => 'publish',
    'posts_per_page' => 3,

);
$series = new WP_Query( $seriesargs );


?>

<h2> last Posts </h2>
<div class="row">

<?php

foreach ( $posts->posts as $post ) {
?>
<div>
<h1> <?php the_title() ?> </h1>
<p> <?php the_excerpt() ?> </p>
<img src="<?php the_post_thumbnail_url() ?>" alt="">
<a href="<?php the_permalink() ?>">Read More</a>
</div>

<?php
}
?>
</div>

<h2> last Movies </h2>
<div class="row">

<?php

foreach ( $movies->posts as $post ) {
?>
<div>
<h1> <?php the_title() ?> </h1>
<p> <?php the_excerpt() ?> </p>
<img src="<?php the_post_thumbnail_url() ?>" alt="">
<a href="<?php the_permalink() ?>">Read More</a>
</div>

<?php
}
?>
</div>

<h2> last Series </h2>
<div class="row">

<?php

foreach ( $series->posts as $post ) {
?>
<div>
<h1> <?php the_title() ?> </h1>
<p> <?php the_excerpt() ?> </p>
<img src="<?php the_post_thumbnail_url() ?>" alt="">
<a href="<?php the_permalink() ?>">Read More</a>
</div>

<?php
}
?>
</div>
<?php
get_footer();   

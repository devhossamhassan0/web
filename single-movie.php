<?php
get_header();

?>
<h1>single-movie</h1>
<?php

if ( have_posts() ) :

    while ( have_posts() ) :the_post();
        the_title();
        the_content();
        echo '<img src="' . get_the_post_thumbnail_url() . '" alt="">';

        endwhile;

endif;


get_footer();

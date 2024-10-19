<?php
add_theme_support( 'post-thumbnails' );
add_theme_support( 'menus');


// enqueue scripts and styles

function my_theme_enqueue_styles() {
    wp_enqueue_style( 'main', get_template_directory_uri() . '/style.css' );
}
add_action( 'wp_enqueue_scripts', 'my_theme_enqueue_styles' );

// register menu


    register_nav_menu( 'header-menu', 'Header Menu' );

function movie_post_type(){
    $lables = array(
        'name' => 'Movies',
        'singular_name' => 'Movie',
        'add_new_item' => 'Add New Movie',
        'new_item' => 'New Movie',
        'edit_item' => 'Edit Movie',
        'view_item' => 'View Movie',
        'all_items' => 'All Movies',    



    );

    $args = array(
        'labels' => $lables,
        'menu_icon' => 'dashicons-video-alt2',
        'supports' => array('title' , 'thumbnail', 'excerpt','editor'), 
        'public' => true,
        'has_archive' => true,
    );

    register_post_type('movie', $args);
}

add_action('init', 'movie_post_type');

function series_post_type(){
    $lables = array(
        'name' => 'Series',
        'singular_name' => 'series',
        'add_new_item' => 'Add New Series',
        'new_item' => 'New Series',
        'edit_item' => 'Edit Series',
        'view_item' => 'View Series',
        'all_items' => 'All Series',    




    );

    $args = array(
        'labels' => $lables,
        'menu_icon' => 'dashicons-tickets-alt',
        'supports' => array('title' , 'thumbnail', 'excerpt','editor'), 
        'public' => true,
        'has_archive' => true,
    );

    register_post_type('series', $args);
}

add_action('init', 'series_post_type');

function custom_footer_content() {
    echo 'Copyright 2024 ebda3design. All Rights Reserved.';
}
add_action('wp_footer', 'custom_footer_content');

function custom_post_title($title,$id) {
    if (is_single() && $id == get_the_ID()) {
        $title = 'my custom title';
} 
return $title;
}

add_filter( 'the_title', 'custom_post_title', 10, 2 ); 
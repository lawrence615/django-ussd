/**
 * Created by Lawrence on 2/17/16.
 */

/**
 * get gulp from node_modules folder and pass it to node variable
 */
var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function () {
    gulp.src('resources/sass/app.scss') // Gets the styles.scss file
        .pipe(sass()) // Passes it through a gulp-sass task
        .pipe(gulp.dest('mobidevlending/modules/blog/static/css')) // Outputs it in the css folder
});

gulp.task('fonts', function () {
    gulp.src('node_modules/bootstrap-sass/assets/fonts/bootstrap/*')
        .pipe(gulp.dest('mobidevlending/modules/blog/static/fonts/bootstrap/'))

});

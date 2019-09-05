var gulp = require('gulp');
var ngAnnotate = require('gulp-ng-annotate');
var uglify = require('gulp-uglify');
var yarn = require('gulp-yarn');

gulp.task('mycyclediary', function () {
  return gulp.src(['./mycyclediary_dot_com/static/javascripts/**/*.js'])
    .pipe(ngAnnotate())
    .pipe(uglify())
    .pipe(gulp.dest('./mycyclediary_dot_com/dist'))
});

gulp.task('yarn', function () {
  return gulp.src(['./package.json', './yarn.lock'])
    .pipe(gulp.dest('./mycyclediary_dot_com/dist'))
    .pipe(yarn({ production: true }));
});

gulp.task('default', gulp.parallel('mycyclediary', 'yarn'));

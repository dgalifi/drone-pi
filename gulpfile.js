var gulp = require('gulp');
var scpClient = require('scp2');

gulp.task('default', ['watch']);

gulp.task('ssh-copy', function (cb) {
    console.log('ssh copy start...');

    scpClient.scp(
        '*.py', {
            "host": "192.168.1.207",
            "port": "22",
            "username": "pi",
            "password": "raspberry",
            "path": "/home/pi/run/"
        }, cb);
});

gulp.task('watch', function (cb) {
    gulp.watch('*.py', ['ssh-copy']);
});
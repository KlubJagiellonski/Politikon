from django_assets import Bundle, register
css = Bundle('css/bootstrap.min.css', 'css/politikon.scss', filters='scss', output='politikon_%(version)s.css')
register('css_all', css)

js = Bundle('js/libs/jquery-1.9.1.js', 'js/libs/knockout-2.2.1.js', 'js/libs/bootstrap.js', Bundle('js/app.coffee', filters='coffeescript'),
            output='politikon_%(version)s.js')
register('js_all', js)

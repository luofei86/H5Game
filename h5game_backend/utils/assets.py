from flask.ext.assets import Bundle, Environment
from .. import app

bundles = {

    # 'home_page_js': Bundle(
    #     'js/lib/jquery-1.11.3.min.js',
    #     'js/common/download.js',
    #     'js/common/navigator.js',
    #     'js/homepage.js',
    #     output= 'gen/homepage.js',
    #     filters='jsmin'
    # ),

    # 'home_page_css': Bundle(
    #     'css/component/base.css',
    #     'css/component/app-row-list.css',
    #     'css/homepage.css',
    #     output='gen/homepage.css',
    #     filters='cssmin'
    # ),

    # 'app_detail_css': Bundle(
    #     'css/lib/tinyscrollbar.css',
    #     'css/component/base.css',
    #     'css/component/app-row-list.css',
    #     'css/component/layout.css',
    #     'css/component/slide.css',
    #     'css/component/app-header.css',
    #     'css/app-detail.css',
    #     output='gen/appdetail.css',
    #     filters='cssmin'
    # ),

    # 'app_detail_js': Bundle(
    #     'js/lib/jquery-1.11.3.min.js',
    #     'js/lib/jquery.tinyscrollbar.min.js',
    #     'js/common/download.js',
    #     'js/common/navigator.js',
    #     'js/appdetail.js',
    #     output='gen/appdetail.js',
    #     filters='jsmin'
    # ),

    # 'app_list_css': Bundle(
    #     'css/lib/tinyscrollbar.css',
    #     'css/component/base.css',
    #     'css/component/layout.css',
    #     'css/component/app-header.css',
    #     'css/component/flashview.css',
    #     'css/component/pager.css',
    #     'css/app-list/panel.css',
    #     'css/app-list/app-row-list.css',
    #     'css/app-list/app-list.css',
    #     output='gen/applist.css',
    #     filters='cssmin'
    # ),

    # 'app_list_js': Bundle(
    #     'js/lib/jquery-1.11.3.min.js',
    #     'js/lib/jquery.tinyscrollbar.min.js',
    #     'js/common/download.js',
    #     'js/common/navigator.js',
    #     'js/common/pager.js',
    #     'js/app-list.js',
    #     output='gen/applist.js',
    #     filters='jsmin'
    # ),

    # 'app_search_css' :Bundle(
    #     'css/lib/tinyscrollbar.css',
    #     'css/component/base.css',
    #     'css/component/pager.css',
    #     'css/app-list/app-row-list.css',
    #     'css/app-search.css',
    #     output='gen/appsearch.css',
    #     filters='cssmin'
    # ),

    # 'app_search_js':  Bundle(
    #     'js/lib/jquery-1.11.3.min.js',
    #     'js/lib/jquery.tinyscrollbar.min.js',
    #     'js/common/download.js',
    #     'js/common/navigator.js',
    #     'js/common/pager.js',
    #     'js/app-search.js',
    #     output='gen/appsearch.js',
    #     filters='jsmin'
    # ),

    # 'auth_app_list_css': Bundle(
    #     'css/lib/tinyscrollbar.css',
    #     'css/component/base.css',
    #     'css/auth-app-list.css',
    #     output='gen/authapp.css',
    #     filters='cssmin'
    # ),

    # 'auth_app_list_js':  Bundle(
    #     'js/lib/jquery-1.11.3.min.js',
    #     'js/lib/jquery.tinyscrollbar.min.js',
    #     'js/common/download.js',
    #     'js/common/navigator.js',
    #     'js/auth-app-list.js',
    #     output='gen/authapp.js',
    #     filters='jsmin'
    # ),
}

assets = Environment(app)
assets.register(bundles)
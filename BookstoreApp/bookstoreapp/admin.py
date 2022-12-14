from bookstoreapp import db, app, dao
from bookstoreapp.models import UserRole, Rule, Product
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class StatsViewG(BaseView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue_by_prod(sel_month=request.args.get('sel_month'))

        return self.render('admin/statsg.html', stats=stats)

class StatsViewB(BaseView):
    @expose('/')
    def index(self):
        stats = dao.product_revenue_by_month(sel_prod=request.args.get('sel_prod'),
                                             from_month=request.args.get('from_month'),
                                             to_month=request.args.get('to_month'))
        return self.render('admin/statsb.html', stats=stats)


class LogoutView(ModelView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Quản trị hệ thống bán sách', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(ModelView(Product, db.session, name='Sản phẩm'))
admin.add_view(ModelView(Rule, db.session, name='Thay đổi quy định'))
admin.add_view(StatsViewG(name='Xem thống kê theo tháng'))
admin.add_view(StatsViewB(name='Xem thống kê theo sản phẩm'))
# admin.add_view(LogoutView(name='Đăng xuất'))


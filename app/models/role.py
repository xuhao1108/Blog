from app.utils.extensions import db


# class Permission(object):
#     # 关注
#     FOLLOW = 1
#     # 评论
#     COMMENT = 2
#     # 写文章
#     WRITE = 4
#     # 管理他人评论
#     MODERATE = 8
#     # 管理员
#     ADMIN = 16


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    default = db.Column(db.Boolean())
    # permission = db.Column(db.Integer(), default=0)
    users = db.relationship('User', backref='role', lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def insert_roles():
        """
        将所有角色添加到数据库中
        :return:
        """
        # 默认三种角色
        roles = ['User', 'Administrator', 'SuperAdministrator']
        for role in roles:
            # 创建role模型对象
            r = Role(name=role)
            # 添加到数据库
            db.session.add(r)
        # 提交操作到数据库
        db.session.commit()
        # 普通用户，管理员，超级管理员
        # roles = {
        #     'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
        #     'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
        #     'SuperAdministrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,
        #                            Permission.ADMIN],
        # }
        # 依次将各角色添加到数据库中
        # default_role = 'User'
        # for key in roles.keys():
        #     # 获取role模型对象，若无，则创建
        #     r = Role.query.filter_by(name=key).first()
        #     if not r:
        #         r = Role(name=key)
        #     # 重置权限
        #     r.reset_permission()
        #     # 重新赋予权限
        #     for per in roles[key]:
        #         r.add_permission(per)
        #     # 判断是否是默认角色
        #     r.default = (key == default_role)
        #     # 添加到数据库
        #     db.session.add(r)

        # def reset_permission(self):
        #     self.permission = 0
        #
        # def add_permission(self, per):
        #     if not self.has_permission(per):
        #         self.permission += per
        #
        # def delete_permission(self, per):
        #     if not self.has_permission(per):
        #         self.permission -= per
        #
        # def has_permission(self, per):
        #     return self.permission & per == per

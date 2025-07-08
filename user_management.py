# user_management.py
from flask import Flask, Blueprint, request, jsonify
from flask_restx import Api, Namespace, fields, Resource
from database import Database

app = Flask(__name__)
api = Api(app, version='1.0', title='用户管理 API', description='用户管理相关接口文档')

user_ns = Namespace('users', description='用户操作')
api.add_namespace(user_ns)

# 定义模型，用于 Swagger UI 的请求体描述
user_model = api.model('UserModel', {
    'telegram_id': fields.String(required=True, description='用户的 Telegram ID'),
    'mode': fields.String(required=True, description='用户关系模式', enum=['friends', 'long-term_compinionship', 'short-term_compinionship'])
})

# 定义响应模型，用于 Swagger UI 的成功创建响应体描述
user_creation_success_response = api.model('UserCreationSuccessResponse', {
    'message': fields.String(description='响应消息'),
    'user_data': fields.Nested(user_model, description='创建的用户数据')
})

@user_ns.route('/male_users')
class MaleUsersAPI(Resource):
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_creation_success_response, code=201)
    @user_ns.response(400, 'Invalid Input')
    def post(self):
        """
        创建一个新的男性用户,first,last,id,
        gender,question。
        """
        data = request.get_json()

        if not data:
            user_ns.abort(400, "请求失败，请确保发送 JSON 格式的数据")

        telegram_id = data.get('telegram_id')
        mode = data.get('mode')

        if not telegram_id:
            user_ns.abort(400, "缺少 'telegram_id' 参数")

        if mode not in ['friends', 'long-term_compinionship', 'short-term_compinionship']:
            user_ns.abort(400, "无效的 'mode' 参数，请选择 'friends'、'long-term_compinionship' 或 'short-term_compinionship'")

        try:
            new_user = {"telegram_id": telegram_id, "mode": mode}
            inserted_id = Database.insert_one('users', new_user)
            print(f"用户数据已插入 MongoDB，ID: {inserted_id}")

            return {
                "message": "新男性用户创建成功",
                "user_data": {
                    "telegram_id": telegram_id,
                    "mode": mode
                }
            }, 201
        except Exception as e:
            user_ns.abort(500, f"创建用户失败: {e}")

if __name__ == '__main__':
    # 连接数据库
    Database.connect()
    try:
        app.run(host='127.0.0.1', debug=True)
    finally:
        # 确保在应用关闭时关闭数据库连接
        Database.close() 
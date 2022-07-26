from flask import Flask,request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})" 
    
#db.create_all()
video_put_args = reqparse.RequestParser()

video_put_args.add_argument("name", type=str, help="Plz enter correct name",required=True)
video_put_args.add_argument("views", type=int, help="Plz enter correct view",required=True)
video_put_args.add_argument("likes", type=int, help="Plz enter correct like",required=True)
videos={}
 
def abort_if_video_doesnot_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video_id is not valid")
        
def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):
    
    @marshal_with(resource_fields)
    def get(self,video_id):
        #abort_if_video_doesnot_exist(video_id)
        print("Parsing args for get")
        print("id=",video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result
        
    @marshal_with(resource_fields)
    def put(self,video_id):
        print("id=",type(video_id))
        #abort_if_video_exists(video_id)
        print("Parsing args for put")
        args = video_put_args.parse_args()
        #print(args['name'])
        print(request.form['name'])
        
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken...")
            
        video = VideoModel(id=video_id, name=request.form['name'], views=request.form['views'], likes=request.form['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
        #args = video_put_args.parse_args()
        #print(args)
        #video_details={'name':args['name'],'views':args['views'],'likes':args['likes']}
        #video_details={'name':request.form['name'],'views':request.form['views'],'likes':request.form['likes']}
        #print(video_details)
        #videos[video_id]=video_details  
        #return video_details, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        #args = video_update_args.parse_args()
        print("Parsing args for patch")
        print("id=",type(video_id))
        result = VideoModel.query.filter_by(id=video_id).first()
        
        if not result:
            abort(404, message="Video doesn't exist, cannot update")
            
        print("value before update is:",result)
        try:
            result.name = request.form['name']
        except:
            pass
        try:
            result.views = request.form['views']
        except:
            pass
        try:
            result.likes = request.form['likes']
        except:
            pass
        #print("after abort",request.form['name'])           
        print("value after update is:",result)
        db.session.commit()
        return result
    
    @marshal_with(resource_fields)
    def delete(self,video_id):
        result = VideoModel.query.get(video_id)
        if not result:
            abort(404, message="Video doesn't exist, cannot delete")
        
        db.session.delete(result)
        db.session.commit()
        return result

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True,port=6000)
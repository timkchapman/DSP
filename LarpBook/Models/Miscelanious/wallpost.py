from LarpBook import db

class WallPost(db.Model):
    __tablename__ = 'wallpost'
    id = db.Column(db.Integer, primary_key=True)
    wall_id = db.Column(db.Integer, db.ForeignKey('user_wall.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    post_time = db.Column(db.Time, nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)
    post_visibility = db.Column(db.String(50), nullable=False)
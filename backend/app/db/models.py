from app.db.database import Base

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    total_posts = Column(Integer)

    posts = relationship("Post", back_populates="account",
                         cascade="all, delete")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    shortcode = Column(String(32), unique=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    date_utc = Column(DateTime, index=True)
    caption = Column(Text)
    likes = Column(Integer)
    comments = Column(Integer)
    url = Column(String)
    video_url = Column(String)
    typename = Column(String)

    account = relationship("Account", back_populates="posts", lazy="selectin")

    # account = relationship("Account", back_populates="posts")

    # __table_args__ = (
    #     Index(
    #         "idx_posts_caption_trgm",
    #         caption,
    #         postgresql_using="gin",
    #         postgresql_ops={"caption": "gin_trgm_ops"},
    #     ),
    # )


# Index("idx_posts_caption_gin", Post.caption, postgresql_using="gin", postgresql_ops={"caption": "gin_trgm_ops"}
#       )
